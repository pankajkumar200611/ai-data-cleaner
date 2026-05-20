import streamlit as st
import streamlit.components.v1 as components
import json

def load_lottieurl(url: str):
    import requests
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def inject_global_js():
    """Injects mouse-follow glow effect tracking."""
    js_code = """
    <script>
    document.addEventListener('mousemove', e => {
        document.documentElement.style.setProperty('--mouse-x', e.clientX + 'px');
        document.documentElement.style.setProperty('--mouse-y', e.clientY + 'px');
    });
    </script>
    <div id="glow-layer"></div>
    """
    components.html(js_code, height=0, width=0)

def render_navbar():
    """Renders the top sticky navbar."""
    navbar_html = """
    <div class="premium-navbar">
        <div class="navbar-brand">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="#00f3ff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M2 17L12 22L22 17" stroke="#b026ff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M2 12L12 17L22 12" stroke="#00f3ff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <span>DataCleaner AI</span>
        </div>
        <div class="navbar-links">
            <div class="navbar-link">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>
            </div>
        </div>
    </div>
    """
    st.markdown(navbar_html, unsafe_allow_html=True)

def render_kpi_card(title, value, trend="+0%", color="#00f3ff"):
    """Renders a premium KPI card."""
    html = f"""
    <div class="glass-card" style="padding: 20px; position: relative;">
        <div style="color: #a0aabf; font-size: 0.9rem; font-weight: 500; font-family: 'Poppins', sans-serif;">{title}</div>
        <div style="font-size: 2.2rem; font-weight: 700; color: #fff; margin: 10px 0;">{value}</div>
        <div style="color: {color}; font-size: 0.8rem; display: flex; align-items: center; gap: 5px;">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="22 7 13.5 15.5 8.5 10.5 2 17"></polyline><polyline points="16 7 22 7 22 13"></polyline></svg>
            {trend} from last run
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
