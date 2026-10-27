"""Source-bounded provision headings, adapted from Matt Zamora's #739 cases."""

import xml.etree.ElementTree as ET

import pytest

from deltatrack.bill_tree import NO_DIVISION, BillTree, normalize_bill, walk_title
from deltatrack.formatters.text_serializer import build_xml_full_text
from tests.corpus_paths import fixture_path


def _preorder(nodes):
    for node in nodes:
        yield node
        yield from _preorder(node["children"])


def test_repeated_provision_headings_keep_their_scope_and_own_jump_targets():
    title = ET.fromstring(
        "<title><enum>I</enum><header>GENERAL PROVISIONS</header>"
        "<appropriations-small><header>Administrative provisions</header></appropriations-small>"
        '<section id="s1"><enum>1.</enum><text>First provision.</text>'
        '<subsection id="s1a"><enum>(a)</enum><header>Application</header><text>First details.</text></subsection>'
        "</section>"
        "<appropriations-small><header>Administrative provisions</header></appropriations-small>"
        '<section id="s3"><enum>3.</enum><text>Second provision.</text></section>'
        '<section id="s2"><enum>2.</enum><text>Unrelated provision.</text></section>'
        '<section id="s4"><enum>4.</enum><text>Another unrelated provision.</text></section>'
        "</title>"
    )
    nodes = walk_title(title, "TITLE I—GENERAL PROVISIONS", NO_DIVISION)
    by_id = {n.element_id: n for n in nodes}
    root = ("TITLE I—GENERAL PROVISIONS",)
    heading = "Administrative provisions"
    assert by_id["s1"].display_path == (*root, heading, "Sec. 1")
    assert by_id["s1a"].display_path == (*root, heading, "Sec. 1", "(a) Application")
    assert by_id["s2"].display_path == (*root, "Sec. 2")
    assert by_id["s3"].display_path == (*root, heading, "Sec. 3")
    assert by_id["s4"].display_path == (*root, "Sec. 4")
    bill = BillTree(118, "hr", 1, "test", nodes)
    text, _, trees, node_ids = build_xml_full_text(bill, bill)
    headings = [n for n in _preorder(trees["v1"]) if n["label"] == heading]
    assert len(headings) == 2
    assert [n["level"] for n in headings] == ["heading", "heading"]
    assert [[c["label"] for c in n["children"]] for n in headings] == [["Sec. 1"], ["Sec. 3"]]
    spans = [n["heading_span"] for n in headings]
    assert spans[0]["start"] < spans[1]["start"]
    for node in headings:
        span = node["heading_span"]
        assert text["v1"][span["start"] : span["end"]] == heading
        full_span = node["full_text_span"]
        assert text["v1"][full_span["start"] : full_span["end"]] == heading
    # The second heading must own the second provision's node, not an alias of the first.
    second_ordinal = nodes.index(by_id["s3"])
    assert headings[1]["children"][0]["id"] == node_ids["v1"][second_ordinal]


@pytest.mark.slow
def test_spending_reduction_heading_does_not_cover_the_va_restriction():
    bill = normalize_bill(fixture_path("118-hr-4366", "2_engrossed-in-house.xml"))
    by_id = {n.element_id: n for n in bill.nodes}
    spending = by_id["HEB273574E6284EA98BE667E703C80E56"]
    restriction = by_id["H4C9E55DDC06B467DB6A7A3004265FB98"]
    assert spending.display_path == ("TITLE IV", "GENERAL PROVISIONS", "SPENDING REDUCTION ACCOUNT", "Sec. 420")
    assert restriction.display_path == ("TITLE IV", "GENERAL PROVISIONS", "Sec. 421")
    assert "Veterans Health Directive 1315" in restriction.body_text
    text, _, trees, _ = build_xml_full_text(bill, bill)
    [heading] = [n for n in _preorder(trees["v1"]) if n["label"] == "SPENDING REDUCTION ACCOUNT"]
    assert [c["label"] for c in heading["children"]] == ["Sec. 420"]
    span = heading["heading_span"]
    assert text["v1"][span["start"] : span["end"]] == "SPENDING REDUCTION ACCOUNT"


def test_repeated_headings_in_separate_bill_bodies_do_not_share_a_target(tmp_path):
    """Bodies may reuse both source ids and local ordinals; neither is a document id."""
    body = (
        "<legis-body><title><enum>I</enum><header>Provisions</header>"
        '<appropriations-small id="h"><header>Administrative provisions</header></appropriations-small>'
        '<section id="s"><enum>1.</enum><text>Provision.</text></section>'
        "</title></legis-body>"
    )
    path = tmp_path / "bill.xml"
    path.write_text(f"<bill>{body}{body}</bill>")
    bill = normalize_bill(path)
    text, _, trees, _ = build_xml_full_text(bill, bill)
    headings = [n for n in _preorder(trees["v1"]) if n["label"] == "Administrative provisions"]
    assert len(headings) == 2
    spans = [n["heading_span"] for n in headings]
    assert spans[0]["start"] < spans[1]["start"]
    for span in spans:
        assert text["v1"][span["start"] : span["end"]] == "Administrative provisions"
