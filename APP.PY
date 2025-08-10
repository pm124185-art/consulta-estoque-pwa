
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Consulta de Estoque", layout="wide")

# Carregar dados
df = pd.read_excel("VALIDADES.xlsx")
df["VALIDADE"] = pd.to_datetime(df["VALIDADE"], errors="coerce")
df["Dias para Vencer"] = (df["VALIDADE"] - datetime.now()).dt.days

# Filtro por intervalo de dias
dias = st.slider("Filtrar por dias até o vencimento", min_value=-365, max_value=365, value=(-30, 60))
df_filtrado = df[(df["Dias para Vencer"] >= dias[0]) & (df["Dias para Vencer"] <= dias[1])]

# Cores
def cor_linha(row):
    if row["Dias para Vencer"] < 0:
        return ["background-color: red; color: white"] * len(row)
    elif row["Dias para Vencer"] <= 30:
        return ["background-color: yellow"] * len(row)
    else:
        return [""] * len(row)

st.subheader("Tabela de Produtos")
st.dataframe(df_filtrado.style.apply(cor_linha, axis=1))

# Gráficos
col1, col2 = st.columns(2)

with col1:
    fig_bar = px.histogram(df_filtrado, x=df_filtrado["VALIDADE"].dt.to_period("M").astype(str),
                           title="Produtos por Mês de Vencimento", labels={"x": "Mês", "y": "Quantidade"})
    st.plotly_chart(fig_bar, use_container_width=True)

with col2:
    status = df_filtrado["Dias para Vencer"].apply(lambda x: "Vencido" if x < 0 else ("Próx 30 dias" if x <= 30 else "Ok"))
    fig_pie_status = px.pie(names=status, title="Distribuição por Status")
    st.plotly_chart(fig_pie_status, use_container_width=True)

# Pizza por fornecedor
fig_pie_forn = px.pie(df_filtrado, names="FORNECEDOR", title="Distribuição por Fornecedor")
st.plotly_chart(fig_pie_forn, use_container_width=True)

# Exportar
st.download_button(
    "Exportar para Excel",
    data=df_filtrado.to_excel(index=False),
    file_name="estoque_filtrado.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
