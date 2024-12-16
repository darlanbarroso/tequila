

# 🥃 Projeto Tequila: API de Predição com YOLOv5 🤖

O **Projeto Tequila** é uma solução completa para a detecção e classificação de imagens utilizando o modelo **YOLOv5**. O sistema oferece uma API baseada em **Flask** para processar imagens e prever se uma imagem representa uma classe "aberta" ou "fechada". O projeto também inclui funcionalidades para treinar e validar o modelo, além de uma interface para realizar testes de carga e deploy em ambientes como **Azure**.

---

## 📂 Estrutura do Projeto

O projeto é dividido em várias pastas e arquivos para diferentes funcionalidades:

```
.
├── api                         # API Flask para predição de imagens
│   ├── app.py                  # Código principal da API Flask
│   ├── best.pt                 # Modelo treinado YOLOv5
│   ├── deploy.sh               # Script para deploy no servidor
│   ├── Dockerfile              # Arquivo para construir a imagem Docker
│   ├── docs                    # Documentação adicional sobre Docker e Azure
│   │   └── dockerAzure.md
│   ├── readme.md               # Este arquivo
│   ├── requirements.txt        # Dependências da API
│   ├── static                  # Arquivos estáticos (JS, CSS)
│   │   ├── script.js
│   │   └── styles.css
│   └── templates               # Arquivos HTML (Front-end)
│       └── index.html
├── assets                      # Imagens e outros ativos do projeto
│   └── Augmentation.png
├── data                        # Scripts relacionados ao dataset
│   ├── download_data.py        # Script para baixar e preparar dados
│   ├── readme.md               # Informações sobre o dataset
│   └── requirements.txt        # Dependências para processamento de dados
├── notebooks                   # Notebooks para treinamento e análise
│   ├── model_training.ipynb    # Notebook de treinamento do modelo
│   └── readme.md               # Explicação sobre o treinamento do modelo
├── readme.md                   # Este arquivo
└── scripts                     # Scripts auxiliares e ferramentas de teste
    ├── 1715279936313.jpg       # Exemplo de imagem
    ├── locustfile.py           # Arquivo de teste de carga
    ├── readme.md               # Informações sobre os testes
    └── requirements.txt        # Dependências para testes
```

---

## 🚀 Funcionalidades do Projeto

### 1. **API de Predição de Imagens com YOLOv5**

A API Flask oferece um endpoint para enviar imagens e obter uma previsão sobre a classe da imagem ("aberta" ou "fechada"). A predição é feita utilizando um modelo **YOLOv5** treinado previamente.

- **Endpoint `/predict`**: Recebe uma imagem, processa e retorna a previsão.
- **Endpoint `/health`**: Verifica se a API está funcionando corretamente.
- **Autenticação**: Requer autenticação básica com nome de usuário e senha, configurados nas variáveis de ambiente `API_USERNAME` e `API_PASSWORD`.

### 2. **Treinamento do Modelo**

O modelo YOLOv5 foi treinado para classificar imagens nas classes "aberta" e "fechada". O treinamento foi feito usando um conjunto de dados customizado do **Roboflow**, e o modelo resultante (`best.pt`) é utilizado na API para fazer as predições.

- **Notebook `model_training.ipynb`**: Contém o código para treinar o modelo utilizando o conjunto de dados.
- **Script `download_data.py`**: Baixa e prepara o conjunto de dados para treinamento.

### 3. **Teste de Carga com Locust**

Utilizamos o **Locust** para realizar testes de carga na API. O arquivo `locustfile.py` define o comportamento dos usuários simulados que interagem com a API, permitindo testar como a API se comporta sob carga.

- **Arquivo `locustfile.py`**: Define o comportamento do teste de carga.
- **Comando de execução**: `locust -f locustfile.py --host=http://localhost:5000`

### 4. **Deploy no Azure (opcional)**

O projeto inclui a documentação para realizar o deploy da API no **Azure** utilizando Docker. A configuração para isso está no arquivo `dockerAzure.md`, localizado na pasta `docs`.

---

## 🛠 Como Usar

### 1. **Configuração da API**

1. **Instalação das dependências**:

   Instale as dependências do projeto utilizando o `requirements.txt`:

   ```bash
   pip install -r api/requirements.txt
   ```

2. **Configuração das variáveis de ambiente**:

   Crie um arquivo `.env` na raiz do projeto e defina as variáveis de ambiente necessárias, como nome de usuário e senha para autenticação básica:

   ```env
   API_USERNAME=admin
   API_PASSWORD=password123
   ```

3. **Rodando a API localmente**:

   Para rodar a API localmente, execute o comando abaixo:

   ```bash
   python api/app.py
   ```

   A API estará disponível em `http://localhost:5000`.

### 2. **Fazendo uma Requisição de Predição**

Você pode enviar uma imagem para o endpoint `/predict` usando o comando `curl`:

```bash
curl -u admin:password123 -F "image=@/caminho/para/imagem.jpg" http://localhost:5000/predict
```

A resposta será um JSON com a classe prevista e a confiança da predição:

```json
{
    "image_name": "imagem.jpg",
    "prediction": "aberta",
    "confidence": 0.95
}
```

### 3. **Teste de Carga com Locust**

Para realizar o teste de carga na API, execute o comando:

```bash
locust -f scripts/locustfile.py --host=http://localhost:5000
```

Depois, acesse a interface de controle do Locust em [http://localhost:8089](http://localhost:8089) para visualizar os resultados do teste.

### 4. **Treinamento do Modelo**

O treinamento do modelo pode ser feito através do notebook `notebooks/model_training.ipynb`. Siga os passos dentro do notebook para treinar o modelo YOLOv5 com o conjunto de dados do **Roboflow**.

---

## 📦 Deploy (Docker)

Para realizar o deploy da aplicação utilizando Docker, siga os passos abaixo:

1. **Construir a Imagem Docker**:

   Navegue até a pasta `api` e execute:

   ```bash
   docker build -t tequila-api .
   ```

2. **Rodar o Container Docker**:

   Após a construção da imagem, rode o container:

   ```bash
   docker run -p 5000:5000 tequila-api
   ```

   A API estará acessível em `http://localhost:5000`.


