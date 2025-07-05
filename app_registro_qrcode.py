
import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Registro de Equipamentos", layout="centered")

st.title("📋 Registro de Escaneamento de QR Codes")
st.write("Registre aqui os equipamentos escaneados via QR Code.")

# Nome do operador
operador = st.text_input("Digite seu nome:")

# Iniciar escaneamento apenas se operador preenchido
if operador:
    st.success(f"Operador ativo: {operador}")

    qr_input = st.text_input("Escaneie ou cole o link do QR Code:")

    if st.button("Registrar leitura"):
        if qr_input:
            # Extrair número do equipamento
            if "#Equipment=" in qr_input:
                equipamento = qr_input.split("#Equipment=")[-1]
            else:
                equipamento = "NÃO IDENTIFICADO"

            data = datetime.now().strftime("%Y-%m-%d")
            hora = datetime.now().strftime("%H:%M:%S")

            registro = {
                "Data": data,
                "Hora": hora,
                "Operador": operador,
                "Equipment number": equipamento,
                "Link escaneado": qr_input
            }

            # Salvar
            log_dir = "logs_qrcode_streamlit"
            os.makedirs(log_dir, exist_ok=True)
            arquivo = os.path.join(log_dir, f"log_{data}.xlsx")

            if os.path.exists(arquivo):
                df_existente = pd.read_excel(arquivo)
                df = pd.concat([df_existente, pd.DataFrame([registro])], ignore_index=True)
            else:
                df = pd.DataFrame([registro])

            df.to_excel(arquivo, index=False)
            st.success(f"✔ Equipamento {equipamento} registrado com sucesso!")

        else:
            st.warning("Por favor, insira o link do QR Code.")
else:
    st.info("Digite seu nome para iniciar o registro.")
