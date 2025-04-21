import streamlit as st
import pandas as pd
import os

#st.set_page_config(page_title='Journal Ratings', page_icon='📚', layout='wide')
st.set_page_config("Journal Ratings Finder",
    "favicon.ico")

# Cargar usuarios autorizados desde Secrets
AUTHORIZED_USERS = [
    os.getenv("USER1"),
    os.getenv("USER2"),
    os.getenv("USER3"),
    os.getenv("USER4"),
    os.getenv("USER5"),
    os.getenv("USER6"),
    os.getenv("USER7"),
    os.getenv("USER8"),
    os.getenv("USER9"),
    os.getenv("USER10"),
    os.getenv("USER11"),
    os.getenv("USER12"),
    os.getenv("USER13"),
    os.getenv("USER14"),
    os.getenv("USER15"),
    os.getenv("USER16"),
    os.getenv("USER17"),
    os.getenv("USER18"),
    os.getenv("USER19"),
    os.getenv("USER20"),
    os.getenv("USER21"),
]
AUTHORIZED_USERS = [u for u in AUTHORIZED_USERS if u]

# Inicializar el estado de sesión
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

# --- LOGIN UI ---
if not st.session_state['authenticated']:
    st.markdown(
        """
        <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
        </style>
        """,
        unsafe_allow_html=True
    )
    st.title("🔐 Login Required")
    with st.form("login_form"):
        email = st.text_input("Email")
        #password = st.text_input("Password", type="password", key="user_password", autocomplete="current-password") # Added autocomplete
        password = st.text_input("Password", type="password", autocomplete="current-password")
        #login_button = st.button("Login")
        submit = st.form_submit_button("Login")

    if submit: #login_button:
        #credential = f"{email}:{password}"
        credential = f"{email.lower()}:{password}"
        if credential in AUTHORIZED_USERS:
            st.session_state['authenticated'] = True
            st.rerun()
        else:
            st.error("Invalid email or password")
    st.stop()

# --- LOGOUT BUTTON ---
with st.sidebar:
    if st.button("Logout"):
        st.session_state['authenticated'] = False
        st.rerun()

# --- APP CONTENT STARTS HERE ---

import streamlit as st
import pandas as pd

# Page config with favicon
#    page_title="Journal Ratings Finder",
#    page_icon="favicon.ico"
#)
 
# Custom CSS for layout and mobile optimizations
custom_css = """
    <style>
    #MainMenu, header, footer {
        visibility: hidden;
    }

    .block-container:has(> footer) {
        padding-bottom: 0 !important;
    }

    .scroll-container {
        overflow-x: auto;
    }

    @media only screen and (max-width: 768px) {
        .main .block-container {
            padding-top: 0.5rem !important;
        }
    }
    </style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    #df = pd.read_excel("Journals.xlsx")
    path = "Journals.xlsx"
    #st.write(f"Intentando abrir: {path}") 
    df = pd.read_excel(path)
    df["Normalized_Title"] = df["Revista"].str.lower().str.strip()
    return df

df = load_data()
unique_titles = df["Revista"].sort_values().unique()

st.title("Academic Journal Ratings Finder")

with st.expander("Journal ratings from five major sources", expanded=True):
    st.markdown("""
    For each origin, the ratings are shown in descending order (best to worst):

    - **AJG**: 4*, 4, 3, 2, 1  
    - **CNRS**: 1*, 1, 2, 3, 4  
    - **CNU**: A, B, C  
    - **VHB**: A+, A, B, C, D  
    - **ABDC**: A*, A, B, C
    """)

# Multiselect input
selected_journals = st.multiselect(
    "Select one or more journal titles:",
    options=unique_titles,
    help="Start typing to filter the list. You can select multiple journals."
)

if selected_journals:
    normalized_selection = [j.lower().strip() for j in selected_journals]
    results = df[df["Normalized_Title"].isin(normalized_selection)]
    
    if not results.empty:
        pivot = results.pivot_table(index="Revista", columns="Origen", values="Rating", aggfunc="first").reset_index()

        # Ensure all columns are present
        full_columns = ["Revista", "AJG", "CNRS", "CNU", "VHB", "ABDC"]
        for col in full_columns:
            if col not in pivot.columns:
                pivot[col] = ""

        pivot = pivot[full_columns]

        # Add scrollable container
        #st.markdown('<div class="scroll-container">', unsafe_allow_html=True)
        #st.dataframe(pivot, use_container_width=True, hide_index=True)
        #st.markdown('</div>', unsafe_allow_html=True)

        # Renombrar la columna 'Revista' a 'Journal'
        pivot = pivot.rename(columns={"Revista": "Journal"})

        def render_html_table(df):
            header = (
                "<thead><tr>"
                "<th>Journal</th>"
                "<th>AJG<br><span style='font-size: 0.75em;'>4*, 4, 3, 2, 1</span></th>"
                "<th>CNRS<br><span style='font-size: 0.75em;'>1*, 1, 2, 3, 4</span></th>"
                "<th>CNU<br><span style='font-size: 0.75em;'>A, B, C</span></th>"
                "<th>VHB<br><span style='font-size: 0.75em;'>A+, A, B, C, D</span></th>"
                "<th>ABDC<br><span style='font-size: 0.75em;'>A*, A, B, C</span></th>"
                "</tr></thead>"
            )

            body_rows = []
            for _, row in df.iterrows():
                body_rows.append(
                    f"<tr>"
                    f"<td>{row['Journal']}</td>"
                    f"<td>{row['AJG']}</td>"
                    f"<td>{row['CNRS']}</td>"
                    f"<td>{row['CNU']}</td>"
                    f"<td>{row['VHB']}</td>"
                    f"<td>{row['ABDC']}</td>"
                    f"</tr>"
                )
            body = "<tbody>" + "".join(body_rows) + "</tbody>"

            table_html = (
                "<table style='width: 100%; border-collapse: collapse; text-align: center;' border='1'>"
                f"{header}{body}"
                "</table>"
            )

            return table_html

        # ✅ Esta es la única línea que debe generar salida
        pivot = pivot.fillna("")
        st.markdown(render_html_table(pivot), unsafe_allow_html=True)


        # Descarga como CSV (igual que antes)
        csv = pivot.to_csv(index=False).encode('utf-8')
        st.download_button("Download results as CSV", csv, "journal_ratings_results.csv", "text/csv")


  
    else:
        st.warning("No matches found.")