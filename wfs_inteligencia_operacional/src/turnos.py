# src/turnos.py
import pandas as pd

def definir_turno(hora):
    if 0 <= hora <= 5:
        return "MADRUGADA"
    elif 6 <= hora <= 11:
        return "MANHÃ"
    elif 12 <= hora <= 17:
        return "TARDE"
    else:
        return "NOITE"

def ranking_turnos_criticos(df):
    if "horario_chegada" not in df.columns:
        raise ValueError("O DataFrame precisa conter a coluna 'horario_chegada'")

    df["hora"] = pd.to_datetime(df["horario_chegada"]).dt.hour
    df["turno"] = df["hora"].apply(definir_turno)

    shift_risk = (
        df.groupby("turno")
          .agg(
              total_voos=("id_voo", "count"),
              risco_medio=("score_risco", "mean"),
              alto_risco=("risco_ultima", lambda x: (x=="ALTO_RISCO").sum())
          )
          .reset_index()
          .sort_values(by="risco_medio", ascending=False)
    )
    shift_risk["pct_alto_risco"] = shift_risk["alto_risco"] / shift_risk["total_voos"] * 100

    shift_risk.to_csv("outputs/tables/ranking_turnos.csv", index=False)
    print("\n📊 RANKING DE TURNOS CRÍTICOS")
    print(shift_risk)

    return shift_risk
