with open("app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
in_tab = False

tabs_code = """    # ----------------- Functional Navbar (Tabs) -----------------
    st.markdown("<style>.stTabs [data-baseweb='tab-list'] { gap: 24px; } .stTabs [data-baseweb='tab'] { height: 50px; white-space: pre-wrap; background-color: rgba(20, 20, 25, 0.4); border-radius: 10px 10px 0 0; padding: 10px 20px; }</style>", unsafe_allow_html=True)
    tab_cleaning, tab_analytics, tab_ai = st.tabs(["🛠️ Data Cleaning", "📊 Analytics", "🤖 AI Assistant"])
"""

for i, line in enumerate(lines):
    if line.strip() == "# ----------------- Main Interface -----------------":
        new_lines.append(tabs_code)
        new_lines.append("\n    with tab_cleaning:\n")
        in_tab = True
        
    elif line.strip() == "# ----------------- Visual Analytics -----------------":
        new_lines.append("\n    with tab_analytics:\n")
        in_tab = True
        
    elif line.strip() == "# ----------------- AI Assistant -----------------":
        new_lines.append("\n    with tab_ai:\n")
        in_tab = True
        
    elif line.strip() == "else:":
        in_tab = False

    if in_tab:
        if line.strip() == "":
            new_lines.append(line)
        else:
            new_lines.append("    " + line)
    else:
        new_lines.append(line)

with open("app.py", "w", encoding="utf-8") as f:
    f.writelines(new_lines)
