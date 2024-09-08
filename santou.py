import streamlit as st
import pandas as pd
import plotly.express as px
import altair as alt

# Configuration de la page
st.set_page_config(
    page_title="Santou Population Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded")

# Chargement des données
data = {
    "District": ["Santou Centre", "Kokoya", "Ndenda", "Paradji", "Kouratountou", "Telithiaoute"],
    "Population Totale": [5144, 2070, 2723, 2174, 2937, 3377],
    "Cible PEV": [17, 7, 9, 7, 10, 11],
    "Cible CPN": [19, 8, 10, 8, 11, 13],
    "PF": [26, 10, 14, 11, 15, 17],
    "Latitude": [10.35, 10.33, 10.31, 10.37, 10.39, 10.32],  # Coordonnées fictives
    "Longitude": [-12.45, -12.42, -12.41, -12.44, -12.48, -12.43]  # Coordonnées fictives
}

df = pd.DataFrame(data)

# Sidebar pour la sélection des couleurs
with st.sidebar:
    st.title("🌍 Santou Population Dashboard")
    
    color_theme_list = ['Blues', 'Cividis', 'Greens', 'Inferno', 'Magma', 'Plasma', 'Reds', 'Turbo', 'Viridis']
    selected_color_theme = st.selectbox('Sélectionner un thème de couleur', color_theme_list)

#######################
# Fonctions pour les visualisations

# Carte Choroplèthe
def make_choropleth(input_df, input_color_theme):
    choropleth = px.choropleth(
        input_df, 
        locations="District", 
        locationmode=None,  # Pas de mode spécifique pour les pays/régions prédéfinis
        color="Population Totale",
        hover_name="District",
        hover_data={"Population Totale": True},
        color_continuous_scale=input_color_theme,
        labels={'Population Totale':'Population'}
    )
    choropleth.update_geos(fitbounds="locations")
    choropleth.update_layout(
        template='plotly_dark',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        margin=dict(l=0, r=0, t=0, b=0),
        height=500
    )
    return choropleth

# Graphique en barres
def make_bar_chart(input_df, x_column, y_column, title):
    bar_chart = px.bar(input_df, x=x_column, y=y_column, color=x_column, title=title)
    bar_chart.update_layout(
        template='plotly_dark',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        margin=dict(l=0, r=0, t=30, b=0),
        height=400
    )
    return bar_chart

# Donut chart
def make_donut(input_value, label, input_color):
    chart_color = [input_color, '#31333F']
    
    source = pd.DataFrame({
        "Topic": [label, ''],
        "Value": [input_value, 100-input_value]
    })
    
    donut_chart = alt.Chart(source).mark_arc(innerRadius=50, outerRadius=100).encode(
        theta=alt.Theta(field="Value", type="quantitative"),
        color=alt.Color(field="Topic", type="nominal", scale=alt.Scale(range=chart_color), legend=None),
        tooltip=[alt.Tooltip(field="Topic", type="nominal"), alt.Tooltip(field="Value", type="quantitative")]
    ).properties(
        width=200,
        height=200
    )
    return donut_chart

#######################
# Tableau de bord

# Colonnes pour les sections principales
col1, col2, col3 = st.columns((2, 5, 2), gap='medium')

with col1:
    st.markdown("### Statistiques Clés des Districts")
    
    # Afficher les métriques pour les districts avec la plus grande et plus petite population
    max_population_district = df.loc[df['Population Totale'].idxmax()]['District']
    max_population_value = df['Population Totale'].max()
    min_population_district = df.loc[df['Population Totale'].idxmin()]['District']
    min_population_value = df['Population Totale'].min()
    
    st.metric(label=f"District le plus peuplé : {max_population_district}", value=max_population_value)
    st.metric(label=f"District le moins peuplé : {min_population_district}", value=min_population_value)
    
    # Donut charts
    st.markdown("#### Répartition par Cibles de Santé")
    donut_cpn = make_donut(65, 'CPN', '#29b5e8')
    donut_pev = make_donut(35, 'PEV', '#F39C12')
    st.altair_chart(donut_cpn)
    st.altair_chart(donut_pev)

with col2:
    st.markdown("### Cartographie des Districts de Santou")
    
    # Afficher la carte choroplèthe
    choropleth = make_choropleth(df, selected_color_theme)
    st.plotly_chart(choropleth, use_container_width=True)
    
    # Graphique en barres : Population par district
    st.markdown("### Population par District")
    bar_chart_population = make_bar_chart(df, "District", "Population Totale", "Population Totale par District")
    st.plotly_chart(bar_chart_population, use_container_width=True)

with col3:
    st.markdown("### Données Complètes des Districts")
    
    # Afficher le tableau des données
    st.dataframe(df[['District', 'Population Totale', 'Cible PEV', 'Cible CPN', 'PF']], height=400)
    
    # Explication du projet
    with st.expander('À propos', expanded=True):
        st.write("""
            - Ce tableau de bord présente les données démographiques et de santé des districts de la sous-préfecture de Santou.
            - Utilisez le menu latéral pour personnaliser le thème des couleurs.
        """)

