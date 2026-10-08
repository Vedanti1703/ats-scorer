import streamlit as st
import textwrap

from frontend.components._helpers import get_svg_icon


def render():
    st.markdown('<div class="content-wrapper">', unsafe_allow_html=True)

    # Hero Row: Two Columns (~55% / 45%)
    col_text, col_preview = st.columns([1.2, 1], gap="large")

    with col_text:
        hero_left_html = textwrap.dedent(f"""
<div class="hero-section">
<div class="pill-badge">
<div class="pill-dot"></div>
<span class="pill-text">AI-Powered Resume Analysis</span>
</div>
<h1 class="hero-headline">
Save hours by<br>using <span class="ai-gradient-text">AI</span> for your<br>job hunt
</h1>
<p class="hero-subtext">
This AI-powered resume analyzer helps candidates improve their resumes and pass ATS screening systems used by recruiters. Land more interviews and beat the ATS.
</p>
</div>
""").strip()
        st.markdown(hero_left_html, unsafe_allow_html=True)

        # Dual Buttons Matching Screenshot:
        # Left: Green "Build Your Resume" (with rocket icon)
        # Right: White "Get Your Resume Score" (with trending-up icon)
        c_left_btn, c_right_btn = st.columns(2)
        with c_left_btn:
            if st.button("🚀 Build Your Resume", key="btn_build_resume", use_container_width=True):
                st.session_state.current_view = 'scorer'
                st.rerun()

        with c_right_btn:
            if st.button("📈 Get Your Resume Score", key="btn_get_score", use_container_width=True):
                st.session_state.current_view = 'scorer'
                st.rerun()

    with col_preview:
        user_svg = get_svg_icon("user", size=30, color="#FFFFFF")
        check_circle_svg = get_svg_icon("check-circle", size=26, color="#4F46E5")

        preview_html = textwrap.dedent(f"""
<div class="resume-mock-wrapper">
<div class="resume-mock-card">
<div class="resume-mock-topbar"></div>
<div class="floating-check-badge">
{check_circle_svg}
</div>
<div class="floating-score-badge">
<span class="floating-score-val">92</span>
<span class="floating-score-lbl">ATS SCORE</span>
</div>
<div class="resume-header-row">
<div class="resume-avatar">
{user_svg}
</div>
<div>
<div class="resume-name">John Doe</div>
<div class="resume-title">Senior Software Engineer</div>
</div>
</div>
<div class="resume-divider"></div>
<div class="resume-section-label">EXPERIENCE</div>
<div class="resume-timeline">
<div class="timeline-entry">
<div class="timeline-dot"></div>
<div>
<span class="timeline-role">Senior Software Engineer</span>
<span class="timeline-company">at Tech Corp</span>
</div>
<div class="timeline-desc">
Led development of AI-powered features that improved user engagement by 40%. Architected scalable microservices serving 1M+ users.
</div>
</div>
<div class="timeline-entry" style="margin-bottom:0;">
<div class="timeline-dot timeline-dot-gray"></div>
<div>
<span class="timeline-role">Software Engineer</span>
<span class="timeline-company" style="color:#475569;">at Startup Inc</span>
</div>
<div class="timeline-desc">
Built scalable backend systems using Python and AWS. Reduced latency by 200ms across all endpoints.
</div>
</div>
</div>
<div class="resume-section-label" style="margin-top:18px;">SKILLS</div>
<div class="resume-chips-row">
<span class="resume-skill-chip">Python</span>
<span class="resume-skill-chip">React</span>
<span class="resume-skill-chip">AWS</span>
<span class="resume-skill-chip">ML</span>
<span class="resume-skill-chip">Docker</span>
</div>
</div>
</div>
""").strip()
        st.markdown(preview_html, unsafe_allow_html=True)

    st.markdown("<div style='height: 80px;'></div>", unsafe_allow_html=True)

    # "How It Works" Section
    how_it_works_head = textwrap.dedent("""
<div class="section-center-head">
<div class="section-eyebrow">WORKFLOW</div>
<h2 class="section-big-title">How It Works</h2>
</div>
""").strip()
    st.markdown(how_it_works_head, unsafe_allow_html=True)

    hw_col1, hw_col2, hw_col3 = st.columns(3)
    with hw_col1:
        upload_icon = get_svg_icon("upload-cloud", size=24, color="#4F46E5")
        hw1_html = textwrap.dedent(f"""
<div class="step-card-modern">
<div class="step-card-icon-tile">{upload_icon}</div>
<div class="step-card-num">STEP 1</div>
<div class="step-card-title">Upload Resume</div>
<p class="step-card-desc">Provide your existing resume in PDF, DOC, or DOCX format. We parse your content directly in your browser session.</p>
</div>
""").strip()
        st.markdown(hw1_html, unsafe_allow_html=True)

    with hw_col2:
        cpu_icon = get_svg_icon("cpu", size=24, color="#4F46E5")
        hw2_html = textwrap.dedent(f"""
<div class="step-card-modern">
<div class="step-card-icon-tile">{cpu_icon}</div>
<div class="step-card-num">STEP 2</div>
<div class="step-card-title">Analyze Match</div>
<p class="step-card-desc">Compare your resume against our multi-vector ATS scoring engine or a targeted job description to detect missing skills.</p>
</div>
""").strip()
        st.markdown(hw2_html, unsafe_allow_html=True)

    with hw_col3:
        sparkles_icon = get_svg_icon("sparkles", size=24, color="#4F46E5")
        hw3_html = textwrap.dedent(f"""
<div class="step-card-modern">
<div class="step-card-icon-tile">{sparkles_icon}</div>
<div class="step-card-num">STEP 3</div>
<div class="step-card-title">Improve & Land</div>
<p class="step-card-desc">Receive prioritized action items, keyword gap chips, and diagnostic recommendations to maximize interview callbacks.</p>
</div>
""").strip()
        st.markdown(hw3_html, unsafe_allow_html=True)

    st.markdown("<div style='height: 70px;'></div>", unsafe_allow_html=True)

    # Scoring Features Grid (5 Cards)
    features_head = textwrap.dedent("""
<div class="section-center-head">
<div class="section-eyebrow">EVALUATION METRICS</div>
<h2 class="section-big-title">The 5 ATS Scoring Dimensions</h2>
</div>
""").strip()
    st.markdown(features_head, unsafe_allow_html=True)

    g1, g2, g3 = st.columns(3)
    with g1:
        f_icon = get_svg_icon("layout", size=22, color="#4F46E5")
        st.markdown(textwrap.dedent(f"""
<div class="feature-card-modern">
<div class="feature-head-row">
<div class="feature-icon-tile">{f_icon}</div>
<span class="weight-pill">20 pts</span>
</div>
<div class="feature-title">Formatting</div>
<p class="feature-desc">Audits layout hierarchy, font consistency, section headers, and machine-parseable text streams.</p>
</div>
""").strip(), unsafe_allow_html=True)

    with g2:
        f_icon = get_svg_icon("key", size=22, color="#4F46E5")
        st.markdown(textwrap.dedent(f"""
<div class="feature-card-modern">
<div class="feature-head-row">
<div class="feature-icon-tile">{f_icon}</div>
<span class="weight-pill">25 pts</span>
</div>
<div class="feature-title">Keywords & Skills</div>
<p class="feature-desc">Scans for industry terminology, tech stack keywords, and density alignment with target job criteria.</p>
</div>
""").strip(), unsafe_allow_html=True)

    with g3:
        f_icon = get_svg_icon("file-text", size=22, color="#4F46E5")
        st.markdown(textwrap.dedent(f"""
<div class="feature-card-modern">
<div class="feature-head-row">
<div class="feature-icon-tile">{f_icon}</div>
<span class="weight-pill">25 pts</span>
</div>
<div class="feature-title">Content Quality</div>
<p class="feature-desc">Evaluates strong action verbs, quantified accomplishments, metric specificity, and bullet structure.</p>
</div>
""").strip(), unsafe_allow_html=True)

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

    g4, g5 = st.columns(2)
    with g4:
        f_icon = get_svg_icon("check-circle", size=22, color="#4F46E5")
        st.markdown(textwrap.dedent(f"""
<div class="feature-card-modern">
<div class="feature-head-row">
<div class="feature-icon-tile">{f_icon}</div>
<span class="weight-pill">15 pts</span>
</div>
<div class="feature-title">Skill Validation</div>
<p class="feature-desc">Semantically verifies that claimed competencies are supported by tangible evidence in your experience.</p>
</div>
""").strip(), unsafe_allow_html=True)

    with g5:
        f_icon = get_svg_icon("cpu", size=22, color="#4F46E5")
        st.markdown(textwrap.dedent(f"""
<div class="feature-card-modern">
<div class="feature-head-row">
<div class="feature-icon-tile">{f_icon}</div>
<span class="weight-pill">15 pts</span>
</div>
<div class="feature-title">ATS Compatibility</div>
<p class="feature-desc">Detects tables, multi-column blocks, non-standard symbols, and layout flaws that cause parsing rejection.</p>
</div>
""").strip(), unsafe_allow_html=True)

    # Final CTA Band
    cta_band_html = textwrap.dedent("""
<div class="cta-band">
<h2>Ready to beat the ATS?</h2>
<p>Get instant institutional-grade diagnostic feedback on your resume today.</p>
</div>
""").strip()
    st.markdown(cta_band_html, unsafe_allow_html=True)

    _, cta_b_col, _ = st.columns([1, 1.2, 1])
    with cta_b_col:
        if st.button("Get Your Resume Score", key="cta_band_btn", use_container_width=True):
            st.session_state.current_view = 'scorer'
            st.rerun()

    # Slim Footer
    target_icon = get_svg_icon("target", size=18, color="#2563EB")
    footer_html = textwrap.dedent(f"""
<div class="slim-footer">
<div style="display:flex; align-items:center; gap:8px;">
{target_icon}
<span style="font-weight:700; color:#0F172A;">ATS Analyzer</span>
<span>&bull; Intelligent Local Resume Scoring</span>
</div>
<div>
&copy; 2026 ATS Analyzer. All data stays private on your machine.
</div>
</div>
""").strip()
    st.markdown(footer_html, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
