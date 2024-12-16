

# 🚀 API de Previsão com YOLOv5 🤖

Este projeto implementa uma API baseada no **Flask** que permite fazer previsões sobre imagens enviadas via requisição HTTP. O modelo de **classificação de imagens YOLOv5** foi treinado para detectar se uma imagem contém uma classe "aberta" ou "fechada". A API também suporta autenticação básica para garantir a segurança ao utilizar os endpoints.

## 📦 Estrutura do Projeto

A estrutura do projeto é a seguinte:

```
api/
├── app.py                  # Código principal da API Flask
├── best.pt                 # Modelo treinado YOLOv5
├── deploy.sh               # Script para deploy no servidor
├── Dockerfile              # Arquivo de configuração para criar a imagem Docker
├── docs                    # Documentação adicional sobre Docker e Azure
│   └── dockerAzure.md
├── readme.md               # Este arquivo
├── requirements.txt        # Dependências do projeto
├── static                  # Arquivos estáticos (JS, CSS)
│   ├── script.js
│   └── styles.css
└── templates               # Arquivos HTML (Front-end)
    └── index.html
```

## 🧰 Dependências

Este projeto depende das seguintes bibliotecas para funcionar corretamente:

- **Flask**: Framework para construção da API.
- **Flask-CORS**: Para habilitar o CORS, permitindo que o front-end se comunique com a API sem restrições de origem.
- **Ultralytics YOLOv5**: Utilizado para carregar e rodar o modelo treinado de detecção de objetos.
- **Pillow**: Para processamento de imagens.
- **Docker** (opcional): Para deploy no container.

### 📦 Instalação das Dependências

Primeiro, instale as dependências necessárias:

```bash
pip install -r requirements.txt
```

### 🐳 Docker (opcional)

Se preferir rodar a aplicação no Docker, utilize o `Dockerfile` e o script `deploy.sh` para configurar o ambiente. Para construir a imagem Docker e rodar o container, execute:

```bash
docker build -t tequila-api .
docker run -p 5000:5000 tequila-api
```

## 🔑 Autenticação

A API requer autenticação básica para proteger os endpoints. Por padrão, o nome de usuário é `admin` e a senha é `password123`. No entanto, esses valores podem ser sobrescritos por variáveis de ambiente para fins de segurança e personalização.

### Exemplo de variáveis de ambiente:
```env
API_USERNAME=admin
API_PASSWORD=password123
```

Se as variáveis de ambiente não forem configuradas, os valores padrão serão usados: admin e password123, para ser mais objetivo.

## 📡 Endpoints da API

### 1. **POST /classify** - Predição de Imagem

Este endpoint permite enviar uma imagem para fazer uma previsão de classe ("aberta" ou "fechada").

**Requisição:**
- Método: `POST`
- Formato de Dados: Multipart (Imagem no corpo da requisição)
- Autenticação: Basic Auth

**Exemplo de requisição cURL:**
```bash
curl -u admin:password123 -F "image=@/path/to/image.jpg" http://localhost:5000/classify
```

**Resposta:**
A resposta será um JSON com os seguintes dados:
```json
{
    "image_name": "image.jpg",
    "classifyion": "aberta",
    "confidence": 0.95
}
```

- **image_name**: Nome original da imagem enviada.
- **classifyion**: Classe prevista (aberta ou fechada).
- **confidence**: Confiança da previsão.

### 2. **GET /health** - Verificação de Saúde

Este endpoint permite verificar se a API está funcionando corretamente.

**Requisição:**
- Método: `GET`

**Resposta:**
```json
{
    "status": "ok"
}
```

### 3. **GET /** - Página Inicial

Este endpoint exibe uma página HTML simples onde é possível fazer o upload de uma imagem para previsão.

---

Claro! Aqui está a adição de um exemplo de requisição de predição via `curl` no **README**:

---

## 📡 Exemplo de Requisição via cURL

### 1. **Predição de Imagem** (`POST /classify`)

Para fazer uma requisição de predição de imagem, você pode usar o comando `curl` conforme o exemplo abaixo.

**Exemplo de requisição cURL:**
```bash
curl -u admin:password123 -F "image=@/caminho/para/imagem.jpg" http://localhost:5000/classify
```

