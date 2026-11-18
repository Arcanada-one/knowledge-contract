# Coordinated flow probe — revision 2

A small, reproducible **mathematical illustration and finite implementation check** for a three-stage fluid line. It evaluates specified release limits; no agent or optimizer chooses them. It provides no empirical validation of a company model, hiring recommendation, or general stability claim.

## Run

Python 3; standard library only. From this directory:

```bash
python3 run_flow_probe.py --inputs cases.json --out raw_results.json
python3 verify_flow_probe.py --inputs cases.json --actual raw_results.json --expected expected_results.json --report verification_report.json
```

The recorded revision 2 run contains **10 cases, 100 periods, and 190 elementary checks with zero violations**. Check counts are not counts of independent scientific experiments. Arithmetic uses exact rational numbers. Noninteger output values are stored as fraction strings.

## Explicit demand accounting

`demand_per_period` means potential need / maximum customer acceptance in that period. Each record reports:

- `shipped`: accepted good units;
- `unserved_demand = demand_per_period - shipped`: unserved potential;
- `cumulative_unserved_demand`: the sum of unserved potential so far.

**There is no customer-order backlog state or backlog dynamics.** Unserved potential is measured but does not carry forward as a new order. It should not be interpreted as measured lost sales in a real business.

The base gated case demonstrates why zero internal work in process (WIP) is insufficient: demand is 70 and shipments are 60 per period. Internal WIP stays at zero, while **10 units per period, 100 over the run, remain unserved**. The gate removes avoidable internal accumulation; it does not resolve the shortage of deliverable output.

## Assumptions

One homogeneous good, three sequential stages, zero initial inventories, constant deterministic inputs, no scrap, and unlimited internal and finished-goods storage. Supply is an availability ceiling; unused supply remains outside the modeled boundary. Zero transit lag lets an upstream output feed downstream processing in the same period. This is a fluid material-balance approximation, not an item-level discrete-event model.

Nominal capacity `c` is processing work per period. Availability `a` and work content `w` give effective good-unit capacity `c*a/w`. Setup loss and rework overhead are fixed aggregate adjustments, not explicit stochastic failure/rework cycles. All admission limits are hand-specified experimental inputs.

## Results

All cases run for 10 periods. Inventories and unserved potential are end-of-run totals.

| Case | Shipped per period | Internal WIP | Finished goods | Unserved potential |
| --- | ---: | ---: | ---: | ---: |
| Base local release 80 | 60 | 200 | 0 | 100 |
| Base gated release 60 | 60 | 0 | 0 | 100 |
| Increase non-bottleneck capacities | 60 | 200 | 0 | 100 |
| Increase stage 2 capacity to 85; demand 70 | 70 | 0 | 0 | 0 |
| Demand 100; material availability 80 | 80 | 0 | 0 | 200 |
| Local release 80; demand 50 | 50 | 0 | 300 | 0 |
| Stage 3 capacity 45 | 45 | 350 | 0 | 250 |
| Stage 2 availability 2/3 | 60 | 0 | 0 | 400 |
| Stage 2 work content 3/2 | 60 | 0 | 0 | 400 |
| No material | 0 | 0 | 0 | 700 |

## Independent checks

`expected_results.json` holds manual fixtures; it is never generated from simulation output. `analytical_bound.py` does not import the simulator. From conservation and the work required by every shipped unit, over T periods:

`Y(T) <= T * min(S, D, c1*a1/w1, c2*a2/w2, c3*a3/w3)`.

This bound assumes the model conditions above. Its attainability does not generalize to arbitrary organizations. The verifier also checks stage balances, processing limits, overall material conservation, and `potential demand = shipped + unserved potential`. It explicitly checks the zero-WIP / unserved-demand counterexample.

## Evidence and history

- `cases.json`: assumptions, units, inputs, demand semantics, and revision origin.
- `raw_results.json`: every period, totals, revision origin, and input SHA-256.
- `expected_results.json`: independent hand-written expectations.
- `verification_report.json`: executed comparisons and input/output/fixture hashes.
- `origin.json`: revision 2 origin and reason for the change.
- `development/v1/`: eight unmodified files from the executed revision 1, with `snapshot_manifest.json` hashes. Revision 1 did not expose unserved potential demand.
- `README.ru.md`: longer Russian explanation for the accompanying research dossier.

Next studies require explicit service times and finite buffers, uncertain arrivals and processing, multiple products, shared resources, customer-backlog dynamics, independent data, and predefined decision-quality criteria. Agent experiments must separately evaluate actual agent choices from supplied knowledge artifacts.

## Historical formatting

The retained revision-1 README is byte-pinned in its snapshot manifest. Its local Markdown configuration follows the upstream [configuration guidance](https://github.com/DavidAnson/markdownlint-cli2#configuration), inherits the root rules and exempts only table-separator spacing (MD060), preserving the original bytes. All other lint rules and the numerical/snapshot checks remain applicable. Current documents use the required table spacing.
