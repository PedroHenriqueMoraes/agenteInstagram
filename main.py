import re
from agente01 import CrewAgents
from salvandoimagem import Image
from postagemIG import User_instagram
import os
from dotenv import load_dotenv
load_dotenv()

chaveApi = os.getenv('OPENAI_API_KEY')
senha_IG = os.getenv('SENHA_IG')

equipe = CrewAgents()
equipe._initialize_agents()
equipe._initialize_taks()
equipe.createCrew()

#pegando as saidas
saida = equipe.formatted_output()

print('este é o prompt: ', saida['prompt'])
print()
print('este é o nome do arquivo: ',saida['nome_arquivo'])
print()
print('este é a descrição: ',saida['descricao'])

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

nomeImagemCorrigido = limpar_nome_arquivo(nome= saida['nome_arquivo'])


#savando imagem
imagemSalva = Image(apiKey= chaveApi)
imagemSalva.creat_image(promptImg = saida['prompt'])
caminhoImagem = imagemSalva.save_image(nameImage = nomeImagemCorrigido )



#criando usuario e postando
usuario = 'noticiadehoje135'
senha = senha_IG
postInstagram = User_instagram(user= usuario, password = senha)
postInstagram.post_Image(imagePath= caminhoImagem, description = saida['descricao'])