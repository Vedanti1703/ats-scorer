import textwrap
from typing import Any, Dict, Optional

import streamlit as st

from frontend.components._helpers import get_svg_icon


def display_jd_comparison(jd_comparison: Optional[Dict[str, Any]]) -> None:
    if not jd_comparison:
        return

    match_pct = float(jd_comparison.get("match_percentage", 0))
    semantic = float(jd_comparison.get("semantic_similarity", 0))
    matched = jd_comparison.get("matched_keywords", []) or []
    missing = jd_comparison.get("missing_keywords", []) or []
    gap = jd_comparison.get("skills_gap", []) or []

    # Top metrics in clean cards
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Keyword Match Rate", f"{match_pct:.0f}%")
        st.progress(min(max(match_pct / 100.0, 0.0), 1.0))
    with col2:
        st.metric("Semantic Similarity", f"{semantic * 100:.0f}%")
        st.progress(min(max(semantic, 0.0), 1.0))

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    # Matched vs Missing Chips with exact specs
    col_matched, col_missing = st.columns(2)

    with col_matched:
        icon_check = get_svg_icon("check", size=14, color="#166534")
        st.markdown(f"#### Matched Keywords ({len(matched)})")
        if matched:
            chips_parts = []
            for kw in matched[:25]:
                chips_parts.append(
                    f'<span style="display:inline-flex; align-items:center; gap:6px; background:#DCFCE7; color:#166534; border:1px solid #BBF7D0; padding:6px 14px; border-radius:9999px; font-size:13.5px; font-weight:600;">{icon_check} {kw}</span>'
                )
            chips_html = f'<div style="display:flex; flex-wrap:wrap; gap:8px; margin-top:8px;">{"".join(chips_parts)}</div>'
            st.markdown(chips_html, unsafe_allow_html=True)
        else:
            st.caption("No direct keyword matches found.")

    with col_missing:
        icon_x = get_svg_icon("x", size=14, color="#9F1239")
        st.markdown(f"#### Missing Keywords ({len(missing)})")
        if missing:
            chips_parts = []
            for kw in missing[:25]:
                chips_parts.append(
                    f'<span style="display:inline-flex; align-items:center; gap:6px; background:#FFE4E6; color:#9F1239; border:1px solid #FECDD3; padding:6px 14px; border-radius:9999px; font-size:13.5px; font-weight:600;">{icon_x} {kw}</span>'
                )
            chips_html = f'<div style="display:flex; flex-wrap:wrap; gap:8px; margin-top:8px;">{"".join(chips_parts)}</div>'
            st.markdown(chips_html, unsafe_allow_html=True)
        else:
            st.caption("All critical keywords from the job description are present!")

    if gap:
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        st.markdown(f"#### Skills Gap ({len(gap)})")
        gap_parts = []
        for skill in gap[:15]:
            gap_parts.append(
                f'<span style="display:inline-flex; align-items:center; background:#F1F5F9; color:#334155; border:1px solid #E2E8F0; padding:6px 14px; border-radius:9999px; font-size:13.5px; font-weight:600;">{skill}</span>'
            )
        gap_html = f'<div style="display:flex; flex-wrap:wrap; gap:8px; margin-top:8px;">{"".join(gap_parts)}</div>'
        st.markdown(gap_html, unsafe_allow_html=True)
