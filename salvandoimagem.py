import shutil
from openai import OpenAI
from dotenv import load_dotenv
import os
import wget
load_dotenv()
 

class Image:
    def __init__(self, apiKey):
        
        client = OpenAI(
        api_key= apiKey
        )

        self.client = client
        self.apiKey = client.api_key

     
    def creat_image(self, promptImg):
        self.prompt = promptImg
        response = self.client.images.generate(
            model="dall-e-3",
            prompt= self.prompt,
            size="1024x1024",
            n=1,
        )
        print(response.data[0].url)

        self.imagemUrl = response.data[0].url

        return self.imagemUrl


    def save_image(self, nameImage):

        self.nameImage = nameImage
        image = f'{self.nameImage}.png'
        wget.download(self.imagemUrl, image)

        folder_path = "images"
        
        # Cria a pasta se ela não existir
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            
        # Move a imagem para a pasta de destino
        destination = os.path.join(folder_path, image)
        shutil.move(image, destination)
        
        print(f"\nImagem movida para: {destination}")

        return destination