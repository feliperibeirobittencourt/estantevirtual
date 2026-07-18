# -*- coding: utf-8 -*-
"""
Configurações do monitor. Ajuste aqui os filtros e as credenciais do Telegram.
"""
import os

# ---------------------------------------------------------------------------
# FILTROS DE BUSCA (validados com você)
# ---------------------------------------------------------------------------
PRECO_MIN_REAIS = 30          # preço mínimo em reais (evita reedições baratas)
PRECO_MAX_REAIS = 100000      # preço máximo em reais
TIPO_LIVRO = "usado"          # "usado", "novo" ou "" para ambos

# Ordenação: "new-releases" = últimos cadastrados (o que queremos)
ORDENACAO = "new-releases"

# Janela de anos para DESTACAR no relatório (o site não filtra intervalo,
# então filtramos aqui no script, lendo o ano de cada anúncio).
ANO_MIN = 1850
ANO_MAX = 1930

# Quantas páginas de resultados ler por autor (cada página ~ 44 itens).
# Como ordenamos por mais recentes, 1-2 páginas cobrem as novidades do dia.
PAGINAS_POR_AUTOR = 2

# Pausa (segundos) entre buscas, para uso civilizado do site.
PAUSA_ENTRE_BUSCAS = 4.0

# ---------------------------------------------------------------------------
# TELEGRAM (opcional — deixe TELEGRAM_ATIVO = False se não quiser)
# ---------------------------------------------------------------------------
TELEGRAM_ATIVO = False
# Quando quiser ativar: mude para True acima, e configure os dois valores
# abaixo (no Mac, cole direto aqui; no GitHub Actions, use "Secrets" — veja
# o GITHUB-PASSO-A-PASSO.md).
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "COLE_SEU_TOKEN_AQUI")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "COLE_SEU_CHAT_ID_AQUI")

# Se True, o Telegram avisa apenas achados dentro da janela de anos (1850-1930).
# Se False, avisa qualquer novidade nova, destacando os que estão na janela.
TELEGRAM_SO_JANELA_ANOS = False

# ---------------------------------------------------------------------------
# ARQUIVOS
# ---------------------------------------------------------------------------
ARQUIVO_HISTORICO = "historico.json"      # memória do que já foi visto
ARQUIVO_EXCEL = "achados_estante.xlsx"     # planilha de saída
