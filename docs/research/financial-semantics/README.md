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
| `rollup_agreement.py` | Adds the typed figures up per agency and checks them against the committee report's "Total, <agency>" lines |

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

**What the 82% is made of.** It is not a quality score for the resolver. Of the 1,163 accounts,
122 are report lines finer than the bill's paragraph (several offices of one "including: ..."
paragraph) and 63 have no single figure in the account's text equal to the report's, so no
method that types one figure per account, rules or a model, can agree on those 185. Where one
figure can, the resolver agrees on 955 of 978 (97.6%). Typing **every** figure (naming the
itemised lines, summing an account's appropriating figures) would raise the ceiling to at most
1,066 (91.7%): 101 of the 122 are a figure printed in the paragraph, and 10 of the 63 are a sum
of two to four figures before its first proviso. The rest are report-versus-bill differences
that only hand-tracing settles.

## Do typed figures add up to the report's agency totals?

The account figures exist to be rolled up: account, agency, department. `rollup_agreement.py`
checks the roll-up against each "Total, <agency>" line of the thirteen Senate reports'
comparative statements (in thousands):

```bash
uv run python docs/research/financial-semantics/rollup_agreement.py
uv run python docs/research/financial-semantics/rollup_agreement.py --resolver structured --details mismatch
```

A report total is attributed to the rows above it by the report's own arithmetic: walking back,
a subtotal contributes its value and is jumped over, and the span is the first run that adds up
to the total. A total no run reproduces is not scored (`report_inconsistent`; the parser's
section context is not reliable enough to attribute it otherwise). The total's name must then
be exactly one bill heading. A report total is net of fee offsets and rescissions, which are
negative rows; a typed figure is gross, so both are compared.

Of the 406 totals, 273 are attributed; 190 of those name a bill heading. Reproduced by the first
command:

| | `classify_bill` | `appropriation_resolver` |
|---|---|---|
| Equals the report's net total | 109 | 113 |
| Equals it with the report's negative rows added back (gross) | 7 | 8 |
| Equals it once accounts' second figures ("together with $X from the ... Trust Fund") are added | 2 | 2 |
| Complete, and none of these | 41 | 31 |
| Incomplete (an appropriating account abstained, or none was typed) | 31 | 36 |

So 121 of the resolver's 154 complete roll-ups reproduce the report's agency total.
`tests/test_rollup_agreement.py` pins the attribution and these counts.

**Why the other 31 do not, hand-traced:**

- **Accounts that appropriate more than one figure.** "...section 436 of the Social Security
  Act, $345,000,000 and, for carrying out ... section 437, $72,515,000" is one account whose
  report total ($417,515,000) is both; "$537,144,000, together with $64,828,000 from the amounts
  available under section 241" is another. A resolver that types one figure per account cannot
  reproduce these, which is the roll-up's evidence for ADR 0025's "every figure gets its own
  type".
- **Money `classify_bill` leaves untyped.** Ten of the 31 have a paragraph under the heading
  that carries money and is classified `unknown`, so the sum undercounts by construction.
- **An obligation limitation typed as an appropriation.** Federal Transit Administration's sum is
  $14.28 billion over the report's: it includes a Highway Trust Fund limitation on obligations,
  which the report keeps out of budget authority. Only the roll-up catches this; no single
  account's figure disagreed with a report line.
- **The report groups accounts the bill heads differently.** Agriculture's "Total, Executive
  Operations" sums thirteen offices; the bill's "Executive Operations" heading carries three.
