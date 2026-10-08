import textwrap
import pandas as pd
import requests
import streamlit as st

from frontend.services import api_client, supabase_client
from frontend.components._helpers import get_svg_icon


def render():
    st.markdown('<div class="content-narrow">', unsafe_allow_html=True)

    access_token = st.session_state.get("access_token")
    user_email = st.session_state.get("user_email")

    if not access_token:
        # Prompt to sign in if signed out
        user_icon = get_svg_icon("user", size=32, color="#64748B")
        st.markdown(
            f"""
            <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:20px; padding:48px 32px; text-align:center; box-shadow:0 8px 24px rgba(15,23,42,0.06); margin-top:20px;">
                <div style="width:64px; height:64px; border-radius:50%; background:#F1F5F9; display:flex; align-items:center; justify-content:center; margin:0 auto 16px auto;">
                    {user_icon}
                </div>
                <h2 style="font-size:24px; font-weight:700; color:#0F172A; margin-bottom:8px;">Account Profile</h2>
                <p style="color:#64748B; font-size:15px; max-width:420px; margin:0 auto 24px auto;">
                    Sign in to your ATS Analyzer account to view your profile, manage saved resume scans, and track your scoring progress.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown('</div>', unsafe_allow_html=True)
        return

    # Signed in state
    initial = (user_email[:1] if user_email else "S").upper()

    st.markdown(
        f"""
        <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:20px; padding:32px; box-shadow:0 8px 24px rgba(15,23,42,0.06); margin-bottom:24px;">
            <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:16px;">
                <div style="display:flex; align-items:center; gap:20px;">
                    <div style="width:72px; height:72px; border-radius:50%; background:#B91C1C; color:#FFFFFF; font-size:28px; font-weight:800; display:flex; align-items:center; justify-content:center; box-shadow:0 4px 14px rgba(185,28,28,0.35); flex-shrink:0;">
                        {initial}
                    </div>
                    <div>
                        <h1 style="font-size:24px; font-weight:800; color:#0F172A; margin:0 0 4px 0 !important;">User Profile</h1>
                        <div style="font-size:15px; font-weight:500; color:#475569;">{user_email}</div>
                        <div style="display:inline-flex; align-items:center; gap:6px; margin-top:6px; background:#ECFDF5; border:1px solid #D1FAE5; padding:2px 8px; border-radius:9999px;">
                            <span style="width:6px; height:6px; border-radius:50%; background:#10B981;"></span>
                            <span style="font-size:11.5px; font-weight:700; color:#065F46; text-transform:uppercase;">Active Account</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Fetch stats from history API
    history = []
    total_analyses = 0
    avg_score = 0.0
    best_score = 0.0

    try:
        history = api_client.get_history(access_token) or []
        if history:
            total_analyses = len(history)
            scores = [float(entry.get("ats_score", 0)) for entry in history]
            avg_score = sum(scores) / len(scores) if scores else 0.0
            best_score = max(scores) if scores else 0.0
    except requests.RequestException:
        pass

    # Overview Stat Cards
    st.markdown("### Activity Overview")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            f"""
            <div class="stat-card-modern">
                <div class="stat-label">Total Resumes Scanned</div>
                <div class="stat-value">{total_analyses}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            f"""
            <div class="stat-card-modern">
                <div class="stat-label">Average ATS Score</div>
                <div class="stat-value">{avg_score:.0f} <span style="font-size:15px; color:#94A3B8; font-weight:500;">/ 100</span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            f"""
            <div class="stat-card-modern">
                <div class="stat-label">Highest Score</div>
                <div class="stat-value">{best_score:.0f} <span style="font-size:15px; color:#94A3B8; font-weight:500;">/ 100</span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)

    # Tabs for History & Resources inside Profile
    tab_history, tab_resources, tab_account = st.tabs(["Saved Analyses", "ATS Guidelines", "Account Settings"])

    with tab_history:
        if not history:
            file_icon = get_svg_icon("file-text", size=32, color="#4F46E5")
            st.markdown(
                f"""
                <div style="background:#FFFFFF; border:1px dashed #C7D2FE; border-radius:20px; padding:48px 24px; text-align:center; margin:24px 0;">
                    <div style="width:64px; height:64px; border-radius:50%; background:#EEF2FF; display:flex; align-items:center; justify-content:center; margin:0 auto 16px auto;">
                        {file_icon}
                    </div>
                    <h3 style="font-size:19px; font-weight:700; color:#0F172A; margin-bottom:8px;">No analyses yet</h3>
                    <p style="color:#64748B; font-size:14px; max-width:380px; margin:0 auto 20px auto;">
                        Run your first resume scan on the Analyzer page to save your baseline score.
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button("Go to Resume Analyzer", key="prof_to_scorer", use_container_width=True):
                st.session_state.current_view = "scorer"
                st.rerun()
        else:
            if len(history) >= 2:
                st.markdown("#### Score Progression Trend")
                try:
                    reversed_history = list(reversed(history))
                    chart_df = pd.DataFrame({
                        "Scan": [f"#{i+1}" for i in range(len(reversed_history))],
                        "Score": [float(entry.get("ats_score", 0)) for entry in reversed_history],
                    })
                    st.line_chart(chart_df.set_index("Scan"), height=200)
                except Exception:
                    pass

            st.markdown(f"#### Saved Resumes ({len(history)})")
            file_icon = get_svg_icon("file-text", size=18, color="#4F46E5")

            for idx, entry in enumerate(history):
                filename = entry.get("filename", "resume.pdf")
                ats_score = float(entry.get("ats_score", 0))
                created_at = (entry.get("created_at") or "")[:10]
                analysis = entry.get("analysis_result", {}) or {}
                entry_id = entry.get("id")

                pill_style = (
                    "background:#DCFCE7; color:#166534; border:1px solid #BBF7D0;"
                    if ats_score >= 80
                    else (
                        "background:#FEF3C7; color:#92400E; border:1px solid #FDE68A;"
                        if ats_score >= 60
                        else "background:#FEE2E2; color:#991B1B; border:1px solid #FECDD3;"
                    )
                )

                st.markdown(
                    f"""
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
                    """,
                    unsafe_allow_html=True,
                )

                col_v, col_d, _ = st.columns([1, 1, 2])
                with col_v:
                    if st.button("View Report", key=f"prof_view_hist_{idx}", use_container_width=True):
                        st.session_state["scorer_analysis"] = analysis
                        st.session_state.current_view = "scorer"
                        st.rerun()
                with col_d:
                    if entry_id and st.button("Delete", key=f"prof_del_hist_{idx}", use_container_width=True):
                        try:
                            api_client.delete_history_entry(str(entry_id), access_token)
                            st.toast("Record deleted")
                            st.rerun()
                        except requests.RequestException:
                            st.error("Failed to delete record.")

    with tab_resources:
        from frontend.views import resources
        resources.render()

    with tab_account:
        st.markdown("#### Account Management")
        st.write(f"Connected as **{user_email}**")
        st.caption("All authentication sessions are managed securely with Supabase.")
        if st.button("Sign Out of Account", key="prof_signout_btn", use_container_width=True):
            supabase_client.sign_out()
            for k in ("access_token", "refresh_token", "user_id", "user_email"):
                st.session_state[k] = None
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
