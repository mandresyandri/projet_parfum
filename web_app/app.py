import pandas as pd
import streamlit as st
from st_mongo_connection import MongoDBConnection

# Connexion et import des données
connection = st.connection("mongodb", type=MongoDBConnection)
data = pd.DataFrame.from_dict(connection.find())

# KPI 
def lower_price(data):
    pass

# Afficher les prix les mois chères
lower = data.sort_values(by="prix", ascending=True)
st.write()


st.metric(label=lower.platform[0], value=lower.prix[0], delta="xx")