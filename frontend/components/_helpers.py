from typing import Tuple

__all__ = [
    "get_score_color",
    "get_score_badge_info",
    "get_score_emoji",
    "get_severity_style",
    "get_severity_badge_class",
    "get_svg_icon",
    "SVG_ICONS",
]


def get_score_color(score: float) -> Tuple[str, str]:
    """Return (text_color, background_color) for a 0–100 score."""
    if score >= 80:
        return "#16A34A", "#DCFCE7"
    if score >= 60:
        return "#D97706", "#FEF3C7"
    return "#E11D48", "#FFE4E6"


def get_score_badge_info(score: float) -> Tuple[str, str, str]:
    """Return (verdict_label, badge_class, stroke_color) for gauges."""
    if score >= 80:
        return "Excellent ATS Score", "badge-excellent", "#16A34A"
    if score >= 60:
        return "Good ATS Score", "badge-good", "#F59E0B"
    return "Needs Improvement", "badge-needs-work", "#EF4444"


def get_score_emoji(score: float) -> str:
    """Fallback text symbol for backward compatibility."""
    if score >= 80:
        return "✓"
    if score >= 60:
        return "•"
    return "!"


def get_severity_style(severity: str) -> Tuple[str, str, str]:
    level = (severity or "").lower()
    if level in ("critical", "high"):
        return "●", "#EF4444", "#FEE2E2"
    if level == "medium":
        return "▲", "#F59E0B", "#FEF3C7"
    return "✓", "#16A34A", "#DCFCE7"


def get_severity_badge_class(severity: str) -> str:
    level = (severity or "").lower()
    if level in ("critical", "high"):
        return "sev-high"
    if level == "medium":
        return "sev-medium"
    return "sev-low"


SVG_ICONS = {
    "target": """<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
<circle cx="12" cy="12" r="10"></circle>
<circle cx="12" cy="12" r="6"></circle>
<circle cx="12" cy="12" r="2"></circle>
</svg>""",

    "rocket": """<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
<path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z"></path>
<path d="M12 15l-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z"></path>
<path d="M9 12H4s.55-3.03 2-4c1.62-1.08 5 0 5 0"></path>
<path d="M12 15v5s3.03-.55 4-2c1.08-1.62 0-5 0-5"></path>
</svg>""",

    "trending-up": """<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
<polyline points="23 6 13.5 15.5 8.5 10.5 1 18"></polyline>
<polyline points="17 6 23 6 23 12"></polyline>
</svg>""",

    "check-circle": """<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
<polyline points="22 4 12 14.01 9 11.01"></polyline>
</svg>""",

    "user": """<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
<path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
<circle cx="12" cy="7" r="4"></circle>
</svg>""",

    "bell": """<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
<path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path>
<path d="M13.73 21a2 2 0 0 1-3.46 0"></path>
</svg>""",

    "upload-cloud": """<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
<polyline points="16 16 12 12 8 16"></polyline>
<line x1="12" y1="12" x2="12" y2="21"></line>
<path d="M20.39 18.39A5 5 0 0 0 18 9h-1.26A8 8 0 1 0 3 16.3"></path>
<polyline points="16 16 12 12 8 16"></polyline>
</svg>""",

    "file-text": """<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
<polyline points="14 2 14 8 20 8"></polyline>
<line x1="16" y1="13" x2="8" y2="13"></line>
<line x1="16" y1="17" x2="8" y2="17"></line>
<polyline points="10 9 9 9 8 9"></polyline>
</svg>""",

    "key": """<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
<path d="M21 2l-2 2m-1.5 1.5L14 9l-1.5-1.5L10 10l-1.5-1.5-4 4a5 5 0 1 0 7.07 7.07l4-4L14 14l2.5-2.5 1.5 1.5 3.5-3.5-2-2 1.5-1.5z"></path>
</svg>""",

    "cpu": """<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
<rect x="4" y="4" width="16" height="16" rx="2" ry="2"></rect>
<rect x="9" y="9" width="6" height="6"></rect>
<line x1="9" y1="1" x2="9" y2="4"></line>
<line x1="15" y1="1" x2="15" y2="4"></line>
<line x1="9" y1="20" x2="9" y2="23"></line>
<line x1="15" y1="20" x2="15" y2="23"></line>
<line x1="20" y1="9" x2="23" y2="9"></line>
<line x1="20" y1="14" x2="23" y2="14"></line>
<line x1="1" y1="9" x2="4" y2="9"></line>
<line x1="1" y1="14" x2="4" y2="14"></line>
</svg>""",

    "layout": """<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
<rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
<line x1="3" y1="9" x2="21" y2="9"></line>
<line x1="9" y1="21" x2="9" y2="9"></line>
</svg>""",

    "alert-triangle": """<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
<path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path>
<line x1="12" y1="9" x2="12" y2="13"></line>
<line x1="12" y1="17" x2="12.01" y2="17"></line>
</svg>""",

    "check": """<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
<polyline points="20 6 9 17 4 12"></polyline>
</svg>""",

    "x": """<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
<line x1="18" y1="6" x2="6" y2="18"></line>
<line x1="6" y1="6" x2="18" y2="18"></line>
</svg>""",

    "sparkles": """<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
<path d="M12 2v4m0 12v4M4.93 4.93l2.83 2.83m8.48 8.48l2.83 2.83M2 12h4m12 0h4M4.93 19.07l2.83-2.83m8.48-8.48l2.83-2.83"></path>
</svg>""",

    "trash": """<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
<polyline points="3 6 5 6 21 6"></polyline>
<path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
</svg>""",

    "download": """<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
<polyline points="7 10 12 15 17 10"></polyline>
<line x1="12" y1="15" x2="12" y2="3"></line>
</svg>""",
}


def get_svg_icon(name: str, size: int = 18, color: str = "currentColor") -> str:
    template = SVG_ICONS.get(name, SVG_ICONS["sparkles"])
    return template.format(size=size, color=color)
