"""Finite situation-state reference model. No I/O, LLM, grants or effects.

Only integer times in one declared clock domain are modeled. Readiness means
structural availability, never permission. All identities are fixture labels.
"""
from dataclasses import dataclass, asdict
from itertools import count
import json

def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)

@dataclass(frozen=True)
class Observation:
    key: str
    scope: str
    source: str
    event_id: str
    sequence: int
    value: object
    state: str
    observed_at: int
    received_at: int
    ttl: int | None = None
    dependencies: tuple[str, ...] = ()

    def __post_init__(self):
        for name in ("key", "scope", "source", "event_id"):
            if not isinstance(getattr(self, name), str) or not getattr(self, name):
                raise ValueError(name + " must be a nonempty string")
        for name in ("sequence", "observed_at", "received_at"):
            if type(getattr(self, name)) is not int or getattr(self, name) < 0:
                raise ValueError(name + " must be a nonnegative integer")
        if self.ttl is not None and (type(self.ttl) is not int or self.ttl <= 0):
            raise ValueError("ttl must be a positive integer or None")
        if self.state not in {"KNOWN", "UNKNOWN", "CONFLICT"}:
            raise ValueError("unsupported observation state")
        if self.state != "KNOWN" and self.value is not None:
            raise ValueError("unknown/conflict uses None, never a guessed value")
        if not isinstance(self.dependencies, tuple) or any(
                not isinstance(k, str) or not k for k in self.dependencies):
            raise ValueError("dependencies must be a tuple of nonempty keys")
        canonical(self.value)

    def payload(self):
        data = asdict(self)
        # Receipt is transport metadata. Re-delivery does not change the event.
        data.pop("received_at")
        return canonical(data)

