#!/bin/bash

LOGDIR="logs"
mkdir -p "$LOGDIR"


DATA=$(date +'%Y%m%d_%H%M%S')
LOGFILE="$LOGDIR/pipeline_$DATA.log"

echo "[$(date)] Iniciando pipeline completo..." >> "$LOGFILE"

-
echo "[$(date)] Ativando ambiente virtual..." >> "$LOGFILE"
source /c/Users/User/Desktop/wfs_inteligencia_operacional/.venv/Scripts/activate

if [ $? -ne 0 ]; then
    echo "[$(date)] ERRO: falha ao ativar ambiente virtual." >> "$LOGFILE"
    exit 1
fi

echo "[$(date)] Executando coleta de dados..." >> "$LOGFILE"
bash shell_scripts/coleta_dados.sh >> "$LOGFILE" 2>&1

if [ $? -ne 0 ]; then
    echo "[$(date)] ERRO: falha na coleta de dados." >> "$LOGFILE"
    exit 1
fi

echo "[$(date)] Executando análise Python (main.py)..." >> "$LOGFILE"
python src/main.py >> "$LOGFILE" 2>&1

if [ $? -eq 0 ]; then
    echo "[$(date)] Pipeline concluído com sucesso." >> "$LOGFILE"
else
    echo "[$(date)] ERRO: falha na execução do pipeline Python." >> "$LOGFILE"
    exit 1
fi

echo "[$(date)] Pipeline finalizado." >> "$LOGFILE"
