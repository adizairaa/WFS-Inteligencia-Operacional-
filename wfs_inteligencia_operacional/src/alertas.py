# src/alertas.py
import pandas as pd

RISK_THRESHOLD = 1.5
risk_map = {"NO_PRAZO": 0, "ATENCAO": 1, "ALTO_RISCO": 2}

def gerar_alertas(df):
    df["score_risco_last"] = df["risco_ultima"].map(risk_map)
    alerts = df[df["score_risco_last"] > RISK_THRESHOLD]

    if not alerts.empty:
        print("\n🚨 ALERTA OPERACIONAL – RISCO CRÍTICO DETECTADO 🚨")
        print(alerts[["id_voo", "tipo_voo", "horario_chegada", "tempo_ultima_bagagem", "sla_ultima", "risco_ultima"]].head(10))
        alerts.to_csv("outputs/tables/alertas_voos_criticos.csv", index=False)
    else:
        print("\n✅ Nenhum voo acima do limiar crítico de risco")
