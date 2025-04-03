import os
import requests
from bs4 import BeautifulSoup
#import transformar_dados


class Extrair:
    def __init__(self, site_url, anexos_desejados):
        self.site_url = site_url
        self.anx_desejados = anexos_desejados

    def baixar(self):
        #Getter arquivos
        resposta = requests.get(self.site_url)
        if resposta.status_code != 200:
            print('ERRO! Ao acessar a página')
            exit()  #Encessar execução

        #"Parseia" o html
        site_html = BeautifulSoup(resposta.text, 'html.parser')
        #print(site_html.prettify())

        #Econtra links PDF
        pdf_links = []
        for link in site_html.find_all('a', href=True):
            if '.pdf' in link['href']:
                pdf_url = link['href']
                print(pdf_url)
                if not (pdf_url.startswith('http') or pdf_url.startswith('https')):
                    pdf_url = self.site_url + pdf_url
                pdf_links.append(pdf_url)
        print('=' * 50)

        # Baixa os PDFs encontrados
        os.makedirs("pdfs", exist_ok=True)  # Cria pasta para salvar os PDFs
        for pdf_url in pdf_links:
            pdf_name = pdf_url.split("/")[-1]  # Nome do arquivo

            #Verificar se o nome do arquivo contém "Anexo I" ou "Anexo II"
            if any(anexo in pdf_name for anexo in self.anx_desejados):
                pdf_path = os.path.join("pdfs", pdf_name)  # combinar corretamente os caminhos
                try:
                    pdf_response = requests.get(pdf_url)
                    if pdf_response.status_code == 200:
                        with open(pdf_path, "wb") as file:
                            file.write(pdf_response.content)
                        print(f"Download concluído: {pdf_name}")
                    else:
                        print(f"Erro ao baixar {pdf_name} (Status Code: {pdf_response.status_code})")
                except requests.RequestException as e:
                    print(f'Erro ao tentar acessar {pdf_name} : {e}')

        print("Todos os downloads finalizados!")


site = 'https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos'
anx = ['Anexo_I', 'Anexo_II']
extrator = Extrair(site, anx)
extrator.baixar()

#Posso importar transformar_dados e chamar função zippar()