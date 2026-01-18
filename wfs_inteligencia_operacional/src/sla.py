# src/sla.py
import pandas as pd

def obter_sla_primeira(tipo_voo):
    return 15 if tipo_voo == "NARROW" else 20

def obter_sla_ultima(tipo_voo):
    return 25 if tipo_voo == "NARROW" else 50

def ajustar_sla_por_tipo(df, tipo_voo, percentile=0.75):
    tempos = df[df["tipo_voo"] == tipo_voo]["tempo_ultima_bagagem"]
    if len(tempos) == 0:
        return obter_sla_ultima(tipo_voo)
    return max(obter_sla_ultima(tipo_voo), tempos.quantile(percentile))

def ajustar_sla_por_horario(df, tipo_voo, hora, percentile=0.75):
    subset = df[(df["tipo_voo"] == tipo_voo) & (pd.to_datetime(df["horario_chegada"]).dt.hour == hora)]
    if len(subset) == 0:
        return obter_sla_ultima(tipo_voo)
    return max(obter_sla_ultima(tipo_voo), subset["tempo_ultima_bagagem"].quantile(percentile))

def ajustar_sla_para_meta(df, meta_alto_risco=0.3, max_iter=10):
    df = df.copy()
    fator = 1.0
    iteracao = 0

    while iteracao < max_iter:
        df["sla_ultima_horario_temp"] = df["sla_ultima_horario"] * fator
        df["risco_ultima_temp"] = df.apply(
            lambda l: "ALTO_RISCO" if l["tempo_ultima_bagagem"] > l["sla_ultima_horario_temp"]*1.0 else
                      ("ATENCAO" if l["tempo_ultima_bagagem"] > l["sla_ultima_horario_temp"]*0.6 else "NO_PRAZO"),
            axis=1
        )
        pct_alto = (df["risco_ultima_temp"] == "ALTO_RISCO").mean()
        if pct_alto <= meta_alto_risco:
            break
        fator *= 1.05
        iteracao += 1

    df["sla_ultima_horario"] = df["sla_ultima_horario"] * fator
    return df
