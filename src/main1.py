import matplotlib
matplotlib.use("TkAgg")

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from tempo_bagagem import calcular_tempos_estimados
from sla import obter_sla_ultima, ajustar_sla_por_horario, ajustar_sla_para_meta
from risco import classificar_risco, score_risco
from turnos import ranking_turnos_criticos
from alertas import gerar_alertas


OUTPUT_DIR = os.path.join("outputs", "graficos")
os.makedirs(OUTPUT_DIR, exist_ok=True)

sns.set_theme(style="whitegrid")


def carregar_dados():
    print("📥 Carregando base de dados...")
    return pd.read_csv("dados/voos.csv")


def calcular_tempos(df):
    print("⏱️ Calculando tempos de bagagem...")
    resultados = df.apply(
        lambda l: calcular_tempos_estimados(l),
        axis=1,
        result_type="expand"
    )
    df["tempo_primeira_bagagem"] = resultados[0]
    df["tempo_ultima_bagagem"] = resultados[1]
    return df


def aplicar_sla(df):
    print("📏 Aplicando SLA por tipo de voo e horário...")
    df["sla_ultima"] = df["tipo_voo"].apply(obter_sla_ultima)
    df["hora_chegada"] = pd.to_datetime(df["horario_chegada"]).dt.hour
    df["sla_ultima_horario"] = df.apply(
        lambda l: ajustar_sla_por_horario(df, l["tipo_voo"], l["hora_chegada"]),
        axis=1
    )
    return df


def avaliar_risco(df):
    print(" Avaliando risco operacional...")

    def risco_seguro(tempo, sla):
        if pd.isna(tempo) or pd.isna(sla):
            return "Baixo"  # fallback operacional
        return classificar_risco(tempo, sla)

    df["risco_ultima"] = df.apply(
        lambda l: risco_seguro(
            l["tempo_ultima_bagagem"],
            l["sla_ultima_horario"]
        ),
        axis=1
    )

    df["score_risco"] = df["risco_ultima"].apply(score_risco)
    return df



def resumo_gerencial(df):
    resumo = df["risco_ultima"].value_counts().to_frame("Quantidade")
    resumo["Porcentagem (%)"] = (
        resumo["Quantidade"] / resumo["Quantidade"].sum() * 100
    ).round(1)

    print("\n📊 RESUMO DE RISCO – ÚLTIMA BAGAGEM")
    print(resumo)

    print("\n🚨 TOP 5 VOOS COM MAIOR RISCO")
    print(
        df.sort_values("score_risco", ascending=False)[
            ["id_voo", "tipo_voo", "tempo_ultima_bagagem",
             "sla_ultima_horario", "risco_ultima"]
        ].head(5)
    )


#GRÁFICOS 
def grafico_risco(df):
    categorias = ["Baixo", "Médio", "Alto"]

    df_plot = df.copy()
    df_plot["risco_ultima"] = pd.Categorical(
        df_plot["risco_ultima"],
        categories=categorias,
        ordered=True
    )

    plt.figure(figsize=(8,5))
    sns.countplot(
        data=df_plot,
        x="risco_ultima",
        order=categorias
    )

    plt.title("Distribuição de Risco Operacional – Última Bagagem")
    plt.xlabel("Nível de Risco")
    plt.ylabel("Quantidade de Voos")

    caminho = os.path.join(OUTPUT_DIR, "grafico_risco_operacional.png")
    plt.tight_layout()
    plt.savefig(caminho)

    plt.show()
    print(f"Gráfico de risco salvo em: {caminho}")


    # Define ordem categórica explícita
    ordem = ["Baixo", "Médio", "Alto"]
    df_plot["risco_ultima"] = pd.Categorical(
        df_plot["risco_ultima"],
        categories=ordem,
        ordered=True
    )

    plt.figure(figsize=(8,5))

    sns.countplot(
        data=df_plot,
        x="risco_ultima",
        order=ordem
    )

    plt.title("Distribuição de Risco Operacional – Última Bagagem")
    plt.xlabel("Nível de Risco")
    plt.ylabel("Quantidade de Voos")

    caminho = os.path.join(OUTPUT_DIR, "grafico_risco_operacional.png")
    plt.tight_layout()
    plt.savefig(caminho)

    plt.show(block=True)

    print(f"Gráfico de risco salvo em: {caminho}")



def grafico_sla(df):
    df["cumpriu_sla"] = df["tempo_ultima_bagagem"] <= df["sla_ultima_horario"]
    sla_resumo = df["cumpriu_sla"].value_counts(normalize=True).mul(100)

    plt.figure(figsize=(6, 6))
    sla_resumo.rename({
        True: "Dentro do SLA",
        False: "Fora do SLA"
    }).plot(
        kind="pie",
        autopct="%1.1f%%",
        startangle=90
    )

    plt.title("Cumprimento do SLA – Última Bagagem")
    plt.ylabel("")

    caminho = os.path.join(OUTPUT_DIR, "grafico_cumprimento_sla.png")
    plt.tight_layout()
    plt.savefig(caminho)

    print(f"✅ Gráfico de SLA salvo em: {caminho}")


def gerar_heatmap(df):
    plt.figure(figsize=(10, 6))

    pivot = df.pivot_table(
        index="hora_chegada",
        columns="tipo_voo",
        values="tempo_ultima_bagagem",
        aggfunc="mean"
    )

    sns.heatmap(pivot, annot=True, fmt=".1f", cmap="coolwarm")
    plt.title("Tempo Médio da Última Bagagem por Hora e Tipo de Voo")
    plt.xlabel("Tipo de Voo")
    plt.ylabel("Hora de Chegada")

    caminho = os.path.join(OUTPUT_DIR, "heatmap_tempo_ultima_bagagem.png")
    plt.tight_layout()
    plt.savefig(caminho)

    print(f"✅ Heatmap salvo em: {caminho}")


def main():
    df = carregar_dados()
    df = calcular_tempos(df)
    df = aplicar_sla(df)
    df = ajustar_sla_para_meta(df, meta_alto_risco=0.3)
    df = avaliar_risco(df)

    resumo_gerencial(df)
    ranking_turnos_criticos(df)
    gerar_alertas(df)

    grafico_risco(df)
    grafico_sla(df)
    gerar_heatmap(df)

    print("\n📌 Gráficos exibidos. Feche as janelas para encerrar.")
    plt.show()  


if __name__ == "__main__":
    main()

