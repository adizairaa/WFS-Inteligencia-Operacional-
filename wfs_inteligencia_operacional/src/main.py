# src/main.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from tempo_bagagem import calcular_tempos_estimados
from sla import obter_sla_ultima, ajustar_sla_por_horario, ajustar_sla_para_meta
from risco import classificar_risco, score_risco
from turnos import ranking_turnos_criticos
from alertas import gerar_alertas

def carregar_dados():
    print("📥 Carregando base de dados...")
    return pd.read_csv("dados/voos.csv")

def calcular_tempos(df):
    print("⏱️ Calculando tempos de bagagem...")
    resultados = df.apply(lambda l: calcular_tempos_estimados(l), axis=1, result_type="expand")
    df["tempo_primeira_bagagem"] = resultados[0]
    df["tempo_ultima_bagagem"] = resultados[1]
    return df

def aplicar_sla(df):
    print("📊 Aplicando SLA por tipo de voo e horário...")
    df["sla_ultima"] = df["tipo_voo"].apply(obter_sla_ultima)
    df["hora_chegada"] = pd.to_datetime(df["horario_chegada"]).dt.hour
    df["sla_ultima_horario"] = df.apply(lambda l: ajustar_sla_por_horario(df, l["tipo_voo"], l["hora_chegada"]), axis=1)
    return df

def avaliar_risco(df):
    print("🚦 Avaliando risco operacional...")
    df["risco_ultima"] = df.apply(lambda l: classificar_risco(l["tempo_ultima_bagagem"], l["sla_ultima_horario"]), axis=1)
    df["score_risco"] = df["risco_ultima"].apply(score_risco)
    return df

def resumo_gerencial(df):
    resumo = df["risco_ultima"].value_counts().to_frame("Quantidade")
    resumo["Porcentagem (%)"] = (resumo["Quantidade"] / resumo["Quantidade"].sum() * 100).round(1)
    print("\n📈 RESUMO DE RISCO – ÚLTIMA BAGAGEM")
    print(resumo)

    print("\n🚦 TOP 5 VOOS COM MAIOR RISCO")
    print(df.sort_values("score_risco", ascending=False)[["id_voo","tipo_voo","tempo_ultima_bagagem","sla_ultima_horario","risco_ultima"]].head(5))

def gerar_heatmap(df):
    plt.figure(figsize=(10,6))
    pivot = df.pivot_table(index=df["hora_chegada"], columns="tipo_voo", values="tempo_ultima_bagagem", aggfunc="mean")
    sns.heatmap(pivot, annot=True, fmt=".1f", cmap="coolwarm")
    plt.title("⏱️ Tempo Médio da Última Bagagem por Hora e Tipo de Voo")
    plt.xlabel("Tipo de Voo")
    plt.ylabel("Hora de Chegada")
    plt.tight_layout()
    plt.show()

def main():
    df = carregar_dados()
    df = calcular_tempos(df)
    df = aplicar_sla(df)
    df = ajustar_sla_para_meta(df, meta_alto_risco=0.3)
    df = avaliar_risco(df)

    resumo_gerencial(df)
    ranking_turnos_criticos(df)
    gerar_alertas(df)
    gerar_heatmap(df)

if __name__ == "__main__":
    main()
