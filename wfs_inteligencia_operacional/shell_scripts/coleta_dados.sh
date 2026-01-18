#!/bin/bash

# -----------------------------------------
# Shell Script: coleta_dados.sh
# Objetivo: coletar e preparar arquivos de dados
# -----------------------------------------

# Configurações de diretório
ORIGEM="dados_origem"       # pasta onde os arquivos originais estão
DESTINO="dados"             # pasta onde os arquivos serão copiados
LOGDIR="logs"               # pasta de logs

# Criar diretórios se não existirem
mkdir -p "$DESTINO"
mkdir -p "$LOGDIR"

# Criar arquivo de log com timestamp
DATA=$(date +'%Y%m%d_%H%M%S')
LOGFILE="$LOGDIR/coleta_$DATA.log"

echo "[$(date)] Iniciando coleta de dados..." >> "$LOGFILE"

# Loop para copiar todos os CSVs da origem
for ARQ in "$ORIGEM"/*.csv; do
    if [ -f "$ARQ" ]; then
        BASENAME=$(basename "$ARQ")
        NOVO_NOME="voos_$(date +'%Y%m%d_%H%M%S').csv"
        cp "$ARQ" "$DESTINO/$NOVO_NOME"
        
        # Validar se o arquivo foi copiado e tem tamanho > 0
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
