import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster

st.set_page_config(
    page_title="IDF Coworking Hub",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .stMetric {
        background-color: #1e2130;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #00d4ff;
    }
    div.stButton > button:first-child {
        background-color: #00d4ff;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data():
    try:
        df = pd.read_csv("coworking_ready.csv")
        df['Emails_Officiels'] = df['Emails_Officiels'].fillna("Contact via site web")
        df['Departement'] = df['Departement'].astype(str).str.replace('.0', '', regex=False)
        return df
    except Exception as e:
        st.error(f"Erreur de chargement des données : {e}")
        return None

df = load_data()

if df is not None:
    st.sidebar.image("https://img.icons8.com/clouds/100/000000/google-maps.png", width=80)
    st.sidebar.title("Filtres avancés")
    
    st.sidebar.markdown("---")
    
    search_query = st.sidebar.text_input("Rechercher un espace", placeholder="Nom, ville...")
    
    available_deps = sorted(df['Departement'].unique())
    selected_deps = st.sidebar.multiselect(
        "Départements d'Île-de-France",
        options=available_deps,
        default=available_deps
    )
    
    st.sidebar.subheader("Sécurité et fiabilité")
    trust_only = st.sidebar.toggle("Espaces vérifiés (SEO Consistent)", value=False)
    
    filtered_df = df[df['Departement'].isin(selected_deps)]
    
    if search_query:
        filtered_df = filtered_df[filtered_df['Titre'].str.contains(search_query, case=False, na=False)]
    
    if trust_only:
        filtered_df = filtered_df[filtered_df['SEO_Consistent'] == True]

    st.title("Dashboard Coworking IDF")
    st.markdown(f"Analyseur de données | {len(filtered_df)} espaces sélectionnés")

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Total sélectionnés", len(filtered_df))
    with m2:
        verified_pct = (filtered_df['SEO_Consistent'].mean() * 100) if not filtered_df.empty else 0
        st.metric("Fiabilité moyenne", f"{verified_pct:.1f}%")
    with m3:
        st.metric("Départements actifs", len(filtered_df['Departement'].unique()))
    with m4:
        st.metric("Sites web", filtered_df['Site_Web'].notna().sum())

    st.markdown("---")


    st.subheader("Localisation des espaces")
    
    if not filtered_df.empty:
        m = folium.Map(location=[48.8566, 2.3522], zoom_start=10, tiles="CartoDB positron")
        marker_cluster = MarkerCluster().add_to(m)

        for _, row in filtered_df.iterrows():

            email = row['Emails_Officiels'] if row['Emails_Officiels'] != 'N/A' else "Consulter le site"
            image = row['Lien Image Principale'] if row['Lien Image Principale'] != 'N/A' else "https://via.placeholder.com/150"
            
            html = f"""
            <div style="font-family: 'Arial'; width: 220px; font-size: 13px;">
                <img src="{image}" style="width:100%; border-radius: 5px; margin-bottom: 5px;">
                <h4 style="margin:0; color:#00d4ff;">{row['Titre']}</h4>
                <p style="margin:5px 0;"><b>Adresse:</b> {row['Adresse']}</p>
                <p style="margin:5px 0;"><b>Email:</b> {email}</p>
                <p style="margin:5px 0;"><b>Tel:</b> {row['Téléphone']}</p>
                <a href="{row['Site_Web']}" target="_blank" style="color:#00d4ff; font-weight:bold;">Accéder au site</a>
            </div>
            """
            
            folium.Marker(
                location=[row['latitude'], row['longitude']],
                popup=folium.Popup(html, max_width=250),
                tooltip=row['Titre'],
                icon=folium.Icon(color='blue' if row['SEO_Consistent'] else 'orange', icon='info-sign')
            ).add_to(marker_cluster)

        st_folium(m, width="100%", height=550)
    else:
        st.warning("Aucun résultat pour ces filtres. Essayez d'élargir votre recherche.")

    with st.expander("Voir la base de données brute (Accessibilité)"):
        st.dataframe(
            filtered_df[['Titre', 'Adresse', 'Code_Postal', 'Emails_Officiels', 'Site_Web', 'SEO_Consistent']],
            use_container_width=True
        )
        
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Exporter la sélection en CSV",
        data=csv,
        file_name='export_coworking_idf.csv',
        mime='text/csv',
    )

st.sidebar.markdown("---")
st.sidebar.caption("Management des coworkings en IDF")