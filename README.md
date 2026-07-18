# Monitor Estante Virtual

Script que verifica, uma vez por dia, se apareceram livros novos dos seus
81 autores no Estante Virtual — filtrando por usados, preço acima de R$30, e
ordenando pelos mais recentes. Gera uma planilha Excel com as novidades + um
histórico acumulado, e (opcionalmente) te avisa no Telegram quando acha algo.

Roda **no seu Mac**, com o **seu** navegador — é uso legítimo do site, no seu
ritmo. Não contém técnicas para driblar bloqueios; se o site um dia barrar a
automação mesmo assim, o certo é parar, não contornar.

---

## 1. Instalação (só na primeira vez)

Abra o aplicativo **Terminal** no Mac (Cmd+Espaço, digite "Terminal", Enter).
Cole os comandos abaixo, um de cada vez:

### a) Instalar o Python (se ainda não tiver)
O macOS moderno já vem com Python 3. Confira digitando:
```
python3 --version
```
Se aparecer algo como `Python 3.11.x`, está ok. Se não, baixe em python.org.

### b) Entrar na pasta do projeto
Supondo que você colocou a pasta em Downloads:
```
cd ~/Downloads/estante-monitor
```

### c) Criar um ambiente isolado e instalar as dependências
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
playwright install chromium
```
O último comando baixa o navegador que o script controla (~150 MB). Demora um
pouco na primeira vez.

---

## 2. Configurar o Telegram (opcional, mas recomendado)

Se você quer receber avisos no celular:

1. No Telegram, procure por **@BotFather** e mande `/newbot`.
2. Siga as instruções (dê um nome e um usuário ao bot). No final, ele te dá um
   **token** parecido com `123456789:ABCdef...`. Copie.
3. Descubra seu **chat id**: procure por **@userinfobot** no Telegram e mande
   qualquer mensagem. Ele responde com seu `Id` (um número).
4. Abra o arquivo `config.py` num editor de texto e cole os dois valores em:
   ```python
   TELEGRAM_TOKEN = "seu_token_aqui"
   TELEGRAM_CHAT_ID = "seu_numero_aqui"
   ```
5. Mande uma mensagem qualquer para o seu bot (procure pelo nome dele e diga
   "oi") — isso é necessário para ele conseguir te responder.

Se não quiser Telegram, deixe `TELEGRAM_ATIVO = False` no `config.py`.

---

## 3. Rodar

Toda vez que quiser checar (com o ambiente ativado — passo 1c):
```
cd ~/Downloads/estante-monitor
source venv/bin/activate
python monitor.py
```

Uma janela do navegador vai abrir e percorrer os autores sozinha. Ao terminar:
- A planilha `achados_estante.xlsx` é atualizada (abas "Novidades de hoje" e
  "Histórico").
- Se configurado, o Telegram recebe os achados novos (⭐ marca os que estão na
  janela 1850–1930).

A primeira rodada vai marcar **tudo** como novidade (é a linha de base). A partir
da segunda, só mostra o que apareceu desde a última vez.

---

## 4. Rodar automático todo dia (opcional)

Para rodar sozinho, ex. todo dia às 9h, use o agendador do macOS (`launchd`) ou
o mais simples: o app **Automator** / **Atalhos** com um gatilho de horário que
executa o comando do passo 3. Peça ajuda para configurar isso quando quiser —
depende da versão do seu macOS.

---

## 5. Ajustes que você pode fazer sozinho

Tudo no `config.py`:
- `PRECO_MIN_REAIS` / `PRECO_MAX_REAIS` — faixa de preço.
- `ANO_MIN` / `ANO_MAX` — janela de anos destacada (1850–1930).
- `TIPO_LIVRO` — "usado", "novo" ou "" para ambos.
- `PAGINAS_POR_AUTOR` — quantas páginas ler por autor.
- `PAUSA_ENTRE_BUSCAS` — segundos entre buscas (mantenha ≥ 3 para uso civilizado).

Para adicionar/remover autores, edite `autores.py`.

---

## 6. Quando quebrar

O Estante Virtual muda o site de tempos em tempos. Quando isso acontecer, o
script provavelmente vai parar de encontrar resultados (vai dizer "0 novo(s)"
para todos). O ponto que costuma precisar de ajuste é a função
`le_resultados_da_pagina()` no `monitor.py` — especificamente os "seletores"
de HTML. Um programador resolve isso rápido, ou me traga o novo HTML da página
e eu ajudo a corrigir.

---

## Aviso

Use com parcimônia (1x/dia). O objetivo é acompanhar novidades para sua coleção
pessoal, não sobrecarregar o site. Bom garimpo!
