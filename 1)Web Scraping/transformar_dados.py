import os
import zipfile


def zippar(pasta_origem):
    arquivo_zip = pasta_origem + '.zip'

    #Verifica se a pasta existe antes de compactar
    if not os.path.exists(pasta_origem):
        print(f"Erro: A pata '{pasta_origem}' não existe")
        return

    with zipfile.ZipFile(arquivo_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(pasta_origem):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, pasta_origem))

    print(f"Pasta'{pasta_origem}' compactada com sucesso como '{arquivo_zip}'")


arquivo = 'pdfs'
zippar(arquivo)
