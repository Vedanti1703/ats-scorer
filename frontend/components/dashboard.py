from typing import Any, Dict

import streamlit as st

from frontend.components.score_display import display_overall_score, display_score_breakdown
from frontend.components.strengths_issues import display_strengths, display_critical_issues
from frontend.components.skill_validation import display_skill_validation
from frontend.components.jd_comparison import display_jd_comparison
from frontend.components.detailed_feedback import display_detailed_feedback
from frontend.components.action_items import display_action_items
from frontend.components.recommendations import display_recommendations


def display_results_dashboard(analysis: Dict[str, Any]) -> None:
    st.markdown("---")

    tab_overview, tab_keywords, tab_feedback, tab_actions = st.tabs([
        "Overview",
        "Keywords & JD Match",
        "Detailed Feedback",
        "Action Items",
    ])

    with tab_overview:
        display_overall_score(analysis)
        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
        display_score_breakdown(analysis)
        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
        col_s, col_i = st.columns(2)
        with col_s:
            display_strengths(analysis.get("strengths") or [])
        with col_i:
            display_critical_issues(analysis)

    with tab_keywords:
        jd_comparison = analysis.get("jd_comparison") or analysis.get("jd_match_analysis")
        if jd_comparison:
            display_jd_comparison(jd_comparison)
        else:
            st.info(
                "No Job Description was provided for this run. "
                "Select 'Paste JD Text' or 'Upload .txt File' in the Analyzer to see targeted keyword match and skills gap."
            )
            comp_scores = analysis.get("component_scores") or {}
            kw_score = comp_scores.get("keywords", 0)
            st.metric("General Keyword & Skill Score", f"{kw_score:.0f} / 25 pts")

    with tab_feedback:
        display_detailed_feedback(analysis)
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        display_skill_validation(analysis)

    with tab_actions:
        display_action_items(analysis)
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        display_recommendations(analysis)