class Model:
    _ids = count(1)

    def __init__(self):
        self.model_id = "fixture-model-" + str(next(self._ids))
        self.generation = 0
        self.latest = {}
        self.events = {}
        self.source_sequences = {}
        self.versions = {}
        self.dependency_versions = {}
        self.clock_watermark = None
        self.clock_invalid = False

    def _clock(self, now):
        if type(now) is not int or now < 0:
            raise ValueError("now must be a nonnegative integer")
        if self.clock_watermark is not None and now < self.clock_watermark:
            self.clock_invalid = True
        self.clock_watermark = max(now, self.clock_watermark or 0)

    def version(self, scope, key):
        return self.versions.get((scope, key), 0)

    def ingest(self, observation):
        self._clock(observation.received_at)
        event = (observation.source, observation.event_id)
        payload = observation.payload()
        if event in self.events:
            return "DUPLICATE" if self.events[event] == payload else "DUPLICATE_REJECTED"
        self.events[event] = payload
        slot = (observation.scope, observation.key, observation.source)
        stream = (observation.scope, observation.source)
        previous_sequence = self.source_sequences.get(stream)
        if previous_sequence is not None and observation.sequence <= previous_sequence:
            return "OUT_OF_ORDER" if observation.sequence < previous_sequence else "SEQUENCE_REJECTED"
        self.source_sequences[stream] = observation.sequence
        # Copy JSON values so a caller cannot mutate stored evidence in place.
        observation = Observation(**{
            **asdict(observation),
            "value": json.loads(canonical(observation.value)),
            "dependencies": observation.dependencies,
        })
        self.latest[slot] = observation
        self.dependency_versions[slot] = {
            key: self.version(observation.scope, key)
            for key in observation.dependencies
        }
        identity = (observation.scope, observation.key)
        self.versions[identity] = self.version(*identity) + 1
        self.generation += 1
        return "UPDATED"

    def _observations(self, scope, key):
        return sorted(
            (obs for (s, k, _), obs in self.latest.items() if s == scope and k == key),
            key=lambda obs: obs.source,
        )

    def _temporal_state(self, observation, now):
        if (self.clock_invalid or observation.observed_at > observation.received_at
                or observation.observed_at > now):
            return "INVALID_TIME"
        if observation.ttl is not None and now - observation.observed_at >= observation.ttl:
            return "STALE"
        return "KNOWN"

    def _resolve(self, scope, key, now, visiting):
        if key in visiting:
            return {"state": "CYCLE", "value": None, "reasons": ["dependency cycle"]}
        observations = self._observations(scope, key)
        if not observations:
            return {"state": "MISSING", "value": None, "reasons": ["no observation"]}
        problems = []
        for obs in observations:
            temporal = self._temporal_state(obs, now)
            if temporal != "KNOWN":
                problems.append(temporal)
            if obs.state != "KNOWN":
                problems.append(obs.state)
            slot = (scope, key, obs.source)
            if any(self.version(scope, dep) != version
                   for dep, version in self.dependency_versions[slot].items()):
                problems.append("INVALIDATED")
            for dep in obs.dependencies:
                state = self._resolve(scope, dep, now, visiting | {key})["state"]
                if state != "KNOWN":
                    problems.append("DEPENDENCY_NOT_READY")
        known = {canonical(obs.value) for obs in observations if obs.state == "KNOWN"}
        if len(known) > 1:
            problems.append("CONFLICT")
        priority = ("INVALID_TIME", "CONFLICT", "UNKNOWN", "STALE", "INVALIDATED",
                    "DEPENDENCY_NOT_READY")
        state = next((s for s in priority if s in problems), "KNOWN")
        return {
            "state": state,
            "value": json.loads(next(iter(known))) if state == "KNOWN" else None,
            "reasons": sorted(set(problems)),
            "sources": [asdict(obs) for obs in observations],
        }

    def resolve(self, scope, key, now):
        self._clock(now)
        return self._resolve(scope, key, now, set())

    def _closure(self, scope, keys):
        found, active, cycles = set(), set(), set()
        def visit(key):
            if key in active:
                cycles.add(key)
                return
            if key in found:
                return
            found.add(key)
            active.add(key)
            dependencies = {
                dep for obs in self._observations(scope, key) for dep in obs.dependencies
            }
            for dep in sorted(dependencies):
                visit(dep)
            active.remove(key)
        for key in sorted(set(keys)):
            visit(key)
        return sorted(found), sorted(cycles)

    def project(self, scope, required, optional, now, budget, costs=None):
        self._clock(now)
        if type(budget) is not int or budget < 0:
            raise ValueError("budget must be a nonnegative integer")
        costs = dict(costs or {})
        if any(type(v) is not int or v <= 0 for v in costs.values()):
            raise ValueError("costs must be positive integers")
        cost = lambda key: costs.get(key, 1)
        closure, cycles = self._closure(scope, required)
        states = {key: self._resolve(scope, key, now, set()) for key in closure}
        total = sum(cost(key) for key in closure)
        reasons = ["cycle:" + key for key in cycles]
        reasons += [key + ":" + states[key]["state"] for key in closure
                    if states[key]["state"] != "KNOWN"]
        if self.clock_invalid:
            reasons.append("CLOCK_INVALID")
        status = "NOT_FIT" if total > budget else ("NOT_READY" if reasons else "READY")
        if total > budget:
            reasons.append("mandatory closure exceeds budget")
        included = list(closure) if total <= budget else []
        omitted = []
        if status == "READY":
            for key in dict.fromkeys(optional):
                if key in included:
                    continue
                extra, extra_cycles = self._closure(scope, [key])
                extra = [candidate for candidate in extra if candidate not in included]
                extra_states = {k: self._resolve(scope, k, now, set()) for k in extra}
                bad = [k + ":" + v["state"] for k, v in extra_states.items()
                       if v["state"] != "KNOWN"]
                if extra_cycles or bad:
                    omitted.append({"key": key, "reason": "NOT_READY", "details": bad})
                elif total + sum(cost(k) for k in extra) > budget:
                    omitted.append({"key": key, "reason": "BUDGET"})
                else:
                    included.extend(extra)
                    states.update(extra_states)
                    total += sum(cost(k) for k in extra)
        else:
            omitted = [{"key": key, "reason": "MANDATORY_CONTEXT_UNAVAILABLE"}
                       for key in dict.fromkeys(optional) if key not in closure]
        snapshot = None
        if status == "READY":
            snapshot = {
                "model_id": self.model_id, "scope": scope, "generation": self.generation,
                "required": list(sorted(set(required))), "closure": closure,
                "versions": {key: self.version(scope, key) for key in closure},
            }
        return {
            "status": status, "scope": scope, "generation": self.generation,
            "required_closure": closure, "required_cost": sum(cost(k) for k in closure),
            "included": included, "cost": total if included else 0, "budget": budget,
            "values": {key: states[key] for key in included},
            "omitted": omitted, "reasons": reasons, "snapshot": snapshot,
            "readiness_grants_permission": False,
        }

    def _scope_matches(self, snapshot, scope):
        return snapshot["scope"] == scope

    def validate(self, snapshot, scope, now):
        self._clock(now)
        reasons = []
        if snapshot is None:
            return {"status": "INVALID", "reasons": ["NO_READY_SNAPSHOT"]}
        if snapshot["model_id"] != self.model_id:
            reasons.append("MODEL_CHANGED")
        if not self._scope_matches(snapshot, scope):
            reasons.append("SCOPE_CHANGED")
        closure, cycles = self._closure(scope, snapshot["required"])
        if closure != snapshot["closure"] or cycles:
            reasons.append("CLOSURE_CHANGED")
        for key, version in snapshot["versions"].items():
            if self.version(scope, key) != version:
                reasons.append("CRITICAL_GENERATION_CHANGED:" + key)
            state = self._resolve(scope, key, now, set())["state"]
            if state != "KNOWN":
                reasons.append(key + ":" + state)
        if self.clock_invalid:
            reasons.append("CLOCK_INVALID")
        return {"status": "INVALID" if reasons else "VALID", "reasons": reasons}

    def refresh(self, scope, required, now, trigger, event_key=None, changed=False,
                snapshot=None):
        self._clock(now)
        if trigger not in {"EVENT", "HEARTBEAT", "EXPIRY", "PRE_ACTION"}:
            raise ValueError("unsupported refresh trigger")
        closure, _ = self._closure(scope, required)
        if trigger == "HEARTBEAT":
            return {"reason": "NO_RELEVANT_CHANGE", "observe": [], "request_model_call": False}
        if trigger == "EVENT":
            relevant = changed and event_key in closure
            return {"reason": "RELEVANT_EVENT" if relevant else "NO_RELEVANT_CHANGE",
                    "observe": [], "request_model_call": bool(relevant)}
        observe = [key for key in closure
                   if self._resolve(scope, key, now, set())["state"] != "KNOWN"]
        invalid = (trigger == "PRE_ACTION" and snapshot is not None
                   and self.validate(snapshot, scope, now)["status"] != "VALID")
        return {
            "reason": "OBSERVATION_NEEDED" if observe else
                      ("SNAPSHOT_CHANGED" if invalid else "FRESH"),
            "observe": observe,
            "request_model_call": bool(invalid and not observe),
        }

