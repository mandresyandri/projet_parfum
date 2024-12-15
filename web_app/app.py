import pandas as pd
import streamlit as st
import plotly.express as px
from st_mongo_connection import MongoDBConnection

# Connexion et import des données
connection = st.connection("mongodb", type=MongoDBConnection)
df = pd.DataFrame.from_dict(connection.find())

# Partie visuel
st.title("Le meilleur prix pour Nina Ricci")
contenance_filter = st.multiselect("Sélectionnez la/les contenances à afficher :", options=df["contenance"].unique(), default=df["contenance"].unique())
filtered_df = df[df["contenance"].isin(contenance_filter)]

fig = px.bar(
    filtered_df,
    x="contenance",
    y="prix",
    color="platform",
    barmode="group",
    title="Prix par contenance et magasin",
    labels={"prix": "Prix (€)", "contenance": "Contenance"}
)

# Afficher le graphique
st.plotly_chart(fig)
