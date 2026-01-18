def classificar_risco(tempo_real, sla):
    if tempo_real <= sla:
        return "NO_PRAZO"
    elif tempo_real <= sla * 1.6:
        return "ATENCAO"
    else:
        return "ALTO_RISCO"

def score_risco(risco):
    mapa = {"NO_PRAZO": 0, "ATENCAO": 1, "ALTO_RISCO": 2}
    return mapa.get(risco, 2)
