# Complete-corpus site consumer rehearsal

17 November 2026. KC-Brain producer-side integration candidate for the existing
site owner. Same-controller author assistance is not independent review. This
record does not establish publication, translation acceptance or native admission.

## Exact inputs and initial refusal

The site input is `Arcanada-one/contract-place-site` at
`4475115ae03fc904aff3c7010ff298865bcbed44`. The publication source is the complete
36-work/72-rendition candidate at
`6eec88097cf5255543c792e53c92f75c0d483728`; the separate roadmap stays at
`55e279c43dc9bcf8732467a32661c2ac4b7cf920`. The runtime is Node 24.22.1 and
Pandoc 3.1.3. No canonical mailbox, live site checkout or external branch was
changed by the local rehearsal.

The first full build applied the previously retained seven-file status-support
patch unchanged and changed the publication pin to the named source. All
manuscripts compiled, but the existing status-label gate refused nine pages:

| Source page | Referenced work | Required public status | Locales |
| --- | --- | --- | --- |
| Source History | Semantic Verification | Research draft | EN, RU, zh-Hans |
| Source Rule Checks | Semantic Bridge | Engineering draft | EN, RU, zh-Hans |
| Research Foundations | Agent Situation | Research draft | EN, RU, zh-Hans |

The direct rendition-consumer PASS therefore did not imply complete site
integration. The failing surface was the reader's presentation of linked work
statuses, outside the scientific manuscript body. The original refusal is
preserved separately; no manuscript was edited to satisfy a presentation check.

## Successor changes and evidence boundary

The successor presents linked-work statuses in the reader sidebar using the
catalogue's work identity, localized title and public status. The original
scientific HTML and source-link destinations remain intact. Repeated links to
one work produce one sidebar entry; different works sharing a status retain
their individual identities.

A second real gap was observed on Semantic Verification's links to Meaning
Geometry sections. Exact-href matching missed fragment links, and the page's
own research-draft badge concealed the missing linked-work badge from the
former page-level label check. The necessary invariant is a label bound to
the exact work, not mere presence of the same label somewhere on the page.

The publication inventory checks also retain exact work identity and type;
they must not accept a same-count substitution when the current catalogue is
expanded from 31 to 36 works. The expected population is eleven papers,
thirteen specifications, eight studies, a glossary, a bibliography and two
appendices. Its 72 target-language bodies yield 108 canonical reader pages.

The candidate README describes that publication source and ten daily
Journal issues in thirty localized article pages. Dated 31-work/62-rendition
and route-count evidence remains historical evidence of its original input.

## Historical links remain bound to their source

Roadmap RM-12 refers to Geometry at the older roadmap revision. Its Git blob
is `077c13ad7e8d47646cd04ed2bdbeadceef48f9e3`, 26,477 bytes, SHA-256
`9462dc29258c66a907f6f2852c2d8f56fd59443658da8474f67bc52a78ee57aa`.
The current corpus's Geometry is blob
`ae74a2b7dfb768a2447622680635540c4a658387`, 34,847 bytes, SHA-256
`d6833494550f82321df97e814898b3e00651ee07d3a9b2cbf44f5235a7941a70`.
These identities were read from both exact Git revisions.

The existing renderer correctly retains the immutable historical GitHub URL
when these bytes differ. It must not redirect that citation to the current
local reader or infer the current work's status for the historical document.
Three older roadmap test expectations incorrectly assumed such a current
link. Their successor expectations preserve and check the entire field
text and exact historical address, while retaining distinct positive and
adverse controls for genuinely current links. No production source-binding
rule or roadmap pin is relaxed to satisfy a stale test expectation.

## Observed results and retained records

The [17-input successor patch](site-consumer/site-36x72-consumer-successor.patch)
has SHA-256
`8f07e0919ab142d1bda27e230a2bea48a4d7e46829ac3de0b65bffe0c891de8d`.
The [local execution receipt](site-consumer/consumer-rehearsal-receipt.json)
binds it to exact inputs, tool versions, commands, output digests and logs.
Its metadata correction retains the previous receipt and identifies all three
test/validation-only files changed after generation. Renderer and generated
bytes did not change in those later edits; the final patch is replayed as one
input in the hosted workflow.

| Executed surface | Observed result |
| --- | --- |
| Full site generation | PASS; 36 works, 72 target bodies, 108 canonical readers |
| HTML and internal links | 354 HTML files, 353 index routes; 22,206 internal links checked |
| Journal and feeds | Ten daily issues in thirty localized pages; six feeds with ten entries each |
| Publication, papers, links, roadmap and localization gates | Five successful standalone checks |
| Python suites | 22 build, 20 localization, 37 roadmap and 11 programme tests passed |
| JavaScript UI suite | 752 checks passed |
| Actual generated-page adverse control | Three positive pages passed; three linked-work badge omissions refused |

The [actual-page control](site-consumer/check_actual_status_binding.py) copies
the generated Semantic Verification reader for each language and removes only
the Meaning Geometry status wrapper. Its own research-draft badge and the
actual Geometry fragment link remain. The checker must refuse the missing
Geometry binding by name, then accept the restored page; retained real output
files must remain byte-identical. This exercises the observed failure, beyond
synthetic markup fixtures. Its [result](site-consumer/actual-status-control.json)
retains original and mutant page digests.

The receipt preserves the first nine-page refusal, the initially incomplete
inventory checks, one implementation import error and outdated programme/
roadmap assertions. The corrected receipt also records that an observer's
initial claim about the ordering of the roadmap guard was unsupported; only
the successful rerun explicitly fixes Pandoc 3.1.3 in that command's PATH.
External URLs were collected but not fetched by the internal-link gate.

## Reproduction and release scope

The successor patch is an input to the existing site integration, not an
installed site change. Apply it only to the exact named site base, verify its
digest and supply detached source and roadmap worktrees at the named commits.
The retained receipt identifies the executed local commands and results.
The added final step in `context-package-rendition-pin.yml` checks the patch
digest and site base, applies the overlay, builds with detached source and
roadmap worktrees, and executes the actual-page control, all four Python
suites, UI suite and five standalone gates. The source pin intentionally names
the checked ancestor `6eec8809`; the later source commit storing this evidence
does not silently repin the proposed site. Explicit source-directory variables
prevent the roadmap and programme suites from skipping their real-source cases.
Hosted execution and its checked commit are reported separately in the PR;
the existence of the workflow is not itself a successful run.
Changing an input pin requires a new consumer run, even when manuscript bytes
appear equal.

The existing site owner still needs non-author review of the proposed consumer
change, the applicable language/scientific acceptance, adoption into the site
branch, its own required CI and release workflow, and actual served-page
verification. The CPU-ARC scientific wording correction is a separate,
author-owned follow-up and is not included in this consumer overlay.

This source candidate has `runtime_authorized=false`. Production use, native
admission, reader benefit and execution cost remain unestablished.
