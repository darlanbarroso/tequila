#!/bin/bash

# Variáveis
ACR_NAME="tequilaacr"  # Nome do seu Azure Container Registry
IMAGE_NAME="flask-yolo-api"
TAG=$(date +"%Y%m%d%H%M%S")  # Gera uma tag baseada na data e hora

# Build da imagem
echo "Building Docker image..."
sudo docker build -t $IMAGE_NAME .

# Tagging da imagem
echo "Tagging the image as $ACR_NAME.azurecr.io/$IMAGE_NAME:$TAG..."
sudo docker tag $IMAGE_NAME $ACR_NAME.azurecr.io/$IMAGE_NAME:$TAG

# Push para o ACR
echo "Pushing the image to Azure Container Registry..."
sudo docker push $ACR_NAME.azurecr.io/$IMAGE_NAME:$TAG

echo "Deploy completed!"
