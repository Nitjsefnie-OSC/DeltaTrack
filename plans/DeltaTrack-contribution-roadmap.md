# DeltaTrack: contribution recovery and financial readiness

Living work plan · Updated October 26, 2026 · Maintainer: Will Hea

## Purpose

Track the useful work originating in Matt’s PRs from its current state to a clear outcome: integrated, replaced, deliberately deferred, or declined with a reason. Carry structural improvements forward and work toward trustworthy financial features under ADR 0025.

This is a navigation and handoff document, not an implementation specification. The work packages below are provisional containers. We can split, combine, reorder, replace, or stop them as evidence develops. No fixed PR count or implementation design is promised. Accepted ADRs govern acceptance; this plan records what we currently think will get us there.

## Where we are

- [#796, financial-readiness ADR 0025](https://github.com/civictechdc/DeltaTrack/pull/796) merged at `45d64e9d`. Adoption bookkeeping is completed separately in `f3e80ffe`: Accepted status and both indexes, without changing criteria or authorizing financial displays.
- Matt’s source contributions are [#734, PDF headings](https://github.com/civictechdc/DeltaTrack/pull/734), [#736, financial ledger and views](https://github.com/civictechdc/DeltaTrack/pull/736), and [#739, XML headings](https://github.com/civictechdc/DeltaTrack/pull/739). #734 and #736 remain open; #739 was already closed upstream without a merge when this PDF turn began. Their Git ancestry does not define the replacement architecture.
- The first XML successor has landed. The next PDF slice is deliberately narrower than #734's heading passes: source-supported comma-ended wrapped account names. Broader XML and PDF recovery remains deferred.
- Financial research has advanced: #854 fixed the notebook’s Title I shortfall and same-named account merging; #845 improved selection and measurement. Neither establishes all-figure financial readiness.
- [#856, bounded XML provision headings](https://github.com/civictechdc/DeltaTrack/pull/856) merged as `68946586`, containing `ff5d98f7`. The PDF branch starts from that `develop` commit, not the XML feature branch. Open successors were checked before implementation and again before delivery; none duplicates this slice.
- [#857, source-supported comma-wrapped PDF account names](https://github.com/civictechdc/DeltaTrack/pull/857) is open against `develop`. Initial implementation: `bf148f6a`, with carried typography authored by Matt in `352d0825` and his coauthor credit on the adaptation. Review of `7a511be` identified the sparse-layout width defect addressed below. Maintainer review remains the integration gate.

## Outcomes to track

| ID | Outcome | Current position | Next useful step | PRs / evidence |
|---|---|---|---|---|
| A | Agreed financial acceptance boundaries | Adoption recorded separately; no financial shipping approval | Apply the accepted criteria to future financial proposals | #796; `f3e80ffe` |
| B | Useful XML structure work integrated | Bounded provision-heading successor merged | Recover remaining supported XML shapes independently; source PR closure did not integrate them | Source: #739; successor #856 |
| C | Useful PDF structure work integrated | Focused comma-wrap successor open against current develop | Will reviews #857, then choose the next source-supported scope repair after integration | Source: #734; successor #857 at `bf148f6a` |
| D | Trustworthy individual financial figures | Existing research provides bounded evidence | Implement and validate one complete mixed-figure example; use what it reveals to choose the next slice | Sources: #736, #845, #854; stage 1 not demonstrated |
| E | Trustworthy financial totals | Existing rollup research exposes unresolved accounting and scope issues | After per-figure work clarifies the inputs, choose a bounded aggregation claim and test it independently | ADR stage 2; not ready |
| F | Meaningful cross-version financial changes | Acceptance decision intentionally deferred | After stage 1 ships, settle the paired-change claim and its criteria, then plan implementation | ADR stage 3; not ready |

These are outcomes, not six mandatory PRs. B and C are independently useful. XML-first is the current sequencing preference because its scope appears smaller and it can improve placement diagnostics; PDF correctness must not depend on trusting XML as an infallible oracle. Financial research can proceed alongside structural work where the necessary source placement is reliable. Financial presentation follows the relevant stage’s gate.

## Current working approach

### Structure: recover useful contributions without inheriting the stack

For XML, recover provision headings first, then assess the remaining shapes independently. A header-only `appropriations-small` immediately before a numbered section can label that section and its subsections, without claiming the later sibling sections. `SPENDING REDUCTION ACCOUNT` therefore labels SEC. 420, not SEC. 421. This replaces #739’s carry-until-next-heading rule, rather than tuning toward PDF/XML agreement. Longer administrative blocks may remain shallower than print.

The successor gives recovered ancestors per-version source-occurrence keys through serialization and the sidecar tree; labels alone cannot distinguish repeats. Tests in `tests/test_xml_provision_headings.py` reject heading loss, unrelated sibling inheritance, repeated-name collapse, missing second jump targets, and collisions between separate bill bodies. Each consequential failure was observed under a targeted mutation. The existing matching sentinels remain the owner of correspondence checks, without duplicate matching tests.

The before/after audit against `develop` at `52d52560` covered every committed XML fixture: content-node count/order and all pre-existing non-display fields were identical. Every pairing-stream digest stayed unchanged. Only XML canonical bytes/digests, the parser-revision stamps, generated XML examples and null-body container counts needed refresh. Null-heading and change-body containment counts did not move. The `Receipts collected` regression now distinguishes heading from body semantically rather than pinning a stale absolute offset; its wrong-body-link mutation failed.

Reviewed commit `ff5d98f7` passed lint, formatting, fast, fail-closed browser and every CI slow gate (including external validation). The final runs reported 2,322 fast passes, 30 browser passes and 2,198 slow passes; existing declared skips/xfails remain. The live-network govinfo gate was deliberately excluded, as in CI. Initial failures were artifact/provenance drift, a stale offset assertion and missing CI registration, all corrected and rerun. Details and mutation evidence are in #856. Chromium before/after inspection and a live click confirmed the new Full bill heading target, with SEC. 420 alone beneath it. No additional substantive review is needed absent a named new material failure; proceed to maintainer review/integration.

Retained in #856: Matt’s provision-heading examples and investigation, adapted with coauthor credit; existing committed H.R. 4366 evidence; focused scope and occurrence tests; re-rendered XML examples. Deferred from #739: same-level NATO/FDA and other account-heading chains, headings inside preceding sections, split-title and deep-container display recovery, representative vehicle fixtures and per-kind placement measurement. No original fixture was deleted, and no PDF recovery, financial interpretation, total or view was imported. #521 and #733 remain open because that slice does not finish them. #739's subsequent upstream closure does not dispose of these remaining contributions.

For PDF, retain #734's glyph-size case-pattern reader, gap-aware first-word measurement, heading-width evidence and repeated-standalone-heading veto. Adapt these into the existing account detector rather than importing the heading-pass framework. A join requires a continuation comma, matching known typography, centered adjacent lines on one page, and a next word that could not fit on the preceding line. Unknown or conflicting evidence preserves the previous reading. No account-name exceptions or financial-text hierarchy rules are included.

The width bound is the full body-defined region eligible under the detector's existing minimum centered-heading inset, not the width of observed headings. Review of `7a511be` reproduced a sparse-layout false join: removing an unrelated wide heading let the short candidate define its own available width. A narrower unrelated heading also failed, so merely excluding the candidate was not a safe remedy. The correction keeps the existing inset eligibility criterion and uses its entire allowed region; heading candidates cannot shrink that bound. The short-heading control now covers wide, narrow and absent unrelated headings, consolidating the earlier negative case. Restoring the faulty calculation was observed to fail the narrow and absent cases; the corrected module passes, including the real H.R. 4366 source-span and downstream-reference control.

The correction's ordered anchor-and-breadcrumb audit found no changes on any committed PDF versus the reviewed head. No real recovery result, PDF canonical baseline or containment-count expectation is changed to accommodate this constructed-input fix. All XML pairing digests and source hashes also remain unchanged; only their derived parser-revision stamps are refreshed. Lint, formatting, fast tests, fail-closed browser tests and every CI slow gate were rerun successfully after the correction; the live-network govinfo gate remains excluded as in CI. This fixes the width-evidence defect without reopening the broader heading design or changing the deferred scope. The PR carries the red/green and final-check results; the next action remains maintainer review, not another unbounded heading pass.

The approach changed after a full-corpus audit: matching typography plus fullness alone joined the ambiguous Members’ Representational Allowances / Including Members’ Clerk Hire stack. Requiring continuation punctuation leaves that boundary alone. The narrower repair recovers the demonstrated H.R. 4366 p.10 lines 13–14 as one account at line 13, instead of a fake parent and an ARMY child. Across the committed PDFs, all newly recovered account labels match normalized raw XML headers. That supports label consistency, not an infallible hierarchy oracle.

Semantic controls in `tests/test_pdf_wrapped_accounts.py` protect joins, intentional separate headings, missing/ambiguous evidence and real report source targets. Targeted mutations reject disabled joins, ignored case/fullness/centering/punctuation/standalone evidence, invented geometry, wrong source coordinates and faulty typography reading. The word-gap boundary has its own control in `tests/test_pdf_text.py`. Existing conservation, identity and correspondence gates remain authoritative rather than duplicated.

The canonical audit across accepted PDF pairs preserves full text, print-break maps and bill identities byte-for-byte. Segmentation changes report paths and some pairing: H.R. 4366 v3→v4's Army account becomes modified rather than falsely relocated. The PDF baseline and affected containment counts reflect inspected changes; null-span counts do not move. XML pairing digests remain identical and only their derived parser revision is restamped. The existing PDF revocation-population pin, extraction/geometry goldens and committed rendered examples need no refresh. Chromium source/report inspection confirms the recovered account's navigation target starts at printed line 13 and retains line 14.

The focused PDF delivery passes lint, formatting, fast tests, fail-closed Chromium tests and every CI slow gate, including external validation. The live-network govinfo gate is deliberately excluded as in CI. Earlier failures exposed artifact/provenance drift, a stale fragment-label test, missing CI registration and an overly broad join rule; each was investigated rather than accepted as a baseline refresh. The final source passed the rerun. A background extractor-cache mismatch was diagnosed against an uncached read, and only the new worktree's generated cache was cleared before the clean audit. Alternating uncached timing on the largest committed print preserves the optimized extraction path, with no new PDFium calls. Detailed evidence belongs in the successor PR, not in another repository research artifact.

Deferred from #734: non-comma and cross-page wraps, stacked-heading resegmentation, sentence/quote filters, mid-title department recovery, broader agency-scope rules and placement scoring. In particular, NATO still leaks into later housing paths, and unrecovered fragments can still become parents. Recovering a name is not certification of its whole ancestry. The title-case agency-promotion rule that checks following dollar text is explicitly separate and unadopted under ADR 0018. No financial interpretation, totals, views or unrelated XML changes travel with this slice.

Necessary tests and refreshed artifacts travel with the behavior they protect. Extract shared validation machinery only when a real shared need emerges.

### Financial work: learn through complete examples

The first proposed slice is a real provision containing both an appropriation and a rescission. It should expose whether each figure can retain its own meaning, fiscal year, account occurrence, source span, and uncertainty. That is an experiment in the representation and interpretation path, not advance approval of a particular schema or classifier.

Choose subsequent slices from the failures and evidence gaps that matter most. Reuse current research and Matt’s source-inspection ideas where useful; avoid maintaining a copied legacy classifier as a second competing implementation.

Build independent-source checks alongside the interpretation work. A successful example is progress, not stage 1 readiness. Before stage 1 ships, the ADR’s full validation and sign-off requirements still apply, including representative bill kinds and an untouched holdout year. Once holdout results inform rule changes, record that exposure rather than continuing to call them unseen evidence.

Totals and paired comparisons remain separately tracked outcomes. Correctly reading individual figures does not settle their accounting basis, additivity, or cross-version correspondence. Do not design those features in detail before the necessary evidence exists.

## Questions that could change the route

| Question | How we will resolve it | Consequence for the plan |
|---|---|---|
| Which remaining XML heading shapes have defensible scope? | Provision-heading adjacency is now controlled; inspect NATO/FDA chains and explicit nested containers next, preserving occurrence identity | Keep the provision slice independent; recover other shapes only with their own evidence |
| Which PDF heading rules are supported by permitted source signals? | Inspect the rule’s evidence and test a counterexample or mutation that would invalidate it | Carry, separate, or drop individual rules |
| Does the per-figure approach represent mixed effects and years without losing occurrences? | A complete real example plus semantic negative controls | Revise the representation before broadening it |
| Which official sources support which financial claims? | Establish usable evidence for the next bounded claim; record missing coverage explicitly | Change validation work or leave a claim unshipped |
| Can totals reconcile on the same scope and accounting basis? | Independent totals and controls for double counting, year mixing, and gross/net differences | Narrow or revise the aggregation claim |

This is the current shortlist, not a requirement to open another study for every row. Add a question only if its answer could change the next action or a consequential conclusion.

## Contribution disposition

| Origin | Intended home | Closure condition |
|---|---|---|
| #739 XML headings and useful fixtures | B: merged #856 carries adapted provision examples/investigation/tests with Matt’s coauthor credit; other heading shapes and vehicle fixtures deferred | Source PR already closed upstream; recover or explicitly dispose of remaining contributions independently |
| #734 typography, heading repairs, examples, placement scorer | C: #857 retains typography, width and standalone evidence; original authorship in `352d0825`, adapted work coauthored in `bf148f6a`; framework, scope rules and scorer deferred | Will reviews/integrates #857; remaining contributions receive their own evidence and disposition, not automatic closure |
| #736 source spans, inspectability, coverage and interface investigation | D–F where useful; interface ideas remain candidates until their claims can ship | Retained material is preserved, deferred work has linked homes, and obsolete integration is explicitly superseded |

Preserve original commit authorship where changes carry directly. For substantially adapted contributions, record provenance and appropriate coauthor credit. Credit examples, tests, and investigation as well as production code. Before closing an original PR, link the actual successors or deferred tracking items and explain its disposition. Do not discard valuable work merely to close the stack; do not keep the stack open indefinitely after every contribution has a clear home.

## How we work across PRs and turns

At the start of a turn, read this plan and inspect the current state of the relevant PRs and target branch. Continue from the recorded position; do not redo completed review by default. Select the smallest useful next action, which may be implementation, a focused experiment, a decision, or procedural closure.

At the end of a substantive turn, update this same document with:

1. What changed or was learned, and how it changes the route.
2. The relevant issue/PR, reviewed commit, and decisive evidence.
3. What remains uncertain or blocked.
4. The next concrete action and who owns it.

Keep the summary current rather than accumulating a transcript. Create implementation issues and PRs when their scope is concrete enough to execute; do not create a speculative ticket tree now. GitHub holds implementation details and review evidence; this plan connects them. No GitHub tracker changes are implied merely by writing this plan.

### Review and stop rule

Before adding a regression test, state the behavior it protects and a concrete failure that must turn it red. Prefer semantic tests and decisive negative controls; remove demonstrated redundant coverage. Run the checks required by the repository for the actual change.

A new substantive review pass must name a plausible, currently untested failure that could materially change the result. Once the consequential invariants have decisive controls and no known decision-changing gap remains, integrate or close the slice. Do not expand review merely because more examples or questions are imaginable. If evidence defeats an approach, record the finding and change course instead of tuning toward the desired result.

## What “done” means

**Contribution recovery is complete** when each useful part of #734, #736, and #739 is integrated or has an explicit, preserved disposition; superseded PRs are closed with credit and links. This can finish before every financial feature ships.

**A financial stage is complete** only when its accepted criteria pass, required sign-off is recorded, and the corresponding export/report integration has landed. Research progress or a merged ADR is not stage completion.

**The overall roadmap is complete** when every tracked outcome is delivered or explicitly removed/deferred by Will. Record delivery, deferral, and rejection distinctly; a deferred financial feature must not be described as shipped. If the goal changes, update the outcomes rather than forcing the old plan to completion.

## Next turn

**Owner: Will reviews [#857](https://github.com/civictechdc/DeltaTrack/pull/857); implementing agent follows up.** Confirm hosted CI and preserve Matt's author/coauthor credit through integration. No further substantive review pass is justified without a named, presently untested failure that could materially change this bounded result. After integration, use a fresh session for a bounded agency-scope repair, starting with the NATO carry-over exposed by H.R. 4366. Require source-based negative controls and do not import the financial-text promotion rule. Alternatively resume the remaining supported XML shapes, explicit container nesting and NATO/FDA chains, retaining occurrence identity. Keep vehicle-fixture work separate from parser correctness and financial readiness. Do not merge or close #734, #739 or #736 as an inferred cleanup step.

This is the single authoritative repository copy, committed in `plans/` despite that directory's general ignore rule. The prior ignored primary-checkout copy has been moved here, not duplicated. Retire the plan only when its remaining outcomes are delivered or explicitly disposed of.

## References

- Repository: https://github.com/civictechdc/DeltaTrack
- Financial tracking epic: https://github.com/civictechdc/DeltaTrack/issues/147
- Readiness ADR: https://github.com/civictechdc/DeltaTrack/pull/796
- Matt’s contributions: https://github.com/civictechdc/DeltaTrack/pull/734 · https://github.com/civictechdc/DeltaTrack/pull/736 · https://github.com/civictechdc/DeltaTrack/pull/739
- Current research improvements: https://github.com/civictechdc/DeltaTrack/pull/845 · https://github.com/civictechdc/DeltaTrack/pull/854
