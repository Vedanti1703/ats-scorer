from typing import Any, Dict

import streamlit as st

from frontend.components._helpers import get_svg_icon


def display_recommendations(analysis: Dict[str, Any]) -> None:
    suggestions = analysis.get("suggestions") or []
    if not suggestions:
        return

    st.markdown("### Strategic Suggestions")
    st.caption("AI-generated editorial and positioning advice.")

    sparkles = get_svg_icon("sparkles", size=16, color="#4F46E5")

    for suggestion in suggestions:
        card_html = f"""
        <div class="saas-card" style="padding: 1rem 1.25rem; margin-bottom: 0.65rem;">
            <div style="display:flex; align-items:flex-start; gap:10px;">
                <div style="margin-top:2px;">{sparkles}</div>
                <div style="font-size:0.9rem; color:#1E293B; line-height:1.5;">{suggestion}</div>
            </div>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)
