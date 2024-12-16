from locust import HttpUser, task, between
import os
import base64
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

class TequilaApiUser(HttpUser):
    # Tempo entre as requisições, para simular um usuário real (de 1 a 3 segundos)
    wait_time = between(1, 3)
    
    # Lê os parâmetros do arquivo .env
    host = os.getenv("LOCUST_HOST", "http://localhost:5000")  # URL base
    username = os.getenv("LOCUST_USERNAME", "admin")  # Nome de usuário
    password = os.getenv("LOCUST_PASSWORD", "password123")  # Senha
    image_path = os.getenv("LOCUST_IMAGE", "1715279936313.jpg")  # Caminho da imagem

    def on_start(self):
        """Executado antes do início das tarefas, para gerar o cabeçalho de autenticação básica"""
        if not all([self.host, self.username, self.password, self.image_path]):
            raise ValueError("Todos os parâmetros devem ser fornecidos: host, username, password, image_path")
        
        self.auth_header = {
            "Authorization": "Basic " + base64.b64encode(f"{self.username}:{self.password}".encode('utf-8')).decode('utf-8')
        }

    @task(1)
    def predict(self):
        """Requisição para predição com a imagem fornecida"""
        if os.path.exists(self.image_path):
            with open(self.image_path, 'rb') as f:
                files = {'image': (self.image_path, f, 'image/jpeg')}
                
                # Envia a requisição POST com autenticação básica
                response = self.client.post("/classify", 
                                            headers=self.auth_header,  # Usando o cabeçalho de autenticação
                                            files=files)

            # Validação da resposta
            if response.status_code == 200:
                print("Predição realizada com sucesso.")
                print(response.json())  # Imprime a resposta da predição para análise
            else:
                print(f"Erro: {response.status_code}")
                print(response.text)  # Exibe a resposta de erro para depuração
        else:
            print(f"Imagem não encontrada no caminho: {self.image_path}")
    
    @task(2)
    def health_check(self):
        """Requisição para verificar a saúde da API"""
        response = self.client.get("/health", 
                                   headers=self.auth_header)  # Usando o cabeçalho de autenticação
        if response.status_code != 200:
            print(f"Erro no health check: {response.status_code}")
        else:
            print("API funcionando corretamente.")
