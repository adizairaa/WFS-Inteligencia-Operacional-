import pandas as pd
import numpy as np
from pathlib import Path

#Configurações para visualizar todas as colunas necessarias 
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)
pd.set_option("display.max_colwidth", None)
# Configuraões necessarias para rodar 
np.random.seed(42)

QUANTIDADE_VOOS = 200
DATA_BASE = "2024-10-01" # lembrar que vem do anuario estatistico de trafego aereo  de 2024 
PASTA_DADOS = Path("dados")
PASTA_DADOS.mkdir(parents=True, exist_ok=True)

# FUNÇÕES necessarias para a analise 


def gerar_horario_realista():
    """
    Gera horários de chegada com picos reais de operação aeroportuária baseada no relatorio utilizado como base de dados. 
    As probabilidades são normalizadas automaticamente.
    """

    pesos_horas = np.array([
        1, 1, 1, 1,      # 0–3 madrugada
        3, 5,            # 4–5
        10, 10, 10, 8,   # 6–9 pico manhã
        6, 5,            # 10–11
        4, 4,            # 12–13
        6, 8, 10,        # 14–16 pico tarde
        10, 8,           # 17–18
        6, 5,            # 19–20
        4, 3,            # 21–22
        6                # 23 pico internacional
    ])

    # Normalização automática (soma = 1) porque no Numpy so aceita igualdade a 1
    probabilidades = pesos_horas / pesos_horas.sum()

    hora = np.random.choice(range(24), p=probabilidades)
    minuto = np.random.choice([0, 10, 20, 30, 40, 50])

    return pd.Timestamp(f"{DATA_BASE} {hora:02d}:{minuto:02d}")


def definir_tipo_voo_por_horario(hora):
    """
    Define o tipo de voo com base no horário.
    """
    if hora >= 22 or hora <= 6:
        return np.random.choice(["WIDE", "NARROW"], p=[0.6, 0.4])
    elif 6 <= hora <= 9 or 16 <= hora <= 19:
        return np.random.choice(["NARROW", "WIDE"], p=[0.8, 0.2])
    else:
        return np.random.choice(["NARROW", "WIDE"], p=[0.7, 0.3])


def gerar_parametros_operacionais(tipo_voo):
    """
    Gera parâmetros operacionais coerentes com o tipo de aeronave.
    """
    if tipo_voo == "NARROW":
        return {
            "quantidade_bagagens": np.random.randint(90, 180),
            "equipes_disponiveis": np.random.randint(3, 6),
            "esteiras_disponiveis": np.random.randint(1, 3),
            "veiculos_disponiveis": np.random.randint(1, 3),
            "tempo_medio_transporte": np.random.uniform(6, 10),
        }
    else:
        return {
            "quantidade_bagagens": np.random.randint(280, 480),
            "equipes_disponiveis": np.random.randint(6, 11),
            "esteiras_disponiveis": np.random.randint(2, 5),
            "veiculos_disponiveis": np.random.randint(2, 4),
            "tempo_medio_transporte": np.random.uniform(8, 14),
        }


# Para poder gerar a base de dados em csv 

print(" Gerando base de dados operacional realista...")

dados = []

for i in range(QUANTIDADE_VOOS):
    horario = gerar_horario_realista()
    hora = horario.hour

    tipo_voo = definir_tipo_voo_por_horario(hora)
    parametros = gerar_parametros_operacionais(tipo_voo)

    dados.append({
        "id_voo": f"VOO{i+1:04d}",
        "tipo_voo": tipo_voo,
        "horario_chegada": horario,
        "hora": hora,
        "distancia_posicao": np.random.choice(["PERTO", "LONGE"], p=[0.65, 0.35]),
        "voos_simultaneos": np.random.randint(1, 7),
        **parametros
    })

df = pd.DataFrame(dados)


caminho_csv = PASTA_DADOS / "voos.csv"
df.to_csv(caminho_csv, index=False)

print(" Base de dados criada com sucesso!")
print(f" Arquivo salvo em: {caminho_csv}")
print("\n📊 Amostra dos dados (com horário de chegada):")
print(
    df[
        [
            "id_voo",
            "tipo_voo",
            "horario_chegada",
            "hora",
            "quantidade_bagagens",
            "equipes_disponiveis",
            "esteiras_disponiveis",
            "veiculos_disponiveis",
            "tempo_medio_transporte",
        ]
    ].head()
)
#  teste 
# if __name__ == "__main__":
#     df = gerar_base_dados()
#     print(df.head())
