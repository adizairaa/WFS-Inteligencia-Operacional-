#!/bin/bash

# -----------------------------------------
# Shell Script: executar_pipeline.sh
# Objetivo: executar pipeline completo WFS Inteligência Operacional
# -----------------------------------------

# Diretórios
LOGDIR="logs"
mkdir -p "$LOGDIR"

# Arquivo de log com timestamp
DATA=$(date +'%Y%m%d_%H%M%S')
LOGFILE="$LOGDIR/pipeline_$DATA.log"

echo "[$(date)] Iniciando pipeline completo..." >> "$LOGFILE"

# -----------------------------------------
# Passo 1: Ativar ambiente virtual
# -----------------------------------------
echo "[$(date)] Ativando ambiente virtual..." >> "$LOGFILE"
source /c/Users/User/Desktop/wfs_inteligencia_operacional/.venv/Scripts/activate

if [ $? -ne 0 ]; then
    echo "[$(date)] ERRO: falha ao ativar ambiente virtual." >> "$LOGFILE"
    exit 1
fi

# -----------------------------------------
# Passo 2: Coleta e preparação de dados
# -----------------------------------------
echo "[$(date)] Executando coleta de dados..." >> "$LOGFILE"
bash shell_scripts/coleta_dados.sh >> "$LOGFILE" 2>&1

if [ $? -ne 0 ]; then
    echo "[$(date)] ERRO: falha na coleta de dados." >> "$LOGFILE"
    exit 1
fi

# -----------------------------------------
# Passo 3: Executar análise Python
# -----------------------------------------
echo "[$(date)] Executando análise Python (main.py)..." >> "$LOGFILE"
python src/main.py >> "$LOGFILE" 2>&1

if [ $? -eq 0 ]; then
    echo "[$(date)] Pipeline concluído com sucesso." >> "$LOGFILE"
else
    echo "[$(date)] ERRO: falha na execução do pipeline Python." >> "$LOGFILE"
    exit 1
fi

echo "[$(date)] Pipeline finalizado." >> "$LOGFILE"
