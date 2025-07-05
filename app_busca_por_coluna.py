
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Consulta de Equipamentos", layout="wide")
st.title("🔍 Consulta Avançada de Equipamentos")

# Carregar a planilha
file_path = "Equipment.xlsx"
df = pd.read_excel(file_path)

st.markdown("Use os campos abaixo para filtrar os dados conforme cada coluna.")

# Criar colunas de busca para os principais campos
col1, col2, col3 = st.columns(3)
col4, col5, col6 = st.columns(3)

with col1:
    f_applicable = st.text_input("Applicable for")
with col2:
    f_status = st.text_input("Status")
with col3:
    f_eq_number = st.text_input("Equipment number")

with col4:
    f_description = st.text_input("Description")
with col5:
    f_model = st.text_input("Model / type number")
with col6:
    f_location = st.text_input("Physical location")

# Aplicar filtros dinamicamente
df_filtrado = df.copy()
if f_applicable:
    df_filtrado = df_filtrado[df_filtrado['Applicable for'].astype(str).str.contains(f_applicable, case=False)]
if f_status:
    df_filtrado = df_filtrado[df_filtrado['Status'].astype(str).str.contains(f_status, case=False)]
if f_eq_number:
    df_filtrado = df_filtrado[df_filtrado['Equipment number'].astype(str).str.contains(f_eq_number, case=False)]
if f_description:
    df_filtrado = df_filtrado[df_filtrado['Description'].astype(str).str.contains(f_description, case=False)]
if f_model:
    df_filtrado = df_filtrado[df_filtrado['Model / type number'].astype(str).str.contains(f_model, case=False)]
if f_location:
    df_filtrado = df_filtrado[df_filtrado['Physical location'].astype(str).str.contains(f_location, case=False)]

# Exibir resultados
st.markdown(f"### 🔎 {len(df_filtrado)} resultado(s) encontrado(s):")
st.dataframe(df_filtrado)

# Botão para download
csv_download = df_filtrado.to_csv(index=False).encode("utf-8")
st.download_button("📥 Baixar resultados filtrados", data=csv_download,
                   file_name="equipamentos_filtrados.csv", mime="text/csv")
