import streamlit as st
import pandas as pd
import time
from streamlit_lottie import st_lottie
from utils.data_cleaner import (get_dataset_stats, remove_duplicates, handle_missing_values, 
                                correct_datatypes, normalize_numeric_data, remove_outliers, 
                                encode_categorical_data)
from utils.visualizations import (plot_missing_heatmap, plot_datatype_pie, 
                                  plot_null_percentage, plot_correlation_matrix)
from utils.ai_assistant import process_query
from utils.ui_components import load_lottieurl, inject_global_js, render_navbar, render_kpi_card

# Page config MUST be the first Streamlit command
st.set_page_config(page_title="DataCleaner AI", page_icon="✨", layout="wide", initial_sidebar_state="collapsed")

# Load custom CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

try:
    local_css("style.css")
except FileNotFoundError:
    pass

# Inject Custom JS & Navbar
# inject_global_js()
render_navbar()

# Sidebar removed as requested
st.session_state.gemini_key = None

# Lottie Animations (using public Lottie JSON URLs)
lottie_ai = load_lottieurl("https://lottie.host/80a2ba1a-3e5e-4c70-96f7-b2eb6e0689b1/XN0M3fWQqT.json")

# ----------------- Hero Section -----------------
st.markdown("<br><br>", unsafe_allow_html=True)
col_hero1, col_hero2, col_hero3 = st.columns([1, 6, 1])
with col_hero2:
    st.markdown("<h1 class='hero-title'>DataCleaner AI</h1>", unsafe_allow_html=True)
    st.markdown("<p class='hero-subtitle'>Transform messy datasets into AI-ready structured data instantly.</p>", unsafe_allow_html=True)

    # Hero Buttons (Removed)

