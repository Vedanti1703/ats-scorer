import textwrap
from typing import Optional

import requests
import streamlit as st

from frontend.services import api_client
from frontend.components.dashboard import display_results_dashboard
from frontend.components._helpers import get_svg_icon


def _read_jd(jd_file, jd_text: str) -> str:
    """Turn whatever the user provided into a plain JD string for the backend."""
    if jd_text:
        return jd_text.strip()
    if jd_file is None:
        return ""
    if jd_file.name.lower().endswith(".txt"):
        return jd_file.getvalue().decode("utf-8", errors="ignore")
    st.warning(
        "Job description files must be plain text (.txt). If your JD is in PDF or DOCX format, "
        "please paste the text into the text area instead."
    )
    return ""


def _show_backend_error(exc: Exception) -> None:
    """Styled alert card with an icon, clear title, short message, and collapsible technical details."""
    alert_icon = get_svg_icon("alert-triangle", size=20, color="#EF4444")
    
    if isinstance(exc, requests.ConnectionError):
        title = "Cannot Connect to Analysis Server"
        short_msg = "The backend service is unreachable. Please verify that FastAPI is running on port 8000."
    elif isinstance(exc, requests.Timeout):
        title = "Request Timed Out"
        short_msg = "The analysis took too long to complete. Try a smaller file or check server logs."
    elif isinstance(exc, requests.HTTPError) and exc.response is not None:
        title = f"Server Error (HTTP {exc.response.status_code})"
        try:
            short_msg = str(exc.response.json().get("detail", exc.response.text))
        except ValueError:
            short_msg = exc.response.text
    else:
        title = "Analysis Error"
        short_msg = "An unexpected error occurred during resume evaluation."

    alert_html = textwrap.dedent(f"""
<div class="error-alert-card">
<div style="flex-shrink:0; margin-top:2px;">{alert_icon}</div>
<div>
<div class="error-title">{title}</div>
<div class="error-message">{short_msg}</div>
</div>
</div>
""").strip()
    st.markdown(alert_html, unsafe_allow_html=True)

    with st.expander("Technical details", expanded=False):
        st.code(str(exc), language="text")


def _summary_text(analysis: dict) -> str:
    """Plain-text summary for client-side download."""
    score = analysis.get("ATS_score", analysis.get("ats_score", 0))
    lines = [f"ATS Score: {score:.0f}/100", ""]
    if analysis.get("strengths"):
        lines.append("STRENGTHS:")
        lines.extend(f"  - {s}" for s in analysis["strengths"])
        lines.append("")
    if analysis.get("critical_issues"):
        lines.append("CRITICAL ISSUES:")
        lines.extend(f"  - {s}" for s in analysis["critical_issues"])
        lines.append("")
    if analysis.get("suggestions"):
        lines.append("SUGGESTIONS:")
        lines.extend(f"  - {s}" for s in analysis["suggestions"])
    return "\n".join(lines)


def _render_export_buttons(analysis: dict) -> None:
    st.markdown("<div style='display:flex; justify-content:flex-end; gap:12px; margin-bottom:16px;'>", unsafe_allow_html=True)
    c1, c2 = st.columns([1, 1])

    with c1:
        if st.button("Generate PDF Report", key="gen_pdf_btn", use_container_width=True):
            try:
                with st.spinner("Generating official PDF report..."):
                    pdf_bytes = api_client.generate_pdf(
                        analysis,
                        access_token=st.session_state["access_token"],
                    )
                st.session_state["scorer_pdf_bytes"] = pdf_bytes
            except requests.RequestException as exc:
                _show_backend_error(exc)

        if "scorer_pdf_bytes" in st.session_state:
            st.download_button(
                "Download PDF",
                data=st.session_state["scorer_pdf_bytes"],
                file_name="ats_resume_report.pdf",
                mime="application/pdf",
                use_container_width=True,
                key="download_pdf_report",
            )

    with c2:
        st.download_button(
            "Download Summary (.txt)",
            data=_summary_text(analysis),
            file_name="ats_summary.txt",
            mime="text/plain",
            use_container_width=True,
            key="download_summary",
        )
    st.markdown("</div>", unsafe_allow_html=True)


