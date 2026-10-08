import sys
import textwrap
from pathlib import Path

import streamlit as st

# Put repo root on sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Configure page
st.set_page_config(
    page_title="ATS Analyzer",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Auth state defaults
for key, default in [
    ("access_token", None),
    ("refresh_token", None),
    ("user_id", None),
    ("user_email", None),
    ("auth_error", None),
    ("auth_info", None),
]:
    if key not in st.session_state:
        st.session_state[key] = default

# Exchange Google OAuth ?code= param if returning from redirect
if not st.session_state.access_token and "code" in st.query_params:
    from frontend.services import supabase_client
    result = supabase_client.exchange_code_for_session(st.query_params["code"])
    st.query_params.clear()
    if "error" in result:
        st.session_state.auth_error = f"Google sign-in failed: {result['error']}"
    else:
        st.session_state.access_token  = result["access_token"]
        st.session_state.refresh_token = result["refresh_token"]
        st.session_state.user_id       = result["user_id"]
        st.session_state.user_email    = result["email"]
        st.rerun()

# Load custom CSS
def load_css():
    try:
        css_path = Path(__file__).parent / 'assets' / 'styles.css'
        with open(css_path, 'r', encoding='utf-8') as f:
            return f'<style>{f.read()}</style>'
    except FileNotFoundError:
        return ''

st.markdown(load_css(), unsafe_allow_html=True)

# View state
if 'current_view' not in st.session_state:
    st.session_state.current_view = 'landing'

from frontend.services import supabase_client

try:
    import frontend.components._helpers as _helpers_mod
    import importlib
    importlib.reload(_helpers_mod)
    get_svg_icon = _helpers_mod.get_svg_icon
except Exception:
    from frontend.components._helpers import get_svg_icon

# Auth Dialog Modal
@st.dialog("Welcome to ATS Analyzer")
def auth_dialog_modal():
    modal_head_svg = get_svg_icon("target", size=24, color="#FFFFFF")
    modal_head_html = textwrap.dedent(f"""
<div style="text-align:center; margin-bottom:16px;">
<div style="width:48px; height:48px; border-radius:12px; background:linear-gradient(135deg,#2563EB,#4F46E5); display:inline-flex; align-items:center; justify-content:center; color:#FFFFFF; margin-bottom:10px; box-shadow:0 4px 12px rgba(37,99,235,0.25);">
{modal_head_svg}
</div>
<h3 style="margin:0; font-size:20px; font-weight:800; color:#0F172A;">Sign in to ATS Analyzer</h3>
<p style="font-size:13.5px; color:#64748B; margin-top:4px;">Optimize your resume and save analysis reports.</p>
</div>
""").strip()
    st.markdown(modal_head_html, unsafe_allow_html=True)

    if st.session_state.auth_error:
        st.error(st.session_state.auth_error)
        st.session_state.auth_error = None
    if st.session_state.auth_info:
        st.info(st.session_state.auth_info)
        st.session_state.auth_info = None

    tab_in, tab_up = st.tabs(["Sign In", "Sign Up"])

    with tab_in:
        with st.form("dialog_signin_form", clear_on_submit=False):
            email = st.text_input("Email", key="modal_signin_email")
            password = st.text_input("Password", type="password", key="modal_signin_pw")
            submitted = st.form_submit_button("Sign In", use_container_width=True, type="primary")
        if submitted:
            result = supabase_client.sign_in_with_password(email, password)
            if "error" in result:
                st.session_state.auth_error = result["error"]
            else:
                st.session_state.access_token  = result["access_token"]
                st.session_state.refresh_token = result["refresh_token"]
                st.session_state.user_id       = result["user_id"]
                st.session_state.user_email    = result["email"]
            st.rerun()

    with tab_up:
        with st.form("dialog_signup_form", clear_on_submit=False):
            email_up = st.text_input("Email", key="modal_signup_email")
            password_up = st.text_input("Password (min 6 chars)", type="password", key="modal_signup_pw")
            submitted_up = st.form_submit_button("Create Account", use_container_width=True, type="primary")
        if submitted_up:
            result = supabase_client.sign_up_with_password(email_up, password_up)
            if "error" in result:
                st.session_state.auth_error = result["error"]
            elif result.get("pending_confirmation"):
                st.session_state.auth_info = f"Check your inbox — confirmation email sent to {result['email']}."
            else:
                st.session_state.access_token  = result["access_token"]
                st.session_state.refresh_token = result["refresh_token"]
                st.session_state.user_id       = result["user_id"]
                st.session_state.user_email    = result["email"]
            st.rerun()

    divider_html = textwrap.dedent("""
<div style="display:flex; align-items:center; margin:14px 0; color:#94A3B8; font-size:12px;">
<div style="flex:1; height:1px; background:#E2E8F0;"></div>
<span style="padding:0 8px; text-transform:uppercase; letter-spacing:0.06em; font-weight:600;">or</span>
<div style="flex:1; height:1px; background:#E2E8F0;"></div>
</div>
""").strip()
    st.markdown(divider_html, unsafe_allow_html=True)

    oauth = supabase_client.google_oauth_url()
    if "error" in oauth:
        st.caption(f"Google sign-in unavailable: {oauth['error']}")
    else:
        st.link_button(
            "Continue with Google",
            url=oauth["url"],
            use_container_width=True,
        )

# Automatically open auth modal if pending error/info
if (st.session_state.auth_error or st.session_state.auth_info) and not st.session_state.access_token:
    auth_dialog_modal()

# Top Sticky Navigation Bar (Matching Screenshot Exactly: Logo | Home Analyzer Profile | Divider Bell Avatar)
with st.container(key="topnav"):
    col_logo, col_home, col_analyzer, col_profile, col_actions = st.columns(
        [3.0, 1.0, 1.1, 1.0, 2.5],
        vertical_alignment="center"
    )

    with col_logo:
        target_svg = get_svg_icon("target", size=20, color="#FFFFFF")
        logo_html = textwrap.dedent(f"""
<div class="logo-lockup">
<div class="logo-tile">{target_svg}</div>
<span class="logo-wordmark">ATS Analyzer</span>
</div>
""").strip()
        st.markdown(logo_html, unsafe_allow_html=True)

    with col_home:
        if st.button("Home", key="nav_home", use_container_width=True):
            st.session_state.current_view = 'landing'
            st.rerun()

    with col_analyzer:
        if st.button("Analyzer", key="nav_analyzer", use_container_width=True):
            st.session_state.current_view = 'scorer'
            st.rerun()

    with col_profile:
        if st.button("Profile", key="nav_profile", use_container_width=True):
            st.session_state.current_view = 'profile'
            st.rerun()

    with col_actions:
        # Divider, Bell with red dot, and Crimson Avatar with "S" initial
        c_div, c_bell, c_avatar = st.columns([0.2, 0.8, 1.2], vertical_alignment="center")
        with c_div:
            st.markdown('<div style="width:1px; height:28px; background:#E2E8F0; margin:0 auto;"></div>', unsafe_allow_html=True)
        with c_bell:
            bell_icon = get_svg_icon("bell", size=22, color="#64748B")
            dot_tag = '<span style="position:absolute; top:-2px; right:2px; width:8px; height:8px; border-radius:50%; background:#EF4444; border:1.5px solid #FFFFFF;"></span>'
            bell_html = f'<div style="position:relative; display:inline-flex; align-items:center; cursor:pointer;" title="Notifications">{bell_icon}{dot_tag}</div>'
            st.markdown(bell_html, unsafe_allow_html=True)
        with c_avatar:
            initial = (st.session_state.user_email[:1] if st.session_state.user_email else "S").upper()
            with st.popover(initial, help="Account"):
                if st.session_state.access_token:
                    st.markdown(f"**{st.session_state.user_email}**")
                    st.caption("Active Session")
                    if st.button("Sign Out", key="top_signout_btn", use_container_width=True):
                        supabase_client.sign_out()
                        for k in ("access_token", "refresh_token", "user_id", "user_email"):
                            st.session_state[k] = None
                        st.rerun()
                else:
                    st.markdown("**User Account**")
                    st.caption("Sign in to save your scans across sessions")
                    if st.button("Sign In / Sign Up", key="popover_signin_btn", use_container_width=True):
                        auth_dialog_modal()

# Dynamic CSS to highlight active nav link with darker bold text
active_key = (
    "home" if st.session_state.current_view == "landing"
    else ("analyzer" if st.session_state.current_view == "scorer"
    else ("profile" if st.session_state.current_view in ("profile", "history")
    else "home"))
)
st.markdown(
    f"""
    <style>
    .st-key-nav_{active_key} button {{
        color: #0F172A !important;
        font-weight: 700 !important;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# Render main views based on current_view
if st.session_state.current_view == 'landing':
    from frontend.views import landing
    landing.render()

elif st.session_state.current_view == 'scorer':
    from frontend.views import scorer
    scorer.render()

elif st.session_state.current_view == 'history':
    from frontend.views import history
    history.render()

elif st.session_state.current_view == 'resources':
    from frontend.views import resources
    resources.render()

elif st.session_state.current_view == 'profile':
    from frontend.views import profile
    profile.render()