**Explicação:**
- `-u admin:password123`: Passa as credenciais de autenticação básica (substitua `admin` e `password123` conforme necessário).
- `-F "image=@/caminho/para/imagem.jpg"`: Envia a imagem para o endpoint `/classify`. Substitua `/caminho/para/imagem.jpg` pelo caminho da sua imagem local.
- `http://localhost:5000/classify`: URL do endpoint de predição da API.

**Resposta esperada (em JSON):**
```json
{
    "image_name": "imagem.jpg",
    "classifyion": "aberta",
    "confidence": 0.95
}
```

- **image_name**: Nome da imagem que foi enviada.
- **classifyion**: Classe prevista (exemplo: "aberta" ou "fechada").
- **confidence**: Confiança da predição (valor entre 0 e 1).

Este comando vai retornar uma resposta em formato JSON, com a previsão da classe e o nível de confiança para a imagem enviada.


## 💻 Execução Local

Para rodar o projeto localmente, siga os passos abaixo:

1. **Configuração das variáveis de ambiente**:
   - Crie um arquivo `.env` na raiz do projeto com as variáveis necessárias (username, password, etc).

2. **Rodar o servidor Flask**:
   Execute o seguinte comando para rodar o servidor:

   ```bash
   python app.py
   ```

3. Acesse a API no endereço: [http://localhost:5000](http://localhost:5000).

4. Acesse a página de upload em: [http://localhost:5000](http://localhost:5000).

5. Para verificar se tudo está funcionando, execute a requisição de saúde:

   ```bash
   curl http://localhost:5000/health
   ```

## 🚀 Deploy no Azure (opcional)

Se você quiser fazer o deploy da aplicação no **Azure**, você pode usar o arquivo `dockerAzure.md` localizado em `docs` para detalhes sobre o processo de deploy com Docker no Azure.

---

## ⚙️ Como Funciona

### 🔨 Flask API

O **Flask** é usado para criar a API e os endpoints de previsão e saúde. Quando uma imagem é enviada para o endpoint `/classify`, ela é processada e passada para o modelo YOLOv5 para inferência.

1. A imagem é recebida no endpoint `/classify`.
2. A imagem é processada e salva como um arquivo temporário.
3. O modelo YOLOv5 faz a previsão (aberta ou fechada) na imagem recebida.
4. A resposta com o nome da classe prevista e a confiança é retornada.

### 🤖 Modelo YOLOv5

O modelo **YOLOv5** foi treinado e salvo no arquivo `best.pt`. Ele é carregado assim que a aplicação é iniciada. O modelo faz a detecção e classificação da imagem enviada.



## 📡 Documentação da API com Swagger

A API de Previsão com YOLOv5 oferece uma documentação interativa via **Swagger UI**, que permite explorar os endpoints e realizar requisições diretamente pela interface gráfica.

### 📝 Acessando a Documentação Swagger

Após iniciar o servidor Flask, você pode acessar a documentação da API através do Swagger UI no seguinte URL:

```
http://localhost:5000/apidocs
```

Isso abrirá a interface do Swagger, onde você verá todos os endpoints disponíveis na API, como:

- **POST /classify**: Enviar uma imagem para fazer a previsão.
- **GET /health**: Verificar se a API está funcionando corretamente.
- **GET /**: Acesso à página inicial para fazer o upload da imagem.

Na interface do Swagger, você poderá visualizar a descrição de cada endpoint, os parâmetros necessários (como a imagem no endpoint `/classify`), e realizar as requisições diretamente pela interface, sem necessidade de usar ferramentas como `curl`.

### 🎯 Como Usar o Swagger UI

1. **Abrir o navegador** e acessar [http://localhost:5000/apidocs](http://localhost:5000/apidocs).
2. **Escolher o endpoint desejado**: No Swagger UI, você verá todos os endpoints listados, como `POST /classify` ou `GET /health`.
3. **Enviar uma requisição**: Para o endpoint `POST /classify`, por exemplo, você poderá fazer o upload de uma imagem diretamente pela interface e ver a previsão retornada em formato JSON.
4. **Explorar mais funcionalidades**: O Swagger UI também oferece uma maneira de testar outros endpoints, ver as respostas de cada um e entender como a API funciona de maneira interativa.


