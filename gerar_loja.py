import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin

urls = [
    "https://www.comprasparaguai.com.br/ar-condicionado-coby-cy-ac-inv-12k-12000btu-220v-50hz-inverter_185484/",
]

headers = {
    "User-Agent": "Mozilla/5.0"
}

os.makedirs("loja", exist_ok=True)

cards = ""

for i, url in enumerate(urls):
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    # ---------- TÍTULO ----------
    titulo = soup.find("h1")
    titulo = titulo.text.strip() if titulo else f"Produto {i}"

    # ---------- IMAGEM DO PRODUTO ----------
    img_url = ""

    img = soup.find("img", attrs={"itemprop": "image"})
    if img and img.get("src"):
        img_url = urljoin(url, img["src"])

    # ---------- ESPECIFICAÇÕES ----------
    specs = ""

    tabela = soup.find("table")
    if tabela:
        for tr in tabela.find_all("tr"):
            tds = tr.find_all("td")
            if len(tds) == 2:
                specs += f"<tr><td>{tds[0].text.strip()}</td><td>{tds[1].text.strip()}</td></tr>"

    # ---------- PÁGINA DO PRODUTO ----------
    produto_html = f"""
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <title>{titulo}</title>
    </head>
    <body>
        <h1>{titulo}</h1>

        <img src="{img_url}" width="400"><br><br>

        <table border="1" cellpadding="8">
            {specs}
        </table>

        <br>
        <a href="index.html">Voltar ao catálogo</a>
    </body>
    </html>
    """

    produto_file = f"produto_{i}.html"
    with open(f"loja/{produto_file}", "w", encoding="utf-8") as f:
        f.write(produto_html)

    # ---------- CARD DO CATÁLOGO ----------
    cards += f"""
    <div style="border:1px solid #ccc;padding:15px;margin:10px;width:250px;">
        <img src="{img_url}" width="220"><br>
        <strong>{titulo}</strong><br><br>
        <a href="{produto_file}">Ver produto</a>
    </div>
    """

# ---------- INDEX ----------
index_html = f"""
<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="UTF-8">
<title>Catálogo</title>
</head>
<body>

<h1>Catálogo de Ar Condicionado</h1>

<div style="display:flex;flex-wrap:wrap;">
{cards}
</div>

</body>
</html>
"""

with open("loja/index.html", "w", encoding="utf-8") as f:
    f.write(index_html)

print("✅ Loja criada com imagens reais!")

