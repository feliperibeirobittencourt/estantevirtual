# -*- coding: utf-8 -*-
"""
Monitor de novidades no Estante Virtual — por autor, com filtros.

O QUE FAZ:
  1. Abre um navegador real (Playwright) na SUA máquina.
  2. Para cada autor, abre a busca já com filtros (usados, preço, mais recentes).
  3. Lê os resultados da página (título, autor, ano, preço, link).
  4. Compara com a rodada anterior (historico.json) e identifica o que é NOVO.
  5. Salva uma planilha Excel com duas abas: "Novidades de hoje" e "Histórico".
  6. (Opcional) Manda no Telegram só os achados novos.

COMO RODAR (depois de instalar — veja README):
  python monitor.py

IMPORTANTE:
  - Este script usa um navegador de verdade, na sua máquina, com seu IP.
    É uso legítimo e no seu ritmo. Não contém nenhuma técnica de "evasão"
    de proteção anti-bot. Se algum dia o site bloquear a automação mesmo
    assim, a resposta correta é parar, não tentar driblar.
  - Rode no máximo 1x por dia.
"""

import json
import time
import re
import os
import sys
import unicodedata
from datetime import datetime
from urllib.parse import quote

import requests
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill, Alignment
from playwright.sync_api import sync_playwright

import config
from autores import TODOS


# ---------------------------------------------------------------------------
# Utilidades
# ---------------------------------------------------------------------------

def slug_autor(nome: str) -> str:
    """Converte 'Álvares de Azevedo' -> 'alvares-de-azevedo' (formato do site)."""
    # remove parênteses e conteúdo
    limpo = re.sub(r"\s*\([^)]*\)", "", nome).strip()
    # remove acentos
    nfkd = unicodedata.normalize("NFD", limpo)
    sem_acento = "".join(c for c in nfkd if unicodedata.category(c) != "Mn")
    sem_acento = re.sub(r"[^a-zA-Z0-9\s-]", "", sem_acento)
    return re.sub(r"\s+", "-", sem_acento.strip()).lower()


def monta_url(nome: str, pagina: int = 1) -> str:
    """
    Monta a URL de busca.

    DESCOBERTA IMPORTANTE (18/07/2026): o campo correto para buscar por autor
    é searchField=autor (não "titulo-autor" com um parâmetro extra "&autor=").
    Usar searchField=autor sozinho já filtra certinho pelos livros do autor,
    sem precisar de mais nada — e sem o problema de zerar resultados para
    autores menos populares que não tinham o campo "autor" (do outro modo)
    marcado no anúncio.
    """
    q = quote(nome)
    preco_min = config.PRECO_MIN_REAIS * 100      # site usa centavos
    preco_max = config.PRECO_MAX_REAIS * 100
    url = (
        f"https://www.estantevirtual.com.br/busca"
        f"?q={q}"
        f"&searchField=autor"
        f"&sort={config.ORDENACAO}"
        f"&_preco={preco_min}-{preco_max}"
    )
    if config.TIPO_LIVRO:
        url += f"&tipo-de-livro={config.TIPO_LIVRO}"
    if pagina > 1:
        url += f"&page={pagina}"
    return url


def extrai_ano(texto: str):
    """Tenta achar um ano de 4 dígitos (18xx/19xx) no texto do anúncio."""
    if not texto:
        return None
    m = re.findall(r"\b(1[6-9]\d{2}|20\d{2})\b", texto)
    if m:
        # pega o primeiro ano plausível
        return int(m[0])
    return None


def extrai_preco(texto: str):
    """Extrai o preço em reais a partir de um texto tipo 'R$ 45,00'."""
    if not texto:
        return None
    m = re.search(r"R\$\s*([\d\.]+),(\d{2})", texto)
    if m:
        inteiro = m.group(1).replace(".", "")
        return float(f"{inteiro}.{m.group(2)}")
    return None


# ---------------------------------------------------------------------------
# Leitura de uma página de busca
# ---------------------------------------------------------------------------

