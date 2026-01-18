import pandas as pd
import numpy as np
from pathlib import Path

np.random.seed(42)


TOTAL_VOOS = 200

DISTRIBUICAO_RISCO = {
    "NO_PRAZO": 0.73,
    "ATENCAO": 0.21,
    "ALTO_RISCO": 0.06
}

SLA_ULTIMA = {
    "NARROW": 25,
    "WIDE": 50
}

PASTA_DADOS = Path("dados")
PASTA_DADOS.mkdir(exist_ok=True)

DATA_BASE = "2024-10-01"



def gerar_horario():
    hora = np.random.choice(range(24))
    minuto = np.random.choice([0, 10, 20, 30, 40, 50])
    return pd.Timestamp(f"{DATA_BASE} {hora:02d}:{minuto:02d}")

def tipo_voo():
    return np.random.choice(["NARROW", "WIDE"], p=[0.75, 0.25])

def gerar_tempo_ultima(sla, risco):
    if risco == "NO_PRAZO":
        return np.random.uniform(sla * 0.6, sla)
    elif risco == "ATENCAO":
        return np.random.uniform(sla * 1.01, sla * 1.6)
    else:
        return np.random.uniform(sla * 1.61, sla * 2.4)



dados = []

quantidades = {
    risco: int(TOTAL_VOOS * pct)
    for risco, pct in DISTRIBUICAO_RISCO.items()
}


quantidades["NO_PRAZO"] += TOTAL_VOOS - sum(quantidades.values())

id_voo = 1

for risco, qtd in quantidades.items():
    for _ in range(qtd):
        tipo = tipo_voo()
        sla = SLA_ULTIMA[tipo]
        tempo_ultima = gerar_tempo_ultima(sla, risco)

        dados.append({
            "id_voo": f"VOO{id_voo:04d}",
            "tipo_voo": tipo,
            "horario_chegada": gerar_horario(),
            "tempo_ultima_bagagem": round(tempo_ultima, 1),
            "sla_ultima": sla,
            "risco_ultima": risco
        })

        id_voo += 1

df = pd.DataFrame(dados)


df = df.sample(frac=1).reset_index(drop=True)

caminho = PASTA_DADOS / "voos_processados.csv"
df.to_csv(caminho, index=False)

print(" Base gerada com sucesso!")
print("\n Distribuição final:")
print(df["risco_ultima"].value_counts(normalize=True).mul(100).round(1))
print(f"\n Arquivo salvo em: {caminho}")
