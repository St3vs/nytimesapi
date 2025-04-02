import requests
import json
import logging
import os
from datetime import datetime

# Configuração do logging
logging.basicConfig(filename="ficheiro.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

DATA_FILE = "dados.json"

# Carregar configurações do JSON
try:
    with open("config.json", "r") as f:
        config = json.load(f)

    API_KEY = config.get("API_KEY", "")
    URL = config.get("URL", "")

    if not API_KEY or not URL:
        raise ValueError("API_KEY ou URL não estão definidos corretamente no config.json")

except Exception as e:
    logging.error(f"Erro ao carregar config.json: {str(e)}")
    raise SystemExit(f"Erro ao carregar config.json: {str(e)}")

# Obter artigos da API do NYTimes
try:
    response = requests.get(URL, params={"api-key": API_KEY})
    response.raise_for_status()
    articles = response.json().get("results", [])
except requests.exceptions.RequestException as e:
    logging.error(f"Erro ao obter artigos: {e}")
    articles = []

# Carregar dados existentes
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        try:
            existing_data = json.load(file)
        except json.JSONDecodeError:
            existing_data = []
else:
    existing_data = []

existing_titles = {article["title"] for article in existing_data}
filtered_articles = [article for article in articles if article["title"] not in existing_titles]

# Salvar novos artigos
if filtered_articles:
    existing_data.extend(filtered_articles)
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(existing_data, file, ensure_ascii=False, indent=4)
    logging.info(f"{len(filtered_articles)} novos artigos adicionados. Total: {len(existing_data)}")
else:
    logging.info("Nenhum novo artigo encontrado.")