# ----------------- File Upload -----------------
st.markdown("<br>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("Drop your messy CSV here", type=["csv"])

if uploaded_file is not None:
    if 'original_df' not in st.session_state or st.session_state.uploaded_filename != uploaded_file.name:
        df = pd.read_csv(uploaded_file)
        st.session_state.original_df = df.copy()
        st.session_state.cleaned_df = df.copy()
        st.session_state.uploaded_filename = uploaded_file.name
        st.session_state.chat_history = [{"role": "assistant", "content": "Hello! I'm your AI Data Analyst. Ask me anything about this dataset."}]
        
    orig_df = st.session_state.original_df
    cleaned_df = st.session_state.cleaned_df
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # ----------------- Dashboard Layout -----------------
    st.markdown("<h3 style='font-family: Poppins; color: #fff;'>Dataset Overview</h3>", unsafe_allow_html=True)
    stats = get_dataset_stats(cleaned_df)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_kpi_card("Missing Values", stats['missing_values'], trend="-5%", color="#ff4757")
    with col2:
        render_kpi_card("Duplicate Rows", stats['duplicate_rows'], trend="-12%", color="#ff4757")
    with col3:
        render_kpi_card("Total Columns", stats['total_cols'], trend="0%", color="#00f3ff")
    with col4:
        render_kpi_card("Total Rows", stats['total_rows'], trend="+15%", color="#00f3ff")
        
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # ----------------- Functional Navbar (Tabs) -----------------
    st.markdown("<style>.stTabs [data-baseweb='tab-list'] { gap: 24px; } .stTabs [data-baseweb='tab'] { height: 50px; white-space: pre-wrap; background-color: rgba(20, 20, 25, 0.4); border-radius: 10px 10px 0 0; padding: 10px 20px; }</style>", unsafe_allow_html=True)
    tab_cleaning, tab_analytics, tab_ai = st.tabs(["🛠️ Data Cleaning", "📊 Analytics", "🤖 AI Assistant"])

    with tab_cleaning:
        # ----------------- Main Interface -----------------
        left_panel, right_panel = st.columns([1.2, 2])
    
        with left_panel:
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.markdown("<h4 style='color: #00f3ff; margin-bottom: 20px;'>🛠️ AI Cleaning Pipeline</h4>", unsafe_allow_html=True)
        
            # Options
            opt_drop_nulls = st.checkbox("Handle Missing Values (Mean/Mode)")
            opt_drop_dupes = st.checkbox("Remove Duplicates")
            opt_auto_types = st.checkbox("Auto Datatype Correction")
            opt_normalize = st.checkbox("Normalize Numeric Data")
            opt_outliers = st.checkbox("Remove Outliers (Z-score > 3)")
            opt_encode = st.checkbox("Encode Categorical Data")
        
            st.markdown("<br>", unsafe_allow_html=True)
        
            st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
            run_ai = st.button("Run AI Cleaning ⚡")
            st.markdown('</div>', unsafe_allow_html=True)
        
            log_placeholder = st.empty()
        
            if run_ai:
                temp_df = orig_df.copy()
            
                # Live logs animation
                logs = ["Initializing AI pipeline...", "Analyzing datatypes...", "Detecting anomalies..."]
                for log in logs:
                    log_placeholder.markdown(f"<code style='color: #a0aabf; font-size: 0.8rem;'>{log}</code>", unsafe_allow_html=True)
                    time.sleep(0.5)
                
                if opt_auto_types: 
                    log_placeholder.markdown("<code style='color: #00f3ff; font-size: 0.8rem;'>Correcting datatypes...</code>", unsafe_allow_html=True)
                    temp_df = correct_datatypes(temp_df)
                    time.sleep(0.4)
                if opt_drop_nulls: 
                    log_placeholder.markdown("<code style='color: #00f3ff; font-size: 0.8rem;'>Imputing missing values...</code>", unsafe_allow_html=True)
                    temp_df = handle_missing_values(temp_df, strategy='mean')
                    time.sleep(0.4)
                if opt_drop_dupes: 
                    log_placeholder.markdown("<code style='color: #00f3ff; font-size: 0.8rem;'>Removing duplicates...</code>", unsafe_allow_html=True)
                    temp_df = remove_duplicates(temp_df)
                    time.sleep(0.4)
                if opt_outliers: 
                    log_placeholder.markdown("<code style='color: #00f3ff; font-size: 0.8rem;'>Filtering outliers...</code>", unsafe_allow_html=True)
                    temp_df = remove_outliers(temp_df)
                    time.sleep(0.4)
                if opt_encode: 
                    log_placeholder.markdown("<code style='color: #00f3ff; font-size: 0.8rem;'>Encoding categoricals...</code>", unsafe_allow_html=True)
                    temp_df = encode_categorical_data(temp_df)
                    time.sleep(0.4)
                if opt_normalize: 
                    log_placeholder.markdown("<code style='color: #00f3ff; font-size: 0.8rem;'>Normalizing numerical features...</code>", unsafe_allow_html=True)
                    temp_df = normalize_numeric_data(temp_df)
                    time.sleep(0.4)
                
                log_placeholder.markdown("<code style='color: #00ff7f; font-size: 0.8rem;'>Pipeline completed successfully. ✓</code>", unsafe_allow_html=True)
                st.session_state.cleaned_df = temp_df
                time.sleep(0.5)
                st.rerun()
            
            st.markdown("</div>", unsafe_allow_html=True)
        
            st.markdown("<br>", unsafe_allow_html=True)
        
            # Export section
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.markdown("<h4 style='color: #b026ff; margin-bottom: 20px;'>💾 Export Artifacts</h4>", unsafe_allow_html=True)
            csv = cleaned_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Clean CSV",
                data=csv,
                file_name="cleaned_dataset.csv",
                mime="text/csv",
            )
            st.button("Export JSON Pipeline", key="export_json")
            st.markdown("</div>", unsafe_allow_html=True)
        
        with right_panel:
            st.markdown("<div class='panel-right'>", unsafe_allow_html=True)
            st.markdown("<h3 style='font-family: Poppins; color: #fff;'>Data Preview</h3>", unsafe_allow_html=True)
        
            tab1, tab2 = st.tabs(["Original Dataset", "Cleaned Dataset"])
            with tab1:
                st.markdown("<div class='panel-left'>", unsafe_allow_html=True)
                st.dataframe(orig_df.head(50), use_container_width=True, height=400)
                st.markdown("</div>", unsafe_allow_html=True)
            
            with tab2:
                st.dataframe(cleaned_df.head(50), use_container_width=True, height=400)
            
                # Data Quality Ring (Simulated with progress)
                quality_score = 100 - (stats['missing_values'] / (stats['total_rows'] * stats['total_cols'] + 1)) * 50 - (stats['duplicate_rows'] / (stats['total_rows'] + 1)) * 50
                quality_score = max(0, min(100, quality_score))
            
                st.markdown(f"""
                <div style="margin-top: 20px; display: flex; align-items: center; gap: 20px;">
                    <div style="width: 60px; height: 60px; border-radius: 50%; background: conic-gradient(#00f3ff {quality_score}%, transparent 0); display: flex; align-items: center; justify-content: center; position: relative;">
                        <div style="width: 50px; height: 50px; border-radius: 50%; background: #0a0a0f; position: absolute;"></div>
                        <span style="position: relative; color: #fff; font-weight: 700; font-size: 0.9rem;">{int(quality_score)}</span>
                    </div>
                    <div>
                        <h5 style="margin: 0; color: #fff;">Data Quality Score</h5>
                        <p style="margin: 0; color: #a0aabf; font-size: 0.9rem;">Dataset is ready for machine learning models.</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<br><br><br>", unsafe_allow_html=True)
    

    with tab_analytics:
        # ----------------- Visual Analytics -----------------
        st.markdown("<h3 style='font-family: Poppins; color: #fff;'>Interactive Analytics</h3>", unsafe_allow_html=True)
        vcol1, vcol2 = st.columns(2)
    
        with vcol1:
            st.plotly_chart(plot_missing_heatmap(cleaned_df), use_container_width=True)
            st.plotly_chart(plot_null_percentage(cleaned_df), use_container_width=True)
        
        with vcol2:
            st.plotly_chart(plot_datatype_pie(cleaned_df), use_container_width=True)
            st.plotly_chart(plot_correlation_matrix(cleaned_df), use_container_width=True)

        st.markdown("<br><br><br>", unsafe_allow_html=True)


    with tab_ai:
        # ----------------- AI Assistant -----------------
        acol1, acol2, acol3 = st.columns([1, 2, 1])
        with acol2:
            st.markdown("<h3 style='font-family: Poppins; color: #fff; text-align: center;'>Ask AI About Your Dataset</h3>", unsafe_allow_html=True)
        
            # Display chat messages
            for message in st.session_state.chat_history:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
                
            # Smart suggestions
            scol1, scol2, scol3 = st.columns(3)
            with scol1:
                if st.button("Which columns have nulls?"):
                    st.session_state.chat_prompt = "Which columns have nulls?"
            with scol2:
                if st.button("Suggest preprocessing"):
                    st.session_state.chat_prompt = "Suggest preprocessing steps"
            with scol3:
                if st.button("Count duplicates"):
                    st.session_state.chat_prompt = "How many duplicate rows?"
                
            # Chat input
            prompt = st.chat_input("Ask anything about your dataset...")
        
            if getattr(st.session_state, 'chat_prompt', None):
                prompt = st.session_state.chat_prompt
                st.session_state.chat_prompt = None
            
            if prompt:
                st.session_state.chat_history.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.markdown(prompt)
                
                with st.spinner("AI is thinking..."):
                    time.sleep(1)
                    response = process_query(prompt, cleaned_df, st.session_state.gemini_key)
                
                st.session_state.chat_history.append({"role": "assistant", "content": response})
                with st.chat_message("assistant"):
                    st.markdown(response)

else:
    # Empty state placeholder
    st.markdown("<br><br>", unsafe_allow_html=True)
    if lottie_ai:
        with st.columns([1, 1, 1])[1]:
            st_lottie(lottie_ai, height=300, key="ai_lottie")
    
    st.markdown("""
        <div style="display:flex; justify-content:center;">
            <div class="glass-card" style="width: 100%; max-width: 600px; text-align: center;">
                <h3 style="color: #fff;">Upload a dataset to begin</h3>
                <p style="color: #a0aabf;">Your data is processed locally and securely via our premium pipeline.</p>
                <div style="margin-top:30px; display: flex; justify-content: center; gap: 10px;">
                    <span style="display:inline-block; width: 8px; height: 8px; background:#00f3ff; border-radius:50%; box-shadow: 0 0 10px #00f3ff;"></span>
                    <span style="display:inline-block; width: 8px; height: 8px; background:#b026ff; border-radius:50%; box-shadow: 0 0 10px #b026ff;"></span>
                    <span style="display:inline-block; width: 8px; height: 8px; background:#00f3ff; border-radius:50%; box-shadow: 0 0 10px #00f3ff;"></span>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
