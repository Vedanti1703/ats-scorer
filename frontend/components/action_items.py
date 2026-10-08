import textwrap
from typing import Any, Dict, List, Tuple

import streamlit as st

from frontend.components._helpers import get_svg_icon


SEVERITY_RANK = {"critical": 0, "high": 1, "medium": 2, "low": 3}


def _collect_action_items(analysis: Dict[str, Any]) -> List[Tuple[str, str, str]]:
    items: List[Tuple[str, str, str]] = []

    for issue in analysis.get("detailed_feedback") or []:
        level = (issue.get("severity_level") or "low").lower()
        title = issue.get("issue_title", "")
        for action in issue.get("action_items") or []:
            items.append((level, title, action))

    if not items:
        for suggestion in analysis.get("suggestions") or []:
            items.append(("medium", "General", suggestion))

    items.sort(key=lambda row: SEVERITY_RANK.get(row[0], 99))
    return items


def display_action_items(analysis: Dict[str, Any]) -> None:
    items = _collect_action_items(analysis)
    if not items:
        return

    st.markdown("### Action Checklist")
    st.caption("Concrete steps to improve your resume score, prioritized by impact.")

    check_icon = get_svg_icon("check-circle", size=18, color="#4F46E5")

    for i, (level, source, action) in enumerate(items):
        if i == 0:
            badge_text = "DO THIS FIRST"
            badge_style = "background:#FEE2E2; color:#991B1B;"
        elif level in ("critical", "high"):
            badge_text = "HIGH IMPACT"
            badge_style = "background:#FEE2E2; color:#991B1B;"
        elif level == "medium":
            badge_text = "MEDIUM IMPACT"
            badge_style = "background:#FEF3C7; color:#92400E;"
        else:
            badge_text = "LOW IMPACT"
            badge_style = "background:#E0F2FE; color:#075985;"

        card_html = textwrap.dedent(f"""
<div class="action-checklist-card">
<div style="margin-top:2px; flex-shrink:0;">{check_icon}</div>
<div style="flex:1;">
<div style="display:flex; align-items:center; gap:8px; margin-bottom:4px;">
<span style="{badge_style} font-size:10px; font-weight:800; text-transform:uppercase; letter-spacing:0.06em; padding:2px 8px; border-radius:9999px;">
{badge_text}
</span>
<span style="font-size:13px; font-weight:600; color:#64748B;">{source}</span>
</div>
<div style="font-size:14.5px; color:#1E293B; line-height:1.45;">{action}</div>
</div>
</div>
""").strip()
        st.markdown(card_html, unsafe_allow_html=True)
