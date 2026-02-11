import os
import urllib.parse

# ================= CONFIGURAÇÃO =================
WHATSAPP_NUMERO = "5599999999999"  # troque pelo seu número
PASTA_BASE = os.getcwd()  # pasta atual
# ===============================================

HTML_INICIO = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="UTF-8">
<title>Catálogo de Ar-Condicionado</title>

<style>
body {
    font-family: Arial, sans-serif;
    margin: 0;
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    transition: background-image 1s ease-in-out;
}

h1 {
    text-align: center;
    background: rgba(255,255,255,0.9);
    padding: 20px;
    margin: 0;
}

.produto {
    background: white;
    width: 90%;
    margin: 20px auto;
    padding: 20px;
    border-radius: 10px;
    display: flex;
    gap: 20px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.2);
}

.produto img {
    width: 220px;
    border-radius: 10px;
}

.specs {
    white-space: pre-line;
    margin-bottom: 15px;
}

.whatsapp {
    display: inline-block;
    background: #25D366;
    color: white;
    padding: 10px 16px;
    border-radius: 6px;
    text-decoration: none;
    font-weight: bold;
}
.whatsapp:hover {
    background: #1ebc59;
}
</style>

<script>
const fundos = [
    "1.jpg",
    "2.jpg",
    "3.jpg",
    "4.jpg",
    "5.jpg"
];

let indice = 0;

function trocarFundo() {
    document.body.style.backgroundImage = `url('${fundos[indice]}')`;
    indice = (indice + 1) % fundos.length;
}

window.onload = () => {
    trocarFundo();
    setInterval(trocarFundo, 15000);
};
</script>

</head>
<body>

<h1>Catálogo de Ar-Condicionado</h1>
"""

HTML_FIM = """
</body>
</html>
"""

html_produtos = ""

# 🔍 Lê apenas pastas válidas
for pasta in sorted(os.listdir(PASTA_BASE)):
    caminho_pasta = os.path.join(PASTA_BASE, pasta)

    if not os.path.isdir(caminho_pasta):
        continue

    img_path = os.path.join(pasta, "imagem.jpg")
    spec_path = os.path.join(pasta, "especificacoes.txt")

    if not os.path.isfile(img_path) or not os.path.isfile(spec_path):
        continue

    with open(spec_path, "r", encoding="utf-8") as f:
        specs = f.read().strip()

    mensagem = f"Olá, quero mais informações sobre o {pasta}"
    mensagem_encoded = urllib.parse.quote(mensagem)
    whatsapp_link = f"https://wa.me/{WHATSAPP_NUMERO}?text={mensagem_encoded}"

    bloco = f"""
    <div class="produto">
        <img src="{img_path}">
        <div>
            <h2>{pasta}</h2>
            <div class="specs">{specs}</div>
            <a class="whatsapp" href="{whatsapp_link}" target="_blank">
                💬 Falar no WhatsApp
            </a>
        </div>
    </div>
    """

    html_produtos += bloco

html_final = HTML_INICIO + html_produtos + HTML_FIM

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_final)

print("✅ Catálogo criado com sucesso! Abra o arquivo index.html")
