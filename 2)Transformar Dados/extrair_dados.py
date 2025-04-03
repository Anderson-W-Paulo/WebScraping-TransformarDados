import pdfplumber
import pandas as pd
import zipfile


class Extratorpdf:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.tabelas_extraidas = []
        self.coluna = None

    def extrair_tabelas(self):
        '''Extrair tabelas de todas as páginas do arquivo pdf'''
        with pdfplumber.open(self.pdf_path) as pdf:
            for num_pagina, pagina in enumerate(pdf.pages):
                print(f'Extraindo dados da página {num_pagina + 1}...')

                #Extrai tabelas da página
                tabelas = pagina.extract_tables()

                for tabela in tabelas:
                    if num_pagina == 2:
                        self.coluna = tabela[0]
                        self.tabelas_extraidas.append(tabela)
                    elif num_pagina > 0:
                        self.tabelas_extraidas.append(tabela[1:])

    def criar_dataframe(self):
        '''Converte os dados extraídos em um DataFrame do Pandas.'''
        if not self.tabelas_extraidas:
            print('Nenhuma tabela encontrada no PDF')

        #
        dados_completos = [linha for tabela in self.tabelas_extraidas for linha in tabela] #list comprehension

        # Criação do DataFrame
        df = pd.DataFrame(dados_completos, columns=self.coluna)
        return df

    def salvar_csv(self, output_file):
        '''Salva o DataFrame em um arquivo CSV.'''
        df = self.criar_dataframe()
        if df is not None:
            df.to_csv(output_file, index=False, sep=';', encoding='utf-8')
            print(f"Arquivo salvo com sucesso: {output_file}")


class Transformarcsv:
    def __init__(self, entrada_arquivo, saida_arquivo, nome_arquivo_zip):
        self.entrada_arquivo = entrada_arquivo
        self.saida_arquivo = saida_arquivo
        self.nome_arquivo_zip = nome_arquivo_zip
        pd.set_option('display.max_colwidth', None) #para impediri truncamento do conteúdo das colunas

    def processar_csv(self):

        try:
            df = pd.read_csv(self.entrada_arquivo, sep=';', encoding='utf-8')
            df = df.iloc[1:].reset_index(drop=True)

            #Renomear as colunas
            df = df.rename(columns={'OD': 'Seg. Odontológica', 'AMB': 'Seg. Ambulatorial'}, inplace=False)

            #substuti as abreviações OD, AMB
            abreciacoes = {'OD': 'Seg. Odontológica', 'AMB': 'Seg. Ambulatorial'}
            df[['Seg. Odontológica', 'Seg. Ambulatorial']] = df[['Seg. Odontológica', 'Seg. Ambulatorial']].replace(abreciacoes)

            #salva CSV modificado
            df.to_csv(self.saida_arquivo, sep=';', encoding='utf-8')
            print(f'Arquivo processado e salvo como {self.saida_arquivo}')
        except Exception as e:
            print(f'Erro! No processamento do CVS: {e}')

    def zippar_csv(self):

        try:
            with zipfile.ZipFile(self.nome_arquivo_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
                zipf.write(self.saida_arquivo, arcname=self.saida_arquivo.split('/')[-1])
                print(f'Arquivo compactado com sucesso: {self.saida_arquivo}')
        except Exception as e:
            print(f'Erro! Ao tentar compcatar CSV: {e}')


arquivo = "Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf"
extrator = Extratorpdf(arquivo)  # Instancia a classe
extrator.extrair_tabelas()  # Extrai as tabelas
extrator.salvar_csv("BancoDados.csv")  # Salva os dados extraídos


processor = Transformarcsv("BancoDados.csv", "BancoDados_modificado.csv", "zip_csv.zip")
processor.processar_csv()
processor.zippar_csv()
