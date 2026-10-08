import textwrap
from typing import Any, Dict, List
import streamlit as st

from frontend.components._helpers import get_svg_icon


def display_strengths(strengths: List[str]) -> None:
    st.markdown("### Strengths")
    if not strengths:
        st.info("Keep improving your resume to unlock strengths!")
        return

    icon_check = get_svg_icon("check-circle", size=16, color="#16A34A")
    for item in strengths:
        card_html = textwrap.dedent(f"""
<div class="striped-card stripe-success">
<div style="display:flex; align-items:flex-start; gap:10px;">
<div style="margin-top:2px; flex-shrink:0;">{icon_check}</div>
<div style="font-size:14.5px; color:#1E293B; font-weight:500;">{item}</div>
</div>
</div>
""").strip()
        st.markdown(card_html, unsafe_allow_html=True)


def display_critical_issues(analysis: Dict[str, Any]) -> None:
    critical = analysis.get("critical_issues") or []
    summary = analysis.get("issues_summary") or []

    if not critical and not summary:
        icon_check = get_svg_icon("check-circle", size=20, color="#16A34A")
        st.markdown(textwrap.dedent(f"""
<div style="background:#DCFCE7; border:1px solid #BBF7D0; border-radius:12px; padding:18px 22px; display:flex; align-items:center; gap:12px;">
{icon_check}
<div>
<strong style="color:#166534; font-size:15px;">Zero Critical Blockers Found</strong>
<div style="color:#15803D; font-size:13.5px; margin-top:2px;">Your resume has no urgent errors that would cause automatic rejection.</div>
</div>
</div>
""").strip(), unsafe_allow_html=True)
        return

    st.markdown("### Critical Issues")
    icon_alert = get_svg_icon("alert-triangle", size=16, color="#EF4444")
    for item in critical:
        card_html = textwrap.dedent(f"""
<div class="striped-card stripe-critical">
<div style="display:flex; align-items:flex-start; gap:10px;">
<div style="margin-top:2px; flex-shrink:0;">{icon_alert}</div>
<div style="font-size:14.5px; color:#0F172A; font-weight:500;">{item}</div>
</div>
</div>
""").strip()
        st.markdown(card_html, unsafe_allow_html=True)

    extra = [s for s in summary if s not in critical]
    if extra:
        with st.expander("Additional Flagged Items", expanded=False):
            for item in extra:
                st.markdown(f"- {item}")
