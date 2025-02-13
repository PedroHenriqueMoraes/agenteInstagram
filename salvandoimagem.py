from openai import OpenAI
from dotenv import load_dotenv
import os
import wget
from agente01 import promptImg
from agente01 import nomeArquivo


load_dotenv()
client = OpenAI(
    api_key= os.getenv('OPENAI_API_KEY')
)

nomeImagem = 'post'

response = client.images.generate(
    model="dall-e-2",
    prompt= promptImg,
    size="512x512",
    quality="standard",
    n=1,
)

print(response.data[0].url)
imagemIA = response.data[0].url


imagem = f'{nomeArquivo}.png'


wget.download(imagemIA, imagem)