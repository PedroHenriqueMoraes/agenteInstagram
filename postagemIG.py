from instagrapi import Client
# from agente01 import generate_description
# from salvandoimagem import imagem


# Credenciais do Instagram
USERNAME = "new_news135"
PASSWORD = "news3504"

# Caminho da imagem e legenda
IMAGE_PATH = 'descoberta_dinossauro_novosensis.png'
CAPTION = 'Nova descoberta de DINO!!!'

# Inicializa o cliente do Instagram
cl = Client()

# Login no Instagram
cl.login(USERNAME, PASSWORD)

# Posta a imagem no feed
media = cl.photo_upload(IMAGE_PATH, CAPTION)

print(f"Postagem feita com sucesso! ID: {media.dict()['id']}")
