
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import re

from countries import countries
import pandas as pd

def scraping_cia():
    # Função para coletar dados de um país
    def get_country_data(country_url):
        fields = {
            "Country": country_url.split("/")[-2],  # Nome do país a partir da URL
            "Location": "",
            "Geographic coordinates": "",
            "Map references": "",
            "Area Total": "",
            "Area Land": "",
            "Area Water": "",
            "Climate": ""
        }


        try:
            # Acessando a página do país
            driver.get(country_url)
            time.sleep(5)  # Tempo para carregar a página

            geography_section = driver.find_element(By.ID, "geography")
            blocks = geography_section.find_elements(By.TAG_NAME, "div")

            for block in blocks:
                try:
                    title = block.find_element(By.TAG_NAME, "h3").text.strip()
                    content = block.find_element(By.TAG_NAME, "p").text.strip()

                    if title == "Location":
                        fields["Location"] = content

                    elif title == "Geographic coordinates":
                        fields["Geographic coordinates"] = content

                    elif title == "Map references":
                        fields["Map references"] = content

                    elif title == "Area":
                        # Extrai linhas específicas do campo 'Area'
                        total_match = re.search(r"total\s*:\s*([^\n]+)", content)
                        land_match = re.search(r"land\s*:\s*([^\n]+)", content)
                        water_match = re.search(r"water\s*:\s*([^\n]+)", content)

                        if total_match:
                            fields["Area Total"] = total_match.group(1).strip()
                        if land_match:
                            fields["Area Land"] = land_match.group(1).strip()
                        if water_match:
                            fields["Area Water"] = water_match.group(1).strip()

                    elif title == "Climate":
                        fields["Climate"] = content

                except:
                    continue

            return fields

        except Exception as e:
            print(f"Erro ao acessar {country_url}: {e}")

    # --- Configurações do Selenium ---
    driver = webdriver.Chrome()

    # Cria um DataFrame em pandas

    data_list = []

    for pais, country_name in countries.items():
        print(f"Coletando dados de {country_name}...")
        data = get_country_data(f'https://www.cia.gov/the-world-factbook/countries/{country_name}/')
        if data:
            data_list.append(data)

    driver.quit()

    return pd.DataFrame(data_list)
