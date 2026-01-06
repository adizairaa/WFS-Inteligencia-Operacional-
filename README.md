# ✈️ WFS Inteligência Operacional – SLA de Bagagens

## 📌 Visão Geral

Este projeto foi desenvolvido como **case técnico para a vaga de Trainee da WFS**, com foco em **inteligência operacional aplicada ao SLA de bagagens aeroportuárias**. A solução demonstra como **engenharia de dados, regras de negócio e análise operacional** podem ser integradas para **reduzir riscos operacionais e financeiros**, apoiando a tomada de decisão.

O projeto simula um ambiente realista de operações aeroportuárias utilizando dados inspirados no **Anuário Estatístico de Tráfego Aéreo 2024**, adotando boas práticas observadas em empresas líderes do setor aéreo.

---

## 🎯 Objetivo do Case

* Monitorar o **SLA da última bagagem** por voo
* Classificar voos por **nível de risco operacional**
* Identificar **turnos críticos**
* Gerar **alertas preventivos**
* Produzir dados prontos para consumo em **Power BI**
* Traduzir risco operacional em **impacto financeiro**

---

## 🧠 Abordagem Analítica

O projeto segue um fluxo completo de dados:

1. **Geração de dados realistas** (simulação operacional)
2. **Cálculo de tempos operacionais** de bagagens
3. **Aplicação dinâmica de SLA** por tipo de voo e horário
4. **Classificação de risco** (NO_PRAZO | ATENÇÃO | ALTO_RISCO)
5. **Ajuste de SLA para metas operacionais**
6. **Alertas automáticos de risco crítico**
7. **Ranking de turnos mais críticos**
8. **Visualização analítica (heatmap)**

---

## 🏗️ Arquitetura do Projeto

```
wfs_inteligencia_operacional/
│
├── src/
│   ├── gerador_dados.py        # Geração de base operacional realista
│   ├── tempo_bagagem.py       # Cálculo de tempos de bagagem (core)
│   ├── sla.py                 # Regras e calibração dinâmica de SLA
│   ├── risco.py               # Classificação e score de risco
│   ├── turnos.py              # Ranking de turnos críticos
│   ├── alertas.py             # Geração de alertas operacionais
│   ├── visualizacoes.py       # Visualizações (heatmap)
│   └── main.py                # Orquestrador do pipeline
│
├── dados/
│   └── voos.csv               # Base gerada
│
├── outputs/
│   └── tables/                # Saídas para Power BI
│
├── shell_scripts/
│   ├── coleta_dados.sh        # Simula ingestão de dados
│   └── pipeline.sh            # Pipeline automatizado
│
└── .venv/                     # Ambiente virtual
```

---

## ⚙️ Pipeline de Dados

O pipeline é automatizado via **Shell Script**, simulando um ambiente corporativo:

1. Ativação do ambiente virtual
2. Coleta e versionamento dos dados CSV
3. Execução do pipeline Python (`main.py`)
4. Geração de logs e arquivos analíticos

Essa estrutura reflete práticas de **Data Engineering e DataOps**.

---

## 🚦 Classificação de Risco

| Nível de Risco | Critério                |
| -------------- | ----------------------- |
| NO_PRAZO       | Tempo ≤ SLA             |
| ATENÇÃO        | SLA < Tempo ≤ SLA × 1.6 |
| ALTO_RISCO     | Tempo > SLA × 1.6       |

A **zona de ATENÇÃO** é o principal diferencial do projeto, permitindo **gestão proativa**, e não apenas corretiva.

---

## 📊 Outputs Analíticos

* `alertas_voos_criticos.csv`
* `ranking_turnos.csv`
* Base tratada pronta para **Power BI**
* Heatmap de risco por horário e tipo de voo

Esses dados permitem a construção de dashboards com:

* Risco operacional em tempo quase real
* Impacto financeiro estimado
* Priorização de recursos por turno

---

## 💰 Análise Financeira (Simulada)

O projeto demonstra como **redução de risco operacional impacta diretamente custos**:

* Multa média por SLA quebrado: **R$ 1.500 / voo**
* Economia potencial anual estimada: **≈ R$ 1,69 milhão**

📌 Os valores são **fictícios**, porém baseados em práticas de contratos de SLA do setor aéreo.

---

## 🛠️ Tecnologias Utilizadas

* Python
* Pandas / NumPy
* Matplotlib / Seaborn
* Shell Script
* Git / GitHub
* Power BI (consumo dos dados)

---

## 📈 Diferenciais do Projeto

* Pensamento orientado a **negócio e finanças**, não apenas código
* Pipeline completo de engenharia de dados
* Simulação realista baseada em dados públicos
* Pronto para integração com BI corporativo
* Foco em **prevenção operacional**

---

## 👩‍💻 Autora

**Adila Zairaa**
Estudante de  Engenharia de Dados | Inteligência Operacional

Projeto desenvolvido para o **processo seletivo de Trainee – WFS**.

---

## 📌 Observação Final

Este repositório representa uma **prova de conceito**, demonstrando capacidade analítica, técnica e visão estratégica aplicada a operações aeroportuárias.
