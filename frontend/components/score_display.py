import math
import textwrap
from typing import Any, Dict

import streamlit as st

from frontend.components._helpers import get_score_badge_info, get_svg_icon


COMPONENTS = [
    ("Formatting",        "formatting",        20, "layout"),
    ("Keywords & Skills", "keywords",          25, "key"),
    ("Content Quality",   "content",           25, "file-text"),
    ("Skill Validation",  "skill_validation",  15, "check-circle"),
    ("ATS Compatibility", "ats_compatibility", 15, "cpu"),
]


def display_overall_score(analysis: Dict[str, Any]) -> None:
    score = float(analysis.get("ATS_score", analysis.get("ats_score", 0)))
    score = max(0.0, min(100.0, score))
    interpretation = analysis.get("interpretation", "Your resume has been evaluated across key ATS screening dimensions.")
    filename = analysis.get("filename", "Resume.pdf")
    
    if score >= 80:
        stroke_color = "#16A34A"
        verdict_text = "Excellent ATS Match"
        verdict_badge_style = "background:#DCFCE7; color:#166534; border:1px solid #BBF7D0;"
    elif score >= 60:
        stroke_color = "#F59E0B"
        verdict_text = "Good ATS Match"
        verdict_badge_style = "background:#FEF3C7; color:#92400E; border:1px solid #FDE68A;"
    else:
        stroke_color = "#EF4444"
        verdict_text = "Needs Work"
        verdict_badge_style = "background:#FEE2E2; color:#991B1B; border:1px solid #FECDD3;"

    # SVG circular progress calculations (180px gauge, r=72)
    radius = 72
    circumference = 2 * math.pi * radius  # ~452.39
    dashoffset = circumference * (1.0 - (score / 100.0))

    col_gauge, col_info = st.columns([1, 1.4], gap="medium")

    with col_gauge:
        gauge_html = textwrap.dedent(f"""
<div class="results-hero-card" style="display:flex; justify-content:center; align-items:center;">
<div class="gauge-svg-container">
<svg width="180" height="180" viewBox="0 0 180 180" style="transform:rotate(-90deg);">
<circle cx="90" cy="90" r="{radius}" fill="none" stroke="#E2E8F0" stroke-width="12" />
<circle cx="90" cy="90" r="{radius}" fill="none" stroke="{stroke_color}" stroke-width="12"
        stroke-linecap="round"
        stroke-dasharray="{circumference:.2f}"
        stroke-dashoffset="{dashoffset:.2f}" />
</svg>
<div class="gauge-center-text">
<span class="gauge-score-huge">{score:.0f}</span>
<span class="gauge-score-max">/100</span>
</div>
</div>
</div>
""").strip()
        st.markdown(gauge_html, unsafe_allow_html=True)

    with col_info:
        file_icon = get_svg_icon("file-text", size=16, color="#64748B")
        info_html = textwrap.dedent(f"""
<div class="results-hero-card" style="height:100%; display:flex; flex-direction:column; justify-content:center;">
<div style="margin-bottom:12px;">
<span style="{verdict_badge_style} font-size:13px; font-weight:700; padding:4px 12px; border-radius:9999px; text-transform:uppercase; letter-spacing:0.04em;">
{verdict_text}
</span>
</div>
<h2 style="font-size:24px; font-weight:800; color:#0F172A; margin:0 0 8px 0 !important;">Overall ATS Compatibility</h2>
<p style="color:#475569; font-size:15px; line-height:1.55; margin-bottom:16px;">
{interpretation}
</p>
<div style="display:flex; align-items:center; gap:8px; font-size:13.5px; color:#64748B;">
{file_icon}
<span style="font-weight:600; color:#1E293B;">{filename}</span>
<span>&bull; Verified Scan</span>
</div>
</div>
""").strip()
        st.markdown(info_html, unsafe_allow_html=True)


def display_score_breakdown(analysis: Dict[str, Any]) -> None:
    component_scores = analysis.get("component_scores") or {}

    st.markdown("### Category Breakdown")

    for label, key, max_score, icon_name in COMPONENTS:
        value = float(component_scores.get(key, 0))
        pct = (value / max_score) if max_score > 0 else 0.0
        pct_clamped = min(max(pct, 0.0), 1.0)
        pct_display = int(pct_clamped * 100)

        if pct_clamped >= 0.8:
            bar_color = "#16A34A"
        elif pct_clamped >= 0.6:
            bar_color = "#F59E0B"
        else:
            bar_color = "#EF4444"

        icon_svg = get_svg_icon(icon_name, size=16, color="#4F46E5")

        row_html = textwrap.dedent(f"""
<div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:12px; padding:14px 18px; margin-bottom:10px; box-shadow:0 1px 2px rgba(15,23,42,0.03);">
<div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:8px;">
<div style="display:flex; align-items:center; gap:8px;">
{icon_svg}
<span style="font-size:14.5px; font-weight:600; color:#0F172A;">{label}</span>
</div>
<div style="font-size:14.5px; font-weight:700; color:#0F172A;">
{value:.0f} <span style="font-weight:400; color:#94A3B8; font-size:13px;">/ {max_score} pts</span>
</div>
</div>
<div style="width:100%; height:8px; background:#F1F5F9; border-radius:9999px; overflow:hidden;">
<div style="width:{pct_display}%; height:100%; background:{bar_color}; border-radius:9999px; transition:width 0.5s ease;"></div>
</div>
</div>
""").strip()
        st.markdown(row_html, unsafe_allow_html=True)