def le_resultados_da_pagina(page):
    """
    Lê os cartões de produto da página atual.
    Retorna lista de dicts: {titulo, autor, ano, preco, link}.

    NOTA DE MANUTENÇÃO: se o site mudar o HTML, os seletores abaixo podem
    quebrar. É aqui que o ajuste normalmente é necessário. Os seletores
    tentam ser tolerantes, mas confira no navegador (inspecionar elemento)
    caso a leitura pare de encontrar itens.
    """
    resultados = []

    # espera os cartões carregarem (o site é JS; precisa aguardar render)
    try:
        page.wait_for_selector("a[href*='/livros/']", timeout=8000)
    except Exception:
        return resultados  # nenhuma correspondência ou página vazia

    # cada produto costuma estar dentro de um link para /livros/
    cards = page.query_selector_all("a[href*='/livros/']")
    vistos = set()
    for card in cards:
        try:
            link = card.get_attribute("href") or ""
            if not link or link in vistos:
                continue
            vistos.add(link)
            if link.startswith("/"):
                link = "https://www.estantevirtual.com.br" + link

            # texto completo do cartão (título, autor, ano, preço costumam estar aqui)
            texto = card.inner_text().strip()
            if not texto:
                continue

            linhas = [l.strip() for l in texto.split("\n") if l.strip()]
            titulo = linhas[0] if linhas else ""
            ano = extrai_ano(texto)
            preco = extrai_preco(texto)

            resultados.append({
                "titulo": titulo,
                "texto": texto,
                "ano": ano,
                "preco": preco,
                "link": link,
            })
        except Exception:
            continue

    return resultados


# ---------------------------------------------------------------------------
# Histórico (memória entre rodadas)
# ---------------------------------------------------------------------------

