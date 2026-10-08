from typing import Any, Dict

import streamlit as st

from frontend.components._helpers import get_svg_icon


def display_skill_validation(analysis: Dict[str, Any]) -> None:
    details = analysis.get("skill_validation_details") or {}
    validated = details.get("validated", [])
    unvalidated = details.get("unvalidated", [])
    total = details.get("total", len(validated) + len(unvalidated))
    pct = details.get("validation_pct", 0.0)

    st.markdown("### Semantic Skill Validation")
    st.caption("Verifies whether skills listed are backed by tangible evidence in your experience and projects.")

    if total == 0:
        st.info("No explicit skills detected in the parsed resume.")
        return

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Skills", total)
    c2.metric("Evidence Found", len(validated))
    c3.metric("Validation Rate", f"{pct:.0f}%")

    st.progress(min(max(pct / 100.0, 0.0), 1.0))

    col_val, col_unval = st.columns(2)

    with col_val:
        icon_check = get_svg_icon("check", size=14, color="#059669")
        st.markdown(f"#### Validated Skills ({len(validated)})")
        if validated:
            chips_html = '<div class="chips-container">'
            for entry in validated[:16]:
                skill = entry.get("skill", "")
                chips_html += f'<span class="chip chip-matched">{icon_check} {skill}</span>'
            chips_html += '</div>'
            st.markdown(chips_html, unsafe_allow_html=True)

            with st.expander("View Evidence Linkage", expanded=False):
                for entry in validated:
                    skill = entry.get("skill", "?")
                    projects = entry.get("projects", []) or []
                    similarity = entry.get("similarity")
                    project_text = ", ".join(projects[:3]) if projects else "Experience section"
                    sim_text = f" ({similarity * 100:.0f}% confidence)" if isinstance(similarity, (int, float)) else ""
                    st.markdown(f"• **{skill}**{sim_text} — demonstrated in: *{project_text}*")
        else:
            st.caption("No skills with verified project context found.")

    with col_unval:
        icon_alert = get_svg_icon("alert-triangle", size=14, color="#D97706")
        st.markdown(f"#### Unvalidated Skills ({len(unvalidated)})")
        st.caption("Listed in skills section but lacking demonstrable evidence in job bullets.")
        if unvalidated:
            chips_html = '<div class="chips-container">'
            for skill in unvalidated[:16]:
                chips_html += f'<span class="chip chip-missing">{icon_alert} {skill}</span>'
            chips_html += '</div>'
            st.markdown(chips_html, unsafe_allow_html=True)
        else:
            st.caption("All skills are supported by project or work experience.")
