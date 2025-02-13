from instagrapi import Client

class User_instagram:
    def __init__(self, user, password):
        self.user = user
        self.password = password
        
    
    def post_Image(self, imagePath, description):
        self.imagePath = imagePath
        self.description = description       
        # Credenciais do Instagram
        USERNAME = self.user
        PASSWORD = self.password

        # Caminho da imagem e legenda
        IMAGE_PATH = self.imagePath
        CAPTION =  self.description

        # Inicializa o cliente do Instagram
        cl = Client()

        # Login no Instagram
        cl.login(USERNAME, PASSWORD)

        # Posta a imagem no feed
        media = cl.photo_upload(IMAGE_PATH, CAPTION)

        print(f"Postagem feita com sucesso! ID: {media.dict()['id']}")
