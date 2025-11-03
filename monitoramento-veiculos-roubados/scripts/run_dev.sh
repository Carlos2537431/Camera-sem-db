#!/bin/bash

# Ativar o ambiente virtual, se necessário
# source venv/bin/activate

# Executar o servidor em modo de desenvolvimento
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload --log-level info