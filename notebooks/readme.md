

# 🤖 Detecção de Imagens com YOLOv8 

Este repositório apresenta uma implementação de um modelo de **classificação de imagens** utilizando a arquitetura **YOLOv8**. O modelo foi treinado com um **dataset personalizado** utilizando o **Roboflow** e técnicas de *data augmentation* para aumentar a performance do modelo. Abaixo, explicamos detalhadamente o fluxo de trabalho, desde a configuração do ambiente até a inferência final.

## 🧰 Dependências

Antes de executar o notebook, instale as dependências necessárias. Elas incluem:

- **PyTorch**: Para o treinamento e inferência do modelo.
- **Ultralytics YOLO**: Biblioteca para uso da arquitetura YOLOv8.
- **Roboflow**: Plataforma para criar e gerenciar datasets.

### 📦 Instalação das Dependências

Você pode instalar as dependências utilizando `pip`:

```bash
pip install torch ultralytics roboflow
```

## 📝 Passos do Notebook

### 1. **Verificação da Instalação do PyTorch e CUDA** 🖥️

Primeiro, verificamos a instalação do PyTorch e se a **CUDA** (para aceleração com GPU) está disponível:

```python
import torch

print("Versão do PyTorch:", torch.__version__)
print("CUDA disponível:", torch.cuda.is_available())
if torch.cuda.is_available():
    print("Nome da GPU:", torch.cuda.get_device_name(0))
```

Este código imprime a versão do PyTorch, se a GPU está disponível para acelerar o treinamento e o nome da GPU utilizada.

### 2. **Importação do Dataset** 📥

O **dataset personalizado** utilizado para treinar o modelo é obtido via **Roboflow**. O dataset contém imagens da aplicação Tequila, com classes que ajudam a treinar o modelo para distinguir entre diferentes categorias de imagens.

```python
from roboflow import Roboflow

rf = Roboflow(api_key="vEk0o12j7gIkeAzeGObz")
project = rf.workspace("nuven").project("tequila")
version = project.version(3)
dataset = version.download("folder")
```

Aqui, a chave de API do Roboflow é usada para acessar o projeto chamado **tequila**, baixando a versão 3 do dataset.

### 3. **Treinamento do Modelo YOLOv8** 🔥

Carregamos o modelo **YOLOv8** pré-treinado e o utilizamos para treinar o modelo com o nosso **dataset personalizado**. O treinamento é realizado por 50 épocas.

```python
from ultralytics import YOLO

model = YOLO("yolov8n-cls.pt")  # Carregando o modelo YOLO pré-treinado
DATA_DIR = "CAMINHO-SEU-DATASET"

results = model.train(data=DATA_DIR, epochs=50, imgsz=640)  # Treinamento do modelo
```

### 4. **Inferência com o Modelo Treinado** 🔍

Após o treinamento, o modelo é carregado e utilizado para **fazer predições** em novas imagens. Abaixo, o modelo é carregado a partir do diretório onde os pesos finais são salvos, e uma imagem de teste é fornecida ao modelo para realizar a classificação.

```python
model = YOLO("runs/classify/train/weights/best.pt")
results = model.predict("CAMINHO-IMAGEM-EXEMPLO.jpg")
```

O código realiza a predição sobre uma imagem de teste. O resultado é extraído, e a classe prevista e a confiança da predição são calculadas:

```python
result = results[0]
class_names = result.names  
probs = result.probs.data.cpu().numpy()  

predicted_class_idx = probs.argmax()
predicted_class = class_names[predicted_class_idx]
confidence = probs[predicted_class_idx]

print(f"Classe Prevista: {predicted_class}")
print(f"Confiança: {confidence:.2f}")
```

### 5. **Saída Esperada** 🎯

Ao final da inferência, o código imprime a **classe prevista** e a **confiança** associada à predição. Por exemplo, se o modelo previu que a imagem corresponde a uma classe chamada "fechada", o modelo também informará o quão confiante ele está com a predição.

```
Classe Prevista: fechada
Confiança: 0.95
```

## 🛠️ Implementação Técnica

### 🧠 Técnicas Utilizadas:

- **Data Augmentation**: O dataset foi enriquecido utilizando as técnicas de aumento de dados fornecidas pelo **Roboflow**, como rotação, inversão, zoom e outras transformações geométricas e fotométricas. Isso permite que o modelo generalize melhor durante o treinamento, melhorando sua capacidade de identificar padrões em novas imagens.
  
- **YOLOv8**: Utilizamos a arquitetura YOLOv8, que é uma das mais avançadas para detecção de objetos e classificação de imagens. Ela oferece alta performance, mesmo com uma quantidade limitada de dados, devido ao seu poder de generalização e aceleração via GPU.

## 📈 Conclusão

Este notebook demonstra como treinar um modelo de classificação de imagens usando a arquitetura **YOLOv8** com um **dataset personalizado** obtido do **Roboflow**. Através do uso de técnicas avançadas de *data augmentation*, o modelo é capaz de realizar predições com alta confiança em novas imagens.

