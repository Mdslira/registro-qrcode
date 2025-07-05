
import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Consulta e Cadastro de Equipamentos", layout="wide")
st.title("📋 Consulta e Cadastro de Equipamentos")

file_path = "Equipment.xlsx"

# Carregar ou criar planilha
if os.path.exists(file_path):
    df = pd.read_excel(file_path)
else:
    df = pd.DataFrame(columns=[
        'Applicable for', 'Status', 'Equipment number', 'Description',
        'product', 'Model / type number', 'Measuring range',
        'Calibration performer', 'Physical location', 'Deadline'
    ])

st.markdown("### 🔍 Filtros por coluna")

# Filtros
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

st.markdown(f"### 🔎 {len(df_filtrado)} resultado(s) encontrado(s):")
st.dataframe(df_filtrado)

csv_download = df_filtrado.to_csv(index=False).encode("utf-8")
st.download_button("📥 Baixar resultados filtrados", data=csv_download,
                   file_name="equipamentos_filtrados.csv", mime="text/csv")

# Seção para novo cadastro
st.markdown("---")
st.markdown("### ➕ Cadastrar novo equipamento")

with st.form("novo_equipamento"):
    c1, c2, c3 = st.columns(3)
    c4, c5, c6 = st.columns(3)

    applicable = c1.text_input("Applicable for")
    status = c2.text_input("Status")
    eq_number = c3.text_input("Equipment number")
    description = c4.text_input("Description")
    product = c5.text_input("Product")
    model = c6.text_input("Model / type number")

    c7, c8, c9 = st.columns(3)
    range_ = c7.text_input("Measuring range")
    performer = c8.text_input("Calibration performer")
    location = c9.text_input("Physical location")
    deadline = st.date_input("Deadline")

    submitted = st.form_submit_button("Salvar equipamento")

    if submitted:
        novo = {
            'Applicable for': applicable,
            'Status': status,
            'Equipment number': eq_number,
            'Description': description,
            'product': product,
            'Model / type number': model,
            'Measuring range': range_,
            'Calibration performer': performer,
            'Physical location': location,
            'Deadline': deadline
        }
        df = pd.concat([df, pd.DataFrame([novo])], ignore_index=True)
        df.to_excel(file_path, index=False)
        st.success(f"Equipamento {eq_number} cadastrado com sucesso!")
