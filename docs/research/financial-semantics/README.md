# DeltaTrack Notebooks

Financial classifier and analysis tools for DeltaTrack bill data.

## Files

| File | Purpose |
|---|---|
| `classify_bill.py` | Rule-based classifier — imported by all notebooks and scripts |
| `01_eda.ipynb` | Exploratory analysis: BBI dataset, XML node structure, PDF pipeline |
| `02_financial_report.ipynb` | Financial summary report for a single bill |
| `03_classifier_stress_test.ipynb` | Interactive classifier validation across multiple bills |
| `stress_test_analysis.py` | Script: parses all 7 reference bills, reports unknowns and FP risks |
| `stress_test_detail.py` | Script: shows full text of unknown nodes per bill type |
| `classifier_notes.md` | Design rationale: pattern decisions and intentionally-unknown categories |
| `committee_agreement.py` | Scores the figure typed as each account's appropriation against the committee report's figure for that account (ADR 0025, proposed, #796) |
| `appropriation_resolver.py` | Picks the one figure an appropriations paragraph appropriates, the way the paragraph is drafted, or abstains |

## Does the typed appropriation equal the committee report's?

ADR 0009's recall check asks whether a committee report's figure for an account appears anywhere
under its agency. ADR 0025 (proposed, #796) asks more: that the figure we **type** as the account's
appropriation **equals** the report's. `committee_agreement.py` measures that over every account
the committee-report answer keys (`tests/data/validation_*.json`) map to a bill node. Committed
fixtures only, so it needs no download:

```bash
uv run python docs/research/financial-semantics/committee_agreement.py                 # both resolvers, all keys
uv run python docs/research/financial-semantics/committee_agreement.py --split held-out
uv run python docs/research/financial-semantics/committee_agreement.py --resolver structured --details wrong_figure
```

On the 1,163 mapped accounts (of 1,267), reproduced by the first command:

| | `classify_bill` (first figure of the primary clause) | `appropriation_resolver` |
|---|---|---|
| Agrees with the report | 920 (79.1%) | 955 (82.1%) |
| Typed a different figure while the report's is in the text | 37 | 2 |
| Typed nothing while the report's figure is in the text | 21 | 21 |
| Typed a figure the report does not state (no single figure in the text matches) | 46 | 46 |
| Answer key finer than the bill node (several report lines, one paragraph) | 122 | 122 |

The resolver changes which figure is chosen, never which paragraphs count as appropriations, so it
reads the paragraph as drafted: an "in all" total; nothing after the first proviso; an explicit
"is hereby appropriated"; otherwise the figure that closes the purpose clause, skipping allowances
inside it and loan levels; and abstaining when none fits. `tests/test_appropriation_resolver.py`
pins each rule and fails on any wrong figure beyond the two listed there (gross versus net for a
fee-funded account; one office of an itemised paragraph).

**How far to trust the numbers.** The rules were written from six answer keys (`DEV` in the
script) and frozen at d394669 before the other eight (`HELD_OUT`) were scored. That frozen version
typed 0 wrong figures on the held-out accounts (the baseline 3) but agreed on 389 against the
baseline's 401, because it abstained more. Reading those abstentions produced the current rules,
which agree on 404, still with 0 wrong figures, but the held-out set has now been seen, so that is
no longer an unbiased estimate. A fresh answer key (`scripts/build_validation.py` on another
fiscal year or the House-reported bills) is the next honest test.

**Open questions this leaves.**

- The 46 figures neither resolver can confirm are not typing errors: the report's figure is not
  one figure in the account's text (a report total built from parts or transfers, one report typo:
  NASA's $3,044,440,000 against the bill's $3,044,400,000). Each needs hand-tracing, which is the
  ADR 0025 process, not a rule.
- `classify_bill` does not type "In addition to amounts made available elsewhere in this Act,
  $X is hereby appropriated" as an appropriation (`APPROP_ALT` matches only "there is
  appropriated"), so six Defense general provisions are missed before the resolver sees them.
  That is a classification rule, which #736 moves into the package, so it is left there.
- Gross versus net: a fee-funded account states both, and reports are inconsistent about which
  they carry. The figure's type, not the resolver, has to say which one a number is.

## Running the scripts

From the `DeltaTrack/` directory:

```bash
uv run python docs/research/financial-semantics/stress_test_analysis.py
uv run python docs/research/financial-semantics/stress_test_detail.py approp   # or: reconciliation, authorization, all
```

Scripts require bill XML files downloaded to `bills/` (gitignored). Download with:

```bash
uv run python tools/fetch_bills.py download 118 hr 4366
```

## Dependencies

The scripts use only stdlib and the project's core dependencies. The Jupyter notebooks use `pandas`, which is in the `dev` dependency group. Running `uv sync` installs everything — no extra steps needed.
