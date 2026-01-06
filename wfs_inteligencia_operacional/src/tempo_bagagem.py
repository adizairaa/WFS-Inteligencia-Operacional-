def calcular_tempos_estimados(linha):
    fator_dist = 1.0 if linha["distancia_posicao"] == "PERTO" else 1.4

    capacidade = (
        linha["equipes_disponiveis"] *
        linha["esteiras_disponiveis"] *
        linha["veiculos_disponiveis"]
    )

    if capacidade == 0:
        return None, None

    fator_concorrencia = 1 + (linha["voos_simultaneos"] - 1) * 0.12

    tempo_ultima = (
        linha["quantidade_bagagens"]
        / capacidade
        * linha["tempo_medio_transporte"]
        * fator_dist
        * fator_concorrencia
    )

    tempo_primeira = tempo_ultima * 0.35
    return round(tempo_primeira,1), round(tempo_ultima,1)
