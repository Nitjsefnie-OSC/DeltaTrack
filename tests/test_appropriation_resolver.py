"""The appropriation resolver: which figure an appropriations paragraph appropriates.

`docs/research/financial-semantics/appropriation_resolver.py` picks one figure per account,
or abstains; `committee_agreement.py` beside it scores that figure against the committee
reports. The unit tests pin each drafting rule on a constructed paragraph, so removing a rule
turns its test red. The slow gate holds the claim the research makes for ADR 0025 (proposed,
#796): where the report's figure is in the account's text, the resolver never types a
different figure, except for the cases listed with their reason.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "docs" / "research" / "financial-semantics"))

import committee_agreement  # noqa: E402
from appropriation_resolver import resolve  # noqa: E402


def test_the_figure_closing_the_purpose_clause_beats_an_allowance_inside_it():
    """The baseline took the first figure; here that is an allowance followed by "for"."""
    text = (
        "For necessary expenses of the Commission, including up to $32,500,000 for payments to "
        "State and local enforcement agencies, $488,221,000, of which $2,788,000 shall be for "
        "the Office of the Inspector General."
    )
    assert resolve(text) == 488_221_000


def test_an_in_all_total_is_the_account():
    """Each itemised line closes like an appropriation; only the "in all" rule finds the total."""
    text = (
        "For expense allowances of the Secretary of the Senate, $7,110; Secretary for the Majority "
        "of the Senate, $7,110; Secretary for the Minority of the Senate, $7,110; in all, $28,440."
    )
    assert resolve(text) == 28_440


def test_no_figure_after_the_first_proviso_is_the_appropriation():
    """The real figure follows a semicolon; a proviso carve-out follows a comma and "shall"."""
    text = (
        "For necessary expenses to carry out the Act, except sections 17 and 21; $31,775,179,000 "
        "to remain available through September 30, 2026: Provided, That of the total amount "
        "available, $5,000,000 shall remain available until expended."
    )
    assert resolve(text) == 31_775_179_000
    assert resolve("For grants to States: Provided, That of the total, $5,000,000 shall remain available.") is None


def test_a_loan_level_is_skipped_for_the_cost_appropriation():
    text = (
        "For the principal amount of direct loans, as authorized by section 379H of the Act, "
        "$8,504,000. For the cost of loans and grants, $3,713,000 under the same terms."
    )
    assert resolve(text) == 3_713_000


def test_an_explicit_appropriating_verb_names_the_figure():
    assert resolve("There is hereby appropriated to the Secretary $1,116,889,000: Provided, That no") == 1_116_889_000


def test_a_ceiling_straight_after_the_purposes_is_the_appropriation():
    text = "For carrying out title IV of Public Law 95-372, not to exceed $349,000, to be derived from receipts."
    assert resolve(text) == 349_000
    # Anywhere else a ceiling is a limit inside the purposes, not the appropriation.
    limited = "For expenses, of which not to exceed $25,000 for official reception, $10,000,000."
    assert resolve(limited) == 10_000_000


def test_it_abstains_rather_than_guess():
    assert resolve("For necessary expenses, such sums as may be necessary.") is None
    assert resolve("None of the funds made available may be used for $5,000,000 of travel.") is None


# The two typing disagreements left where the report's figure is in the text. Neither is a
# figure picked from the wrong place: each is a question the figure's type has to answer.
KNOWN_WRONG_FIGURES = {
    # Gross versus net: the bill appropriates $10,020,729,000 and estimates the general-fund
    # cost after fees at $7,400,729,000; this report carries the net figure, the USPTO's the
    # gross, so the resolver returns gross (see the resolver's docstring).
    (
        "homeland_security",
        (
            "security, enforcement, and investigations",
            "transportation security administration",
            "operations and support",
        ),
    ),  # noqa: E501
    # The report lists one office of an itemised paragraph ("...Office of the Whistleblower
    # Ombudsman, $750,000; ...") as an account; the paragraph appropriates its total.
    ("leg_branch", ("legislative branch", "house of representatives", "salaries, officers and employees")),
}


@pytest.mark.slow
def test_no_wrong_figure_where_the_report_figure_is_in_the_text():
    """ADR 0025's zero tolerance, on the committed committee-report answer keys.

    A `wrong_figure` is a figure typed as the account's appropriation while the report's own
    figure for that account is in the text: an error a reader would add up. Fails on any new
    one, and on a listed one that no longer occurs, so the list cannot go stale.
    """
    results, _ = committee_agreement.measure(resolve)
    wrong = {(r.jurisdiction, r.path) for r in results if r.outcome == "wrong_figure"}
    assert wrong == KNOWN_WRONG_FIGURES, (
        f"new: {sorted(wrong - KNOWN_WRONG_FIGURES)}; no longer wrong: {sorted(KNOWN_WRONG_FIGURES - wrong)}"
    )
    assert sum(r.outcome == "agree" for r in results) >= 955, "fewer accounts agree with their report than measured"
