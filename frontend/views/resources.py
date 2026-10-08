import textwrap
import streamlit as st

from frontend.components._helpers import get_svg_icon


def render():
    st.markdown('<div class="content-wrapper">', unsafe_allow_html=True)

    header_html = textwrap.dedent("""
<div style="text-align:center; margin-bottom: 40px;">
<h1 style="font-size:36px; font-weight:800; color:#0F172A; margin-bottom:8px !important;">ATS Resources & Guidelines</h1>
<p style="font-size:16px; color:#64748B; max-width:600px; margin:0 auto;">
Proven best practices, parsing mechanics, and high-frequency industry keywords to help you sail past automated filters.
</p>
</div>
""").strip()
    st.markdown(header_html, unsafe_allow_html=True)

    # 3-Column Resource Card Grid
    st.markdown("### Core Optimization Guides")
    col1, col2, col3 = st.columns(3)

    with col1:
        layout_icon = get_svg_icon("layout", size=22, color="#4F46E5")
        st.markdown(textwrap.dedent(f"""
<div class="step-card-modern">
<div class="step-card-icon-tile">{layout_icon}</div>
<div class="step-card-title">ATS Layout Anatomy</div>
<p class="step-card-desc">
Learn why multi-column layouts, tables, and floating text boxes cause parsing failures, and how single-column designs achieve 100% text extraction.
</p>
</div>
""").strip(), unsafe_allow_html=True)
        if st.button("Read Layout Guide", key="guide_layout", use_container_width=True):
            st.toast("Layout Guide: Stick to single-column, standard headings, and PDF/DOCX formats.")

    with col2:
        key_icon = get_svg_icon("key", size=22, color="#4F46E5")
        st.markdown(textwrap.dedent(f"""
<div class="step-card-modern">
<div class="step-card-icon-tile">{key_icon}</div>
<div class="step-card-title">Keyword Density Strategy</div>
<p class="step-card-desc">
Discover how to weave required skills naturally into accomplishment bullets without triggering algorithmic keyword stuffing penalties.
</p>
</div>
""").strip(), unsafe_allow_html=True)
        if st.button("Read Keyword Guide", key="guide_keyword", use_container_width=True):
            st.toast("Keyword Guide: Mirror the job description terms in your project bullets.")

    with col3:
        check_icon = get_svg_icon("check-circle", size=22, color="#4F46E5")
        st.markdown(textwrap.dedent(f"""
<div class="step-card-modern">
<div class="step-card-icon-tile">{check_icon}</div>
<div class="step-card-title">Action Verb Matrix</div>
<p class="step-card-desc">
Replace passive language with high-impact action verbs (Architected, Spearheaded, Accelerated) paired with quantified metrics.
</p>
</div>
""").strip(), unsafe_allow_html=True)
        if st.button("Read Verb Matrix", key="guide_verbs", use_container_width=True):
            st.toast("Action Verb Guide: Quantify achievements with dollar amounts, %, or user metrics.")

    st.markdown("<div style='height: 48px;'></div>", unsafe_allow_html=True)

    # Do's and Don'ts Cards
    st.markdown("### ATS Do's and Don'ts")
    col_do, col_dont = st.columns(2)

    icon_check = get_svg_icon("check", size=16, color="#166534")
    icon_x = get_svg_icon("x", size=16, color="#9F1239")

    with col_do:
        st.markdown(textwrap.dedent(f"""
<div style="background:#FFFFFF; border:1px solid #E2E8F0; border-top:4px solid #16A34A; border-radius:16px; padding:24px; box-shadow:0 8px 24px rgba(15,23,42,0.04); height:100%;">
<div style="display:flex; align-items:center; gap:8px; margin-bottom:16px;">
<div style="background:#DCFCE7; width:28px; height:28px; border-radius:50%; display:flex; align-items:center; justify-content:center;">
{icon_check}
</div>
<strong style="color:#166534; font-size:17px;">Recommended Best Practices</strong>
</div>
<ul style="color:#334155; font-size:14px; line-height:1.7; padding-left:20px; margin:0;">
<li><strong>Standard Section Headings:</strong> Work Experience, Education, Skills, Projects.</li>
<li><strong>Contextual Keyword Evidence:</strong> Demonstrate skills in bullet accomplishment points.</li>
<li><strong>Quantified Impact:</strong> Always pair actions with numbers, percentages, or scale.</li>
<li><strong>Standard Fonts:</strong> Inter, Arial, Calibri, or Roboto for universal OCR parsing.</li>
<li><strong>PDF or DOCX Export:</strong> Keep text selectable and copyable.</li>
</ul>
</div>
""").strip(), unsafe_allow_html=True)

    with col_dont:
        st.markdown(textwrap.dedent(f"""
<div style="background:#FFFFFF; border:1px solid #E2E8F0; border-top:4px solid #EF4444; border-radius:16px; padding:24px; box-shadow:0 8px 24px rgba(15,23,42,0.04); height:100%;">
<div style="display:flex; align-items:center; gap:8px; margin-bottom:16px;">
<div style="background:#FFE4E6; width:28px; height:28px; border-radius:50%; display:flex; align-items:center; justify-content:center;">
{icon_x}
</div>
<strong style="color:#9F1239; font-size:17px;">Critical Pitfalls to Avoid</strong>
</div>
<ul style="color:#334155; font-size:14px; line-height:1.7; padding-left:20px; margin:0;">
<li><strong>Tables and Multi-Columns:</strong> Scrambles reading order in older ATS engines.</li>
<li><strong>Header/Footer Placement:</strong> Crucial contact details in headers are often missed.</li>
<li><strong>Graphics, Icons, or Photos:</strong> Non-text media bloats file size and triggers errors.</li>
<li><strong>Unexpanded Acronyms:</strong> Always write the full name first followed by acronym.</li>
<li><strong>Keyword Stuffing:</strong> Hidden white text or keyword dumps result in blacklisting.</li>
</ul>
</div>
""").strip(), unsafe_allow_html=True)

    st.markdown("<div style='height: 48px;'></div>", unsafe_allow_html=True)

    # High-Frequency Keywords by Domain
    st.markdown("### Top Keywords by Industry Domain")

    tab1, tab2, tab3 = st.tabs(["Engineering & Tech", "Product & Business", "Design & UX"])

    with tab1:
        st.markdown(textwrap.dedent("""
<div style="display:flex; flex-wrap:wrap; gap:8px; margin-top:12px;">
<span class="resume-skill-chip">Python</span>
<span class="resume-skill-chip">FastAPI</span>
<span class="resume-skill-chip">TypeScript</span>
<span class="resume-skill-chip">React</span>
<span class="resume-skill-chip">Docker</span>
<span class="resume-skill-chip">Kubernetes</span>
<span class="resume-skill-chip">AWS</span>
<span class="resume-skill-chip">PostgreSQL</span>
<span class="resume-skill-chip">Microservices</span>
<span class="resume-skill-chip">CI/CD</span>
<span class="resume-skill-chip">Distributed Systems</span>
<span class="resume-skill-chip">REST APIs</span>
</div>
""").strip(), unsafe_allow_html=True)

    with tab2:
        st.markdown(textwrap.dedent("""
<div style="display:flex; flex-wrap:wrap; gap:8px; margin-top:12px;">
<span class="resume-skill-chip">Product Strategy</span>
<span class="resume-skill-chip">Cross-Functional Leadership</span>
<span class="resume-skill-chip">Agile / Scrum</span>
<span class="resume-skill-chip">KPI Definition</span>
<span class="resume-skill-chip">Stakeholder Management</span>
<span class="resume-skill-chip">Go-to-Market (GTM)</span>
<span class="resume-skill-chip">User Research</span>
<span class="resume-skill-chip">A/B Testing</span>
<span class="resume-skill-chip">Roadmap Planning</span>
</div>
""").strip(), unsafe_allow_html=True)

    with tab3:
        st.markdown(textwrap.dedent("""
<div style="display:flex; flex-wrap:wrap; gap:8px; margin-top:12px;">
<span class="resume-skill-chip">Design Systems</span>
<span class="resume-skill-chip">Figma Prototyping</span>
<span class="resume-skill-chip">Information Architecture</span>
<span class="resume-skill-chip">User Flows</span>
<span class="resume-skill-chip">Accessibility (WCAG)</span>
<span class="resume-skill-chip">Interaction Design</span>
<span class="resume-skill-chip">Usability Testing</span>
<span class="resume-skill-chip">Design Tokens</span>
</div>
""").strip(), unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
