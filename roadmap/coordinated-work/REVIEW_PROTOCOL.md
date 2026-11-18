# Review Protocol: Source Discovery, Claim Appraisal, and Transfer

**Coordinated Work · research programme v0.1**

This protocol develops a scoping review and an evidence map for organizational decisions supported by agents. It separates finding a record, establishing its identity, reading a work, evaluating a claim, and transferring that claim to an organizational setting. The present protocol follows an exploratory search; it is not a preregistration of searches already performed.

## Questions and scope

The review asks how prior work represents organizational needs; connects demand, processes, resources, skills, and quality; handles shared resources and delayed actions; evaluates uncertainty; and establishes the evidence needed for a decision. It also asks where reported benefits hold, which comparisons support them, and which counterexamples limit transfer.

Search families include workforce planning, skills-based staffing, resource-constrained scheduling, queueing networks, production control, organizational cybernetics, sociotechnical systems, causal productivity, process mining, digital twins, enterprise agents, environment grounding, forecast reconciliation, and robust control. Context families include manufacturing, services, projects, knowledge work, logistics, healthcare operations, and public services. Combining these dimensions is preferable to one broad query whose results obscure their origin.

Primary publisher pages, author and institutional repositories, official classifications, standards bodies, bibliographic indexes, and backward/forward citation searches are eligible discovery routes. Books, papers, preprints, standards, and datasets receive distinct source types. A business narrative can supply a managerial proposition without being treated as a theorem or controlled experiment.

Reporting should use the relevant elements of [PRISMA-ScR](https://doi.org/10.7326/M18-0850) and [PRISMA-S](https://doi.org/10.1186/s13643-020-01542-z). Reporting compliance does not establish the scientific quality of the included evidence.

## Current corpus and extraction limitations

The [manifest](corpus/corpus_manifest.json) records 157 checked core records and 1,019 citation candidates, retaining 1,176 records from 1,177 inputs after one confirmed merge. It does not report 1,176 unique works. Twenty-six same-title/year groups and four near-title pairs remain unresolved. Completed full-text critical appraisals remain zero.

The bulk candidates come from two entry points: [Ernst et al., An Annotated Bibliography of Personnel Scheduling and Rostering (2004)](https://doi.org/10.1023/B:ANOR.0000019087.46656.e2), and [Van den Bergh et al., Personnel scheduling: A literature review (2013)](https://doi.org/10.1016/j.ejor.2012.11.029), using its [November 2012 author version](https://lirias.kuleuven.be/retrieve/c911cbdc-9bc8-4047-9a8f-3fa6319f70ae).

The first extraction retains 713 citation records, including two ambiguous pairs. The second retains 306 numbered references. Its review reports 291 examined works; a review's study count and its reference-list length are different quantities. Bibliography extraction can discover a work without verifying the cited spelling, year, edition, DOI, or conclusion. It also inherits the review's coverage and publication-date limits.

Retain the parent document and version, retrieval date, bibliography location or reference ordinal, extracted text, parser decisions, and unresolved ambiguities. Preserve an original capture or content hash when available. A later correction must retain the earlier record and explain the change. Extraction should be reproducible from the same captured material; independently resolving the cited publication is a separate step. No mass OpenAlex API import was performed in this initial stage.

## Records, identities, and versions

A bibliographic record needs a local stable identifier, title, authors as recorded, date and date interpretation, source type, identifier when verified, canonical or discovery URL, provenance, and current review status. Missing metadata remain unknown. A plausible DOI must never be completed from a title guess.

Resolve identities using verified identifiers and the combination of title, authors, venue, edition, and publication history. Exact title/year agreement flags a candidate relationship; it does not by itself establish identity. Track preprint-to-journal, correction, translation, edition, retraction, and duplicate relationships explicitly. A book's new edition may change relevant content even when its title is unchanged.

Separate original publication dates from digitization or platform-migration dates. Record both online-first and issue dates when they differ. An official standard's published revision, draft revision, amendment, and current status require separate treatment. Versions used to support a claim must be fixed before an experiment or release.

Possible record states are: discovered; bibliographic identity checked; abstract screened; full text available; full text reviewed; critically appraised; claim extracted; transfer assessed. Availability is not reading, and reading is not appraisal. Reviewers record transitions, exclusions, and reasons rather than promoting every discovered citation to accepted evidence.

## Claim cards and critical appraisal

Each claim card records the proposition in its own terms, source and version, precise page/section/theorem, evidence type, variables and units, assumptions, uncertainty, known exceptions, and scope. It then records the proposed organizational use, any adaptation, the proposed KC contribution, and the engineering or empirical check that could challenge it. Keep the source author's statement, the reviewer's interpretation, and an adopted organizational rule distinguishable.

For a theorem, inspect definitions, assumptions, proof obligations, and limiting cases. For an empirical study, inspect sampling, measurement, confounding, identification, missingness, uncertainty, and the comparator. For a simulation, inspect the conceptual model, implementation, input calibration, verification, and validation against the intended system. For a standard, inspect its version, scope, and normative status; a standard is not evidence that adopting it causes a performance gain.

For example, [Little's queueing result](https://doi.org/10.1287/opre.9.3.383) requires consistent definitions of the averages involved. It does not establish that lowering WIP always increases output, or prescribe a workforce size. Such extensions require their own assumptions and tests. Similarly, a corporate-agent benchmark can support claims about its measured tasks without establishing beneficial real-world staffing decisions.

Use independent coding on a defined overlap sample and adjudicate disagreements. Record agreement and unresolved interpretations. Prioritize influential assumptions, closest competing approaches, negative findings, and operational counterexamples over citation popularity alone.

The novelty assessment must explicitly compare the proposed profile with [Malone and Crowston's coordination framework](https://doi.org/10.1145/174666.174668), including its dependency classes and associated coordination mechanisms. Their interdisciplinary framing predates this programme. The [author version](https://ccs.mit.edu/papers/ccswp157.html) also makes that conceptual scope accessible. A new diagram of dependencies is not sufficient evidence of a new theory. A potentially distinct contribution would need to specify and demonstrate what the KC profile adds to decision evidence, applicability checks, or outcomes beyond that prior work and its successors.

## Reproducibility and completion gates

For each future search export, record the exact query, provider/database, date, filters, returned count, pagination or cutoff, export version, and applicable access limits. Preserve the distinction between intended query scope and what was actually retrieved. Record failed or partial retrievals. Subscription access or an inaccessible full text must remain visible as an evidence limitation.

The first reading set should establish the nearest prior art and the assumptions that define the proposed models. Expand forward into recent citations and laterally into underrepresented industries. Stop a review version when its stated questions have defensible coverage and its remaining gaps are explicit, not when a target bibliography count is reached.

Acceptance requires a reproducible search/extraction history, resolved identities for cited claims, traceable appraisals, a map of competing explanations, and an explicit novelty boundary. Unresolved candidates can remain in a discovery appendix but cannot carry a scientific conclusion. Review outputs feed the [72-step plan](plan/roadmap_steps.json); the plan records intended work, not completion of these gates.
