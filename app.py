import streamlit as st
import pandas as pd

from src.tempo_bagagem import calcular_tempos_estimados
from src.sla import obter_sla_ultima, ajustar_sla_por_horario
from src.risco import classificar_risco, score_risco

st.set_page_config(
    page_title="WFS – Inteligência Operacional",
    layout="wide"
)

st.title("✈️ WFS – Painel de Inteligência Operacional")
st.markdown("Monitoramento de SLA, risco e performance operacional")

# ----------------------------
# Carregar dados
# ----------------------------
@st.cache_data
def carregar_dados():
    return pd.read_csv("dados/voos.csv")

df = carregar_dados()

# ----------------------------
# Processamento
# ----------------------------
resultados = df.apply(
    lambda l: calcular_tempos_estimados(l),
    axis=1,
    result_type="expand"
)

df["tempo_primeira_bagagem"] = resultados[0]
df["tempo_ultima_bagagem"] = resultados[1]

df["sla_ultima"] = df["tipo_voo"].apply(obter_sla_ultima)
df["hora_chegada"] = pd.to_datetime(df["horario_chegada"]).dt.hour
df["sla_ultima_horario"] = df.apply(
    lambda l: ajustar_sla_por_horario(df, l["tipo_voo"], l["hora_chegada"]),
    axis=1
)

def risco_seguro(tempo, sla):
    if pd.isna(tempo) or pd.isna(sla):
        return "Baixo"
    r = classificar_risco(tempo, sla)
    return r if r in ["Baixo", "Médio", "Alto"] else "Baixo"

df["risco"] = df.apply(
    lambda l: risco_seguro(l["tempo_ultima_bagagem"], l["sla_ultima_horario"]),
    axis=1
)

# ----------------------------
# KPIs
# ----------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Voos Analisados", len(df))

with col2:
    pct_sla = (df["tempo_ultima_bagagem"] <= df["sla_ultima_horario"]).mean() * 100
    st.metric("SLA Cumprido (%)", f"{pct_sla:.1f}%")

with col3:
    risco_alto = (df["risco"] == "Alto").sum()
    st.metric("Voos Alto Risco", risco_alto)

# ----------------------------
# Gráficos
# ----------------------------
st.subheader("📊 Distribuição de Risco Operacional")
st.bar_chart(df["risco"].value_counts())

st.subheader("🔥 Heatmap – Tempo Médio da Última Bagagem")
heatmap = df.pivot_table(
    index="hora_chegada",
    columns="tipo_voo",
    values="tempo_ultima_bagagem",
    aggfunc="mean"
)
st.dataframe(heatmap.style.background_gradient(cmap="coolwarm"))
