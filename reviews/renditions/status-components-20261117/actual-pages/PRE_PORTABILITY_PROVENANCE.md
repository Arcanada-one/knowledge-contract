# Harness provenance before portability repair

`badge_actual_page_probe_pre_portability.py` preserves the exact script bytes
present immediately before the portability edits. SHA-256:
`4d5f2c449352c06f43038df39728e8de19be11ce143ea4faa49204f22dff97e0`.

This is the later CLI-adapted script, not the exact script that executed the
original completed54 receipt. The original executed script had already been
edited in place before a separate copy was made. Its exact file was not
preserved; no reconstructed replacement is presented as original evidence.
The actual old54 receipt and setup-failure record remain unchanged.

The portable successor SHA-256 is
`f12f09fac9dfb50abf25af26ddf3f625c1ea46af311381f774f145180de61987`.
It created a fresh same-script baseline in `portable_old_baseline/` and a
separate expected-failure run in `portable_old_expected_refusal/`. Each has
its own `execution.json`, stdout, stderr and complete result. The ordinary
run exited0; the same script with `--expect-fixed` exited1 as required.
Both result files have SHA-256
`50e0091abf0a2aa49e2dd1b470c78c5d72e4b4b84ba30c717350551c73b414bf`.
The explicit commands and different process exits remain in the respective
execution records. All54 input hashes, condition labels and old-checker
decisions matched the completed original54 receipt. Source bytes were hashed
before and after both runs and remained unchanged.