def carrega_historico():
    if os.path.exists(config.ARQUIVO_HISTORICO):
        try:
            with open(config.ARQUIVO_HISTORICO, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def salva_historico(hist):
    with open(config.ARQUIVO_HISTORICO, "w", encoding="utf-8") as f:
        json.dump(hist, f, ensure_ascii=False, indent=2)


# ---------------------------------------------------------------------------
# Telegram
# ---------------------------------------------------------------------------

def envia_telegram(mensagem: str):
    if not config.TELEGRAM_ATIVO:
        return
    if "COLE_SEU" in config.TELEGRAM_TOKEN or "COLE_SEU" in str(config.TELEGRAM_CHAT_ID):
        print("  [Telegram] Token/chat_id não configurados — pulando envio.")
        return
    try:
        url = f"https://api.telegram.org/bot{config.TELEGRAM_TOKEN}/sendMessage"
        requests.post(url, data={
            "chat_id": config.TELEGRAM_CHAT_ID,
            "text": mensagem,
            "parse_mode": "HTML",
            "disable_web_page_preview": True,
        }, timeout=20)
    except Exception as e:
        print(f"  [Telegram] Falha ao enviar: {e}")


# ---------------------------------------------------------------------------
# Excel
# ---------------------------------------------------------------------------

def salva_excel(novidades, todos_de_hoje):
    """
    novidades: lista de dicts que são NOVOS nesta rodada
    todos_de_hoje: lista de dicts com tudo lido hoje (para o histórico)
    """
    hoje = datetime.now().strftime("%Y-%m-%d %H:%M")

    # se o arquivo já existe, abre para acrescentar ao histórico
    if os.path.exists(config.ARQUIVO_EXCEL):
        wb = load_workbook(config.ARQUIVO_EXCEL)
    else:
        wb = Workbook()
        wb.remove(wb.active)  # remove a aba padrão vazia

    # --- Aba de novidades (recriada a cada rodada) ---
    nome_aba_novidades = "Novidades de hoje"
    if nome_aba_novidades in wb.sheetnames:
        del wb[nome_aba_novidades]
    ws_nov = wb.create_sheet(nome_aba_novidades, 0)

    cabecalho = ["Autor", "Grupo", "Título", "Ano", "Preço (R$)", "Na janela 1850-1930?", "Link", "Visto em"]
    ws_nov.append(cabecalho)
    for c in range(1, len(cabecalho) + 1):
        cel = ws_nov.cell(row=1, column=c)
        cel.font = Font(name="Arial", bold=True, color="FFFFFF")
        cel.fill = PatternFill("solid", fgColor="7A3B2E")
        cel.alignment = Alignment(horizontal="center")

    for item in novidades:
        na_janela = "SIM" if (item.get("ano") and config.ANO_MIN <= item["ano"] <= config.ANO_MAX) else ""
        ws_nov.append([
            item.get("autor_busca", ""),
            item.get("grupo", ""),
            item.get("titulo", ""),
            item.get("ano", ""),
            item.get("preco", ""),
            na_janela,
            item.get("link", ""),
            hoje,
        ])

    # destaca linhas que estão na janela de anos
    for row in range(2, ws_nov.max_row + 1):
        if ws_nov.cell(row=row, column=6).value == "SIM":
            for col in range(1, len(cabecalho) + 1):
                ws_nov.cell(row=row, column=col).fill = PatternFill("solid", fgColor="EEF1E8")

    # largura de colunas
    larguras = [22, 10, 45, 8, 12, 20, 50, 16]
    for i, w in enumerate(larguras, start=1):
        ws_nov.column_dimensions[chr(64 + i)].width = w

    # --- Aba de histórico (acumula tudo, nunca apaga) ---
    nome_aba_hist = "Histórico"
    if nome_aba_hist not in wb.sheetnames:
        ws_hist = wb.create_sheet(nome_aba_hist)
        ws_hist.append(cabecalho)
        for c in range(1, len(cabecalho) + 1):
            cel = ws_hist.cell(row=1, column=c)
            cel.font = Font(name="Arial", bold=True, color="FFFFFF")
            cel.fill = PatternFill("solid", fgColor="2B2620")
            cel.alignment = Alignment(horizontal="center")
        for i, w in enumerate(larguras, start=1):
            ws_hist.column_dimensions[chr(64 + i)].width = w
    else:
        ws_hist = wb[nome_aba_hist]

    # acrescenta as novidades ao histórico
    for item in novidades:
        na_janela = "SIM" if (item.get("ano") and config.ANO_MIN <= item["ano"] <= config.ANO_MAX) else ""
        ws_hist.append([
            item.get("autor_busca", ""),
            item.get("grupo", ""),
            item.get("titulo", ""),
            item.get("ano", ""),
            item.get("preco", ""),
            na_janela,
            item.get("link", ""),
            hoje,
        ])

    wb.save(config.ARQUIVO_EXCEL)


# ---------------------------------------------------------------------------
# Programa principal
# ---------------------------------------------------------------------------

def main():
    print("=" * 60)
    print("Monitor Estante Virtual —", datetime.now().strftime("%d/%m/%Y %H:%M"))
    print("=" * 60)

    historico = carrega_historico()
    novidades = []
    total_lidos = 0

    # Permite testar com poucos autores (via variável de ambiente LIMITE_AUTORES),
    # em vez de rodar os 81 de uma vez enquanto ainda estamos ajustando o script.
    limite = int(os.environ.get("LIMITE_AUTORES", str(len(TODOS))))
    lista_autores = TODOS[:limite]
    if limite < len(TODOS):
        print(f"[modo teste] rodando só os primeiros {limite} de {len(TODOS)} autores")

    pasta_debug = "debug"
    os.makedirs(pasta_debug, exist_ok=True)

    with sync_playwright() as p:
        # No Mac (headless=False) você vê a janela do navegador trabalhando.
        # No GitHub Actions não existe tela, então detectamos automaticamente
        # (o GitHub define a variável de ambiente CI=true) e rodamos "invisível".
        rodando_no_github = os.environ.get("CI", "").lower() == "true"
        navegador = p.chromium.launch(headless=rodando_no_github)
        contexto = navegador.new_context(
            locale="pt-BR",
            user_agent=("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/120.0 Safari/537.36"),
        )
        page = contexto.new_page()

        for idx, (nome, grupo) in enumerate(lista_autores, start=1):
            print(f"[{idx:02d}/{len(lista_autores)}] {nome} ({grupo})...", end=" ", flush=True)
            chave_autor = slug_autor(nome)
            vistos_antes = set(historico.get(chave_autor, []))
            novos_deste_autor = []

            for pagina in range(1, config.PAGINAS_POR_AUTOR + 1):
                url = monta_url(nome, pagina)
                try:
                    page.goto(url, timeout=30000, wait_until="domcontentloaded")
                except Exception as e:
                    print(f"(erro ao abrir: {e})", end=" ")
                    continue

                itens = le_resultados_da_pagina(page)
                total_lidos += len(itens)

                # DIAGNÓSTICO: se mesmo com o fallback não achou nada, salva
                # print + HTML da página para conseguirmos ver depois o que
                # o robô realmente recebeu (pode ser genuinamente sem estoque,
                # ou pode ser algum bloqueio/erro que ainda não identificamos).
                if len(itens) == 0:
                    try:
                        base = f"{pasta_debug}/{idx:02d}_{chave_autor}_p{pagina}"
                        page.screenshot(path=f"{base}.png", full_page=True)
                        with open(f"{base}.html", "w", encoding="utf-8") as f:
                            f.write(page.content())
                    except Exception as e:
                        print(f"(falha ao salvar diagnóstico: {e})", end=" ")

                for item in itens:
                    # identificador único do anúncio = link
                    ident = item["link"]
                    if ident in vistos_antes:
                        continue  # já tínhamos visto
                    # é novo!
                    item["autor_busca"] = nome
                    item["grupo"] = grupo
                    novos_deste_autor.append(item)

                time.sleep(config.PAUSA_ENTRE_BUSCAS)

            # atualiza histórico deste autor (une antigos + novos)
            todos_ident = list(vistos_antes) + [i["link"] for i in novos_deste_autor]
            historico[chave_autor] = todos_ident

            novidades.extend(novos_deste_autor)
            print(f"{len(novos_deste_autor)} novo(s)")

        navegador.close()

    # salva memória e planilha
    salva_historico(historico)
    salva_excel(novidades, None)

    print("-" * 60)
    print(f"Total de anúncios lidos: {total_lidos}")
    print(f"Novidades nesta rodada: {len(novidades)}")

    # Telegram
    if novidades:
        na_janela = [n for n in novidades
                     if n.get("ano") and config.ANO_MIN <= n["ano"] <= config.ANO_MAX]
        alvo = na_janela if config.TELEGRAM_SO_JANELA_ANOS else novidades

        if alvo:
            linhas = [f"📚 <b>{len(alvo)} novidade(s) no Estante Virtual</b>", ""]
            for n in alvo[:30]:  # limita a 30 por mensagem
                ano = n.get("ano") or "?"
                preco = f"R$ {n['preco']:.2f}" if n.get("preco") else "?"
                marca = " ⭐" if (n.get("ano") and config.ANO_MIN <= n["ano"] <= config.ANO_MAX) else ""
                linhas.append(f"• <b>{n['autor_busca']}</b>{marca} — {n['titulo']} ({ano}, {preco})\n{n['link']}")
            if len(alvo) > 30:
                linhas.append(f"\n… e mais {len(alvo) - 30}. Veja a planilha.")
            envia_telegram("\n".join(linhas))
            print(f"Telegram: avisado sobre {len(alvo)} achado(s).")
    else:
        print("Nenhuma novidade — nada enviado ao Telegram.")

    print(f"Planilha salva em: {config.ARQUIVO_EXCEL}")
    print("Concluído.")


if __name__ == "__main__":
    main()
