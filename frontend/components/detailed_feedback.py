import textwrap
from typing import Any, Dict, List

import streamlit as st

from frontend.components._helpers import get_svg_icon


SEVERITY_ORDER = ["critical", "high", "medium", "low"]


def _group_by_severity(issues: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    grouped: Dict[str, List[Dict[str, Any]]] = {level: [] for level in SEVERITY_ORDER}
    for issue in issues:
        level = (issue.get("severity_level") or "low").lower()
        grouped.setdefault(level, []).append(issue)
    return grouped


def _render_issue(issue: Dict[str, Any]) -> None:
    level = (issue.get("severity_level") or "low").lower()
    title = issue.get("issue_title", "Untitled issue")
    impact = issue.get("ats_impact", "")
    explanation = issue.get("explanation", "")
    where = issue.get("where_it_appears", "")
    how_to_fix = issue.get("how_to_fix", "")
    action_items = issue.get("action_items") or []
    example = issue.get("example_improvement", "")

    if level in ("critical", "high"):
        stripe_class = "stripe-critical"
        badge_style = "background:#FEE2E2; color:#991B1B;"
        icon = get_svg_icon("alert-triangle", size=16, color="#EF4444")
    elif level == "medium":
        stripe_class = "stripe-medium"
        badge_style = "background:#FEF3C7; color:#92400E;"
        icon = get_svg_icon("alert-triangle", size=16, color="#F59E0B")
    else:
        stripe_class = "stripe-low"
        badge_style = "background:#E0F2FE; color:#075985;"
        icon = get_svg_icon("check-circle", size=16, color="#0EA5E9")

    card_html = textwrap.dedent(f"""
<div class="striped-card {stripe_class}">
<div style="display:flex; align-items:center; justify-content:space-between; gap:12px;">
<div style="display:flex; align-items:center; gap:10px;">
{icon}
<div>
<div style="font-size:15px; font-weight:700; color:#0F172A;">{title}</div>
<div style="font-size:13.5px; color:#64748B;">{impact}</div>
</div>
</div>
<span style="{badge_style} font-size:11px; font-weight:700; text-transform:uppercase; letter-spacing:0.06em; padding:3px 10px; border-radius:9999px;">
{level.upper()}
</span>
</div>
</div>
""").strip()
    st.markdown(card_html, unsafe_allow_html=True)

    with st.expander(f"View Fix Guidance: {title}", expanded=False):
        if explanation:
            st.markdown(f"**Explanation:** {explanation}")
        if where:
            st.markdown(f"**Location in Resume:** `{where}`")
        if how_to_fix:
            st.markdown(f"**How to Fix:** {how_to_fix}")
        if action_items:
            st.markdown("**Actionable Steps:**")
            for item in action_items:
                st.markdown(f"- {item}")
        if example:
            st.markdown("**Example Improvement:**")
            st.code(example, language="text")


def display_detailed_feedback(analysis: Dict[str, Any]) -> None:
    issues = analysis.get("detailed_feedback") or []
    if not issues:
        return

    st.markdown("### Detailed Diagnostic Feedback")
    st.caption(f"{len(issues)} issue(s) detected across your resume.")

    grouped = _group_by_severity(issues)
    for level in SEVERITY_ORDER:
        items = grouped.get(level, [])
        if not items:
            continue
        st.markdown(f"#### {level.title()} Priority ({len(items)})")
        for issue in items:
            _render_issue(issue)
