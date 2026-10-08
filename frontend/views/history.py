import textwrap
import pandas as pd
import requests
import streamlit as st

from frontend.services import api_client
from frontend.components._helpers import get_svg_icon


def _show_backend_error(exc: Exception) -> None:
    alert_icon = get_svg_icon("alert-triangle", size=18, color="#EF4444")
    if isinstance(exc, requests.ConnectionError):
        msg = "Unable to connect to the backend server. Is uvicorn running on port 8000?"
    elif isinstance(exc, requests.HTTPError) and exc.response is not None:
        msg = f"Server returned error code {exc.response.status_code}: {exc.response.text}"
    else:
        msg = f"Unexpected error: {exc}"

    st.markdown(textwrap.dedent(f"""
<div class="error-alert-card">
<div style="flex-shrink:0;">{alert_icon}</div>
<div>
<div class="error-title">History Error</div>
<div class="error-message">{msg}</div>
</div>
</div>
""").strip(), unsafe_allow_html=True)


def render() -> None:
    st.markdown('<div class="content-narrow">', unsafe_allow_html=True)

    header_html = textwrap.dedent("""
<div style="margin-bottom: 28px;">
<h1 style="font-size:32px; font-weight:800; color:#0F172A; margin-bottom:6px !important;">Analysis History</h1>
<p style="font-size:15px; color:#64748B; margin:0;">
Review previous resume scores, identify progression trends, and revisit detailed reports.
</p>
</div>
""").strip()
    st.markdown(header_html, unsafe_allow_html=True)

    access_token = st.session_state.get("access_token")
    if not access_token:
        st.warning("Please sign in from the top navigation bar to view your saved resume scans.")
        st.markdown('</div>', unsafe_allow_html=True)
        return

    try:
        history = api_client.get_history(access_token)
    except requests.RequestException as exc:
        _show_backend_error(exc)
        st.markdown('</div>', unsafe_allow_html=True)
        return

    # Empty State
    if not history:
        file_icon = get_svg_icon("file-text", size=32, color="#4F46E5")
        empty_html = textwrap.dedent(f"""
<div style="background:#FFFFFF; border:1px dashed #C7D2FE; border-radius:20px; padding:56px 24px; text-align:center; margin:32px 0;">
<div style="width:64px; height:64px; border-radius:50%; background:#EEF2FF; display:flex; align-items:center; justify-content:center; margin:0 auto 16px auto;">
{file_icon}
</div>
<h3 style="font-size:20px; font-weight:700; color:#0F172A; margin-bottom:8px;">No analyses yet</h3>
<p style="color:#64748B; font-size:14.5px; max-width:400px; margin:0 auto 24px auto;">
You haven't scanned any resumes under this account. Run your first analysis to see your score and history here.
</p>
</div>
""").strip()
        st.markdown(empty_html, unsafe_allow_html=True)

        _, btn_col, _ = st.columns([1, 1.4, 1])
        with btn_col:
            if st.button("Score Your First Resume", key="empty_scorer_cta", use_container_width=True):
                st.session_state.current_view = "scorer"
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        return

    # Summary Stat Cards on top
    scores = [float(entry.get("ats_score", 0)) for entry in history]
    total_count = len(history)
    avg_score = sum(scores) / total_count if total_count > 0 else 0.0
    best_score = max(scores) if scores else 0.0

    stat_col1, stat_col2, stat_col3 = st.columns(3)
    with stat_col1:
        st.markdown(textwrap.dedent(f"""
<div class="stat-card-modern">
<div class="stat-label">Total Analyses</div>
<div class="stat-value">{total_count}</div>
</div>
""").strip(), unsafe_allow_html=True)
    with stat_col2:
        st.markdown(textwrap.dedent(f"""
<div class="stat-card-modern">
<div class="stat-label">Average Score</div>
<div class="stat-value">{avg_score:.0f} <span style="font-size:16px; color:#94A3B8; font-weight:500;">/ 100</span></div>
</div>
""").strip(), unsafe_allow_html=True)
    with stat_col3:
        st.markdown(textwrap.dedent(f"""
<div class="stat-card-modern">
<div class="stat-label">Best Score</div>
<div class="stat-value">{best_score:.0f} <span style="font-size:16px; color:#94A3B8; font-weight:500;">/ 100</span></div>
</div>
""").strip(), unsafe_allow_html=True)

    # Score Trend Line Chart
    if len(history) >= 2:
        st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)
        st.markdown("### Score Progression Trend")
        try:
            reversed_history = list(reversed(history))
            chart_df = pd.DataFrame({
                "Scan": [f"#{i+1}" for i in range(len(reversed_history))],
                "Score": [float(entry.get("ats_score", 0)) for entry in reversed_history],
            })
            st.line_chart(chart_df.set_index("Scan"), height=220)
        except Exception:
            pass

    st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)
    st.markdown("### Past Analyses")

    # List of Past Analyses as clean card rows
    file_icon = get_svg_icon("file-text", size=18, color="#4F46E5")

    for idx, entry in enumerate(history):
        filename = entry.get("filename", "resume.pdf")
        ats_score = float(entry.get("ats_score", 0))
        created_at = (entry.get("created_at") or "")[:10]
        analysis = entry.get("analysis_result", {}) or {}
        entry_id = entry.get("id")

        if ats_score >= 80:
            pill_style = "background:#DCFCE7; color:#166534; border:1px solid #BBF7D0;"
        elif ats_score >= 60:
            pill_style = "background:#FEF3C7; color:#92400E; border:1px solid #FDE68A;"
        else:
            pill_style = "background:#FEE2E2; color:#991B1B; border:1px solid #FECDD3;"

        card_left_html = textwrap.dedent(f"""
<div class="history-row-card">
<div style="display:flex; align-items:center; gap:12px;">
{file_icon}
<div>
<div style="font-size:15px; font-weight:700; color:#0F172A;">{filename}</div>
<div style="font-size:12.5px; color:#94A3B8;">Scanned on {created_at}</div>
</div>
</div>
<span style="{pill_style} font-size:13px; font-weight:700; padding:4px 12px; border-radius:9999px;">
{ats_score:.0f} / 100
</span>
</div>
""").strip()
        st.markdown(card_left_html, unsafe_allow_html=True)

        col_v, col_d, _ = st.columns([1, 1, 2])
        with col_v:
            if st.button("View Report", key=f"view_hist_{idx}", use_container_width=True):
                st.session_state["scorer_analysis"] = analysis
                st.session_state.current_view = "scorer"
                st.rerun()
        with col_d:
            if entry_id and st.button("Delete", key=f"del_hist_{idx}", use_container_width=True):
                try:
                    api_client.delete_history_entry(str(entry_id), access_token)
                    st.toast("Entry deleted")
                    st.rerun()
                except requests.RequestException as exc:
                    _show_backend_error(exc)

    st.markdown('</div>', unsafe_allow_html=True)
