import os
import requests
from bs4 import BeautifulSoup
import time

BASE = "https://www.comprasparaguai.com.br"
URL_BASE = "https://www.comprasparaguai.com.br/ar-condicionado/?page="

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def limpar_nome(nome):
    return "".join(c for c in nome if c.isalnum() or c in " _-").strip()

# ---------- PEGAR LINKS DOS PRODUTOS DA PÁGINA ----------
def baixar_categoria(pagina):
    url = URL_BASE + str(pagina)
    print(f"\n📄 Varredura da página {pagina}")

    r = requests.get(url, headers=headers, timeout=15)
    soup = BeautifulSoup(r.text, "html.parser")

    produtos = set()

    for a in soup.select("a[href*='ar-condicionado-']"):
        href = a.get("href")
        if href:
            produtos.add(BASE + href)

    return list(produtos)

# ---------- BAIXAR DADOS DO PRODUTO ----------
def baixar_produto(url):
    print("🔍 Produto:", url)

    r = requests.get(url, headers=headers, timeout=15)
    soup = BeautifulSoup(r.text, "html.parser")

    h1 = soup.find("h1")
    if not h1:
        return

    nome = h1.text.strip()
    pasta = limpar_nome(nome)

    os.makedirs(pasta, exist_ok=True)

    # ---------- IMAGEM CORRETA (og:image) ----------
    img_meta = soup.find("meta", property="og:image")

    if img_meta:
        img_url = img_meta.get("content")
        if img_url:
            img_data = requests.get(img_url, headers=headers).content
            with open(f"{pasta}/imagem.jpg", "wb") as f:
                f.write(img_data)

    # ---------- ESPECIFICAÇÕES ----------
    specs = ""
    tabela = soup.find("table")

    if tabela:
        for tr in tabela.find_all("tr"):
            tds = tr.find_all("td")
            if len(tds) == 2:
                specs += f"{tds[0].text.strip()}: {tds[1].text.strip()}\n"

    with open(f"{pasta}/especificacoes.txt", "w", encoding="utf-8") as f:
        f.write(specs)

    print("✅ Salvo:", pasta)

# ---------- LOOP PRINCIPAL ----------
def main():
    for pagina in range(2, 23):  # páginas 2 até 22
        links = baixar_categoria(pagina)
        print(f"➡️ Produtos encontrados: {len(links)}")

        for link in links:
            try:
                baixar_produto(link)
                time.sleep(1)  # evita bloqueio
            except Exception as e:
                print("❌ Erro:", e)

main()

