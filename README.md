✈️  – Inteligência Operacional de Bagagens

Este projeto tem como objetivo analisar, simular e comparar cenários operacionais (AS IS × TO BE) no processo de desembarque de bagagens, utilizando análise de dados, regras de SLA e avaliação de risco operacional.

O foco é apoiar a tomada de decisão por meio de métricas objetivas, simulações e visualizações gráficas, seguindo boas práticas de projetos analíticos aplicados ao contexto aeroportuário.

🎯 Objetivo do Projeto

Simular o tempo de entrega da primeira e última bagagem

Avaliar o cumprimento de SLA

Classificar o risco operacional

Comparar cenários AS IS (atual) × TO BE (otimizado)

Visualizar resultados com gráficos comparativos e heatmaps

Criar base para dashboard interativo (Streamlit)

🧠 Conceito Analítico

O projeto utiliza variáveis operacionais reais, como:

Quantidade de bagagens

Equipes disponíveis

Esteiras e veículos

Voos simultâneos

Distância operacional (PERTO / LONGE)

Tempo médio de transporte

A partir desses dados, são calculados:

⏱️ Tempo estimado da primeira bagagem

⏱️ Tempo estimado da última bagagem

📊 SLA (horário alvo)

⚠️ Risco operacional (baixo, médio, alto)

📁 Estrutura do Projeto
wfs_inteligencia_operacional/
│
├── data/
│   └── base_operacional.csv
│
├── src/
│   ├── tempo_bagagem.py        # Cálculo de tempos estimados
│   ├── cenario.py              # Simulação AS IS × TO BE
│   ├── visualizacao.py         # Gráficos e heatmaps
│   ├── main.py / main1.py      # Execução principal
│
├── app.py                      # Dashboard Streamlit (opcional)
│
├── requirements.txt
├── README.md
└── .gitignore

🧮 Lógica de Cálculo (Resumo)
Capacidade Operacional
capacidade = equipes × esteiras × veículos

Fatores de Ajuste

Distância operacional

Concorrência de voos simultâneos

Tempos Estimados

Primeira bagagem ≈ 35% do tempo da última

Última bagagem baseada na capacidade real

⚠️ Classificação de Risco

O risco é definido com base na relação entre:

Tempo estimado da última bagagem

SLA estabelecido

Exemplo conceitual:

Situação	Risco
Dentro do SLA	Baixo
Até +10 min	Médio
Acima disso	Alto
📊 Visualizações

O projeto gera:

Gráficos comparativos de SLA (AS IS × TO BE)

Distribuição de risco operacional

Heatmap de risco por voo / cenário

Comparação visual de desempenho

Os gráficos são exibidos diretamente na tela (sem fechamento automático).

▶️ Como Executar
1️⃣ Ativar o ambiente virtual
source .venv/Scripts/activate

2️⃣ Executar o projeto
python src/main.py


ou

python src/main1.py

🌐 Dashboard Interativo (Streamlit)

O projeto pode ser visualizado como dashboard:

streamlit run app.py


Permite:

Seleção de cenário

Visualização interativa de SLA e risco

Análise exploratória dos dados

🛠️ Tecnologias Utilizadas

Python 3.11

Pandas

NumPy

Matplotlib

Seaborn

Streamlit

Git & GitHub

📌 Contexto Acadêmico e Profissional

Este projeto foi desenvolvido como um case de inteligência operacional, inspirado em práticas reais de empresas do setor aéreo e logístico, com foco em:

Análise de desempenho

Gestão de SLA

Redução de risco operacional

Apoio à decisão estratégica

👤 Autora

Adila Zairaa
Analista de Dados | Tecnologia | Inteligência Operacional
GitHub: https://github.com/adizairaa