def render() -> None:
    st.markdown('<div class="content-narrow">', unsafe_allow_html=True)

    # Page Title
    header_html = textwrap.dedent("""
<div style="text-align:center; margin-bottom: 36px;">
<h1 style="font-size:36px; font-weight:800; color:#0F172A; margin-bottom:8px !important;">Resume Analyzer</h1>
<p style="font-size:16px; color:#64748B; max-width:540px; margin:0 auto;">
Upload your resume and optionally match against a job description to get instant ATS scoring and actionable guidance.
</p>
</div>
""").strip()
    st.markdown(header_html, unsafe_allow_html=True)

    # Step 1 Card: Upload Resume
    step1_head = textwrap.dedent("""
<div class="stepper-card-wrapper">
<div class="stepper-header-row">
<div class="stepper-number-badge">1</div>
<div class="stepper-title">Upload Your Resume</div>
</div>
""").strip()
    st.markdown(step1_head, unsafe_allow_html=True)

    resume_file = st.file_uploader(
        "Choose your resume file (PDF, DOC or DOCX)",
        type=["pdf", "doc", "docx"],
        help="Supported formats: PDF, DOC, DOCX up to 5 MB",
        key="resume_upload",
        label_visibility="collapsed",
    )
    if resume_file:
        check_icon = get_svg_icon("check", size=14, color="#16A34A")
        badge_html = textwrap.dedent(f"""
<div style="display:inline-flex; align-items:center; gap:8px; background:#DCFCE7; border:1px solid #BBF7D0; padding:6px 14px; border-radius:9999px; margin-top:10px;">
{check_icon}
<span style="font-size:13px; font-weight:600; color:#166534;">{resume_file.name} ({(resume_file.size / 1024):.1f} KB)</span>
</div>
""").strip()
        st.markdown(badge_html, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # Step 2 Card: Add Job Description
    step2_head = textwrap.dedent("""
<div class="stepper-card-wrapper">
<div class="stepper-header-row">
<div class="stepper-number-badge">2</div>
<div class="stepper-title">Add Job Description (Optional)</div>
</div>
""").strip()
    st.markdown(step2_head, unsafe_allow_html=True)

    jd_method = st.radio(
        "Input method:",
        ["Paste JD Text", "Upload .txt File", "General Scoring (No JD)"],
        horizontal=True,
        key="jd_input_method",
        label_visibility="collapsed",
    )

    jd_file = None
    jd_text = ""

    if jd_method == "Paste JD Text":
        jd_text = st.text_area(
            "Paste Job Description:",
            height=140,
            placeholder="Paste target job responsibilities, qualifications, and requirements here...",
            key="jd_text",
            label_visibility="collapsed",
        )
    elif jd_method == "Upload .txt File":
        jd_file = st.file_uploader(
            "Upload Job Description (.txt only)",
            type=["txt"],
            key="jd_upload",
            label_visibility="collapsed",
        )
    else:
        st.caption("General ATS Scoring mode evaluates overall resume structure, readability, and content quality without a specific target role.")

    st.markdown("</div>", unsafe_allow_html=True)

    # Step 3 Card: Analyze
    step3_head = textwrap.dedent("""
<div class="stepper-card-wrapper">
<div class="stepper-header-row">
<div class="stepper-number-badge">3</div>
<div class="stepper-title">Run ATS Inspection</div>
</div>
""").strip()
    st.markdown(step3_head, unsafe_allow_html=True)

    access_token = st.session_state.get("access_token")

    if not resume_file:
        st.info("Upload your resume in Step 1 to begin.")
        st.markdown("</div>", unsafe_allow_html=True)
        if st.session_state.get("scorer_analysis"):
            display_results_dashboard(st.session_state["scorer_analysis"])
        st.markdown('</div>', unsafe_allow_html=True)
        return

    if not access_token:
        st.warning("Please sign in or create an account using the top navigation bar to analyze your resume.")
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        return

    # Prominent Full-Width Green Analyze Button
    analyze = st.button("Run Comprehensive ATS Analysis", key="analyze_btn", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    if not analyze:
        if st.session_state.get("scorer_analysis"):
            _render_export_buttons(st.session_state["scorer_analysis"])
            display_results_dashboard(st.session_state["scorer_analysis"])
        st.markdown('</div>', unsafe_allow_html=True)
        return

    # Fresh Analysis Execution
    st.session_state.pop("scorer_pdf_bytes", None)
    st.session_state.pop("scorer_analysis", None)

    job_description = _read_jd(jd_file, jd_text) if jd_method != "General Scoring (No JD)" else ""

    try:
        with st.spinner("Analyzing resume structure, keyword match, and semantic skill evidence..."):
            analysis = api_client.analyze_resume(
                resume_file=resume_file,
                access_token=access_token,
                job_description=job_description,
            )
    except requests.RequestException as exc:
        _show_backend_error(exc)
        st.markdown('</div>', unsafe_allow_html=True)
        return

    st.session_state["scorer_analysis"] = analysis
    _render_export_buttons(analysis)
    display_results_dashboard(analysis)

    st.markdown('</div>', unsafe_allow_html=True)
