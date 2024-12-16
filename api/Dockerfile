# Imagem base com Python
FROM python:3.10-slim

# Atualizar e instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && apt-get clean

# Configurar diretório de trabalho
WORKDIR /app

# Copiar arquivos do projeto para o contêiner
COPY . /app

# Instalar PyTorch primeiro (versão CPU)
RUN pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu

# Instalar dependências do projeto
RUN pip install -r requirements.txt

# Expor a porta usada pela API Flask
EXPOSE 5000

# Comando para iniciar a API
CMD ["python", "app.py"]
