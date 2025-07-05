
import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Registro de Equipamentos", layout="centered")

st.title("📋 Registro de Escaneamento de QR Codes")
st.write("Registre os equipamentos escaneados e visualize os dados ao vivo.")

# Nome do operador
operador = st.text_input("Digite seu nome:")

if operador:
    st.success(f"Operador ativo: {operador}")

    # Diretório e arquivo de log
    log_dir = "logs_qrcode_streamlit"
    os.makedirs(log_dir, exist_ok=True)
    data = datetime.now().strftime("%Y-%m-%d")
    hora = datetime.now().strftime("%H:%M:%S")
    log_file = os.path.join(log_dir, f"log_{data}.xlsx")

    # Entrada do QR Code
    qr_input = st.text_input("📸 Escaneie ou cole o link do QR Code:")

    if st.button("Registrar leitura"):
        if qr_input:
            if "#Equipment=" in qr_input:
                equipamento = qr_input.split("#Equipment=")[-1]
            else:
                equipamento = "NÃO IDENTIFICADO"

            registro = {
                "Data": data,
                "Hora": hora,
                "Operador": operador,
                "Equipment number": equipamento,
                "Link escaneado": qr_input
            }

            if os.path.exists(log_file):
                df_existente = pd.read_excel(log_file)
                df = pd.concat([df_existente, pd.DataFrame([registro])], ignore_index=True)
            else:
                df = pd.DataFrame([registro])

            df.to_excel(log_file, index=False)
            st.success(f"✔ Equipamento {equipamento} registrado!")
        else:
            st.warning("Por favor, escaneie ou insira o link.")

    # Exibir registros do operador no dia
    st.subheader("📄 Equipamentos escaneados hoje")
    if os.path.exists(log_file):
        df_log = pd.read_excel(log_file)
        df_operador = df_log[df_log["Operador"] == operador]
        st.dataframe(df_operador)

        # Download do log
        csv = df_operador.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Baixar lista do dia", data=csv,
                           file_name=f"registro_{operador}_{data}.csv", mime="text/csv")

    # Campo de busca geral nos registros do dia
    st.subheader("🔍 Buscar registros do dia (qualquer operador)")
    busca = st.text_input("Digite parte do equipamento, operador ou link:")

    if busca and os.path.exists(log_file):
        df_busca = pd.read_excel(log_file)
        filtro = df_busca.apply(lambda row: busca.lower() in str(row).lower(), axis=1)
        resultados = df_busca[filtro]
        st.write(f"🔎 {len(resultados)} resultado(s) encontrado(s).")
        st.dataframe(resultados)

        csv_resultados = resultados.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Baixar resultados filtrados", data=csv_resultados,
                           file_name=f"resultados_filtrados_{data}.csv", mime="text/csv")
