#!/bin/bash

ORIGEM="dados_origem"       # pasta onde os arquivos originais estão
DESTINO="dados"             # pasta onde os arquivos serão copiados
LOGDIR="logs"               # pasta de logs


mkdir -p "$DESTINO"
mkdir -p "$LOGDIR"


DATA=$(date +'%Y%m%d_%H%M%S')
LOGFILE="$LOGDIR/coleta_$DATA.log"

echo "[$(date)] Iniciando coleta de dados..." >> "$LOGFILE"


for ARQ in "$ORIGEM"/*.csv; do
    if [ -f "$ARQ" ]; then
        BASENAME=$(basename "$ARQ")
        NOVO_NOME="voos_$(date +'%Y%m%d_%H%M%S').csv"
        cp "$ARQ" "$DESTINO/$NOVO_NOME"
        
       
        if [ -s "$DESTINO/$NOVO_NOME" ]; then
            echo "[$(date)] Copiado: $ARQ → $DESTINO/$NOVO_NOME" >> "$LOGFILE"
        else
            echo "[$(date)] ERRO: arquivo vazio ou falha na cópia: $ARQ" >> "$LOGFILE"
        fi
    else
        echo "[$(date)] Nenhum arquivo encontrado em $ORIGEM" >> "$LOGFILE"
    fi
done

echo "[$(date)] Coleta de dados concluída." >> "$LOGFILE"
