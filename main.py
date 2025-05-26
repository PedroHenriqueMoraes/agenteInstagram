import re
import schedule
from agente01 import CrewAgents
from salvandoimagem import Image
from postagemIG import User_instagram
import os
from dotenv import load_dotenv
import time
load_dotenv()

def limpar_nome_arquivo(nome):
    # Lista de extensões comuns para remover
    extensoes = ['.jpg', '.jpeg', '.png', '.gif', '.svg', '.img', '.webp']
    
    # Converte para minúsculo para fazer a comparação
    nome = nome.lower()
    
    # Remove qualquer extensão da lista
    for ext in extensoes:
        if nome.endswith(ext):
            nome = nome[:-len(ext)]
    
    # Remove caracteres especiais e espaços extras
    nome = re.sub(r'[^\w\s-]', '', nome)
    nome = re.sub(r'\s+', '_', nome.strip())
    
    return nome

def job():
    chaveApi = os.getenv('OPENAI_API_KEY')
    senha_IG = os.getenv('SENHA_IG')


    #pegando as saidas
    equipe = CrewAgents()
    equipe._initialize_agents()
    equipe._initialize_taks()
    equipe.createCrew()
    saida = equipe.formatted_output()
    print('este é o prompt: ', saida['prompt'])
    print('este é o nome do arquivo: ',saida['nome_arquivo'])
    print('este é a descrição: ',saida['descricao'])

    nomeImagemCorrigido = limpar_nome_arquivo(nome= saida['nome_arquivo'])
    #savando imagem
    imagemSalva = Image(apiKey= os.getenv('OPENAI_API_KEY'))
    imagemSalva.creat_image(promptImg = saida['prompt'])
    caminhoImagem = imagemSalva.save_image(nameImage = nomeImagemCorrigido )


    #criando usuario e postando
    postInstagram = User_instagram(
        user= 'noticiadehoje135', 
        password = os.getenv('SENHA_IG'))
    
    postInstagram.post_Image(
        imagePath= caminhoImagem, 
        description = saida['descricao'])

def main():
    print("Iniciando o programa...")
    
    # schedule.every().day.at("12:00").do(job)
    job()
    
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)

if __name__ == "__main__":
    main()

