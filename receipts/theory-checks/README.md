# Theory check receipts

One JSON receipt per run of a check registered in [`evaluation/kc3-checks.json`](../../evaluation/kc3-checks.json), schema `KC3CheckReceipt/v1`, and one `KC3RevisionProposal/v1` file for every refuted or weakened outcome. A receipt cites the SHA-256 and commit of the registry; `tools/check_kc3_registry.py` and its tests reject a receipt that cites another digest, skips a gate, has a failed control and still claims `supported` or `refuted`, or exceeds its recorded spend cap. This directory is empty until the first check has run.
