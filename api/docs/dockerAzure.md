# Guia para Deploy de Aplicação Flask com Docker e Azure e Plano de Escalabilidade da API

Este guia descreve como criar e implantar uma aplicação Flask utilizando Docker e Azure e detalha um plano de escabilidade da API

---

## Configurações Iniciais

### Configuração de Porta no Dockerfile
No Dockerfile, a porta exposta está definida como `5000`. Altere-a conforme a necessidade:

```dockerfile
EXPOSE 5000
```

---

## Criando o Contêiner Docker

### 1. Construir a Imagem Docker Localmente
Execute o seguinte comando no diretório do projeto (cd api) para criar a imagem:

```bash
docker build -t flask-yolo-api .
```

### 2. Testar o Contêiner Localmente
Para executar o contêiner localmente, use o comando abaixo. Adapte a porta conforme a necessidade da sua aplicação:

```bash
docker run -p 5000:5000 flask-yolo-api
```

---

## Fazer o Deploy no Azure

### 1. Login na Azure
Certifique-se de estar logado na Azure usando o seguinte comando:

```bash
az login
```

### 2. Criar um Registro de Contêiner no Azure
Crie um Azure Container Registry (ACR) com o comando abaixo:

```bash
az acr create --resource-group <Resource-Group-Name> --name <ACR-Name> --sku Basic
```

#### Exemplo:

```bash
az acr create --resource-group TequilaResourceGroup --name TequilaContainerRegistry --sku Basic
```

### 3. Fazer o Push da Imagem Docker para o Registro
Marque sua imagem Docker com o caminho do ACR e faça o push:

```bash
docker tag flask-yolo-api <ACR-Name>.azurecr.io/flask-yolo-api:v1
docker push <ACR-Name>.azurecr.io/flask-yolo-api:v1
```

#### Exemplo:

```bash
docker tag flask-yolo-api tequilaContainerRegistry.azurecr.io/flask-yolo-api:v1
docker push tequilaContainerRegistry.azurecr.io/flask-yolo-api:v1
```

---

## Criar um App na Azure

### 1. Login na Conta Azure
Certifique-se de estar autenticado na Azure, conforme descrito anteriormente.

### 2. Criar o Aplicativo Web
No portal Azure, pesquise por **Aplicativo Web para Contêineres** e siga as instruções para configurar o aplicativo com a imagem do registro criado.

---

## Observações Finais
- Certifique-se de que sua aplicação Flask está corretamente configurada para rodar na porta definida no Dockerfile.
- Verifique as permissões no ACR e no recurso do aplicativo para evitar problemas de autenticação.
- Utilize o Azure CLI para automatizar o processo sempre que possível.

---

## Automatização do Deploy
O script `.sh` é baseado no ano, mês, hora, minuto e segundo. Toda vez que fizer alguma alteração no código, execute o `.sh` novamente e atualize na Azure a tag que está sendo usada. Aguarde até 10 minutos para que a atualização seja refletida no ambiente. Caso algum problema, reinicie a aplicação web e espera mais alguns minutos.

---

## Plano de escalabilidade da API

Este plano detalha como escalar a API baseada nos requisitos de **High-Throughput Scenarios**, **Database Design**, **Monitoring and Metrics**, **Security**, e **Documentation**. O foco é no uso de ferramentas e serviços do **Azure** para garantir alta disponibilidade, desempenho e escalabilidade.

---

## **1. Cenário de Alto Tráfego (High-Throughput Scenarios)**

### **1.1 Simulação de Alto Tráfego**
Para avaliar o comportamento da API sob **1.000 requisições por segundo**, os seguintes passos serão aplicados:
1. Utilize o **Locust** (já configurado no projeto) para realizar testes.
   ```bash
   locust -f locustfile.py --host=http://<app-service-url>
   ```
2. **Configurações do Teste**:
   - Usuários simultâneos: **1.000**
   - Taxa de aumento: **100 usuários/segundo**
   - Endpoint: `/predict`  

3. **Resultado Esperado**:
   - Identificar **tempo de resposta**, **erro em requisições** e **limite da instância**.

---

### **1.2 Estratégias de Escalabilidade**

**Horizontais e Verticais**:
1. **Escalabilidade Horizontal**:
   - Utilize **Azure App Service** com **Auto Scaling** baseado em métricas:
     - **CPU Usage** > 70%
     - **Requisições por segundo**
   - O **Load Balancer** integrado no Azure App Service distribuirá a carga entre múltiplas instâncias.

2. **Escalabilidade Vertical**:
   - Caso o limite seja atingido, aumente os recursos das instâncias (RAM, CPU) no Azure App Service.

3. **Caching**:
   - Implementar cache local usando **Redis** no Azure Cache for Redis.
   - Armazene previsões de imagens já processadas para evitar processamento duplicado.

4. **Armazenamento Externo**:
   - Armazenar imagens recebidas no **Azure Blob Storage** e utilizar referências no processamento.

---

## **2. Design de Banco de Dados**

Para armazenar logs das requisições, metadados de imagens, resultados de classificação e timestamps, o seguinte design é proposto:

### **2.1 Estrutura do Banco de Dados**

Utilize **Azure Cosmos DB** (NoSQL) para escalabilidade e alta disponibilidade.

| **Campo**            | **Tipo**        | **Descrição**                           |
|-----------------------|-----------------|----------------------------------------|
| `request_id`         | String (UUID)   | ID único da requisição                 |
| `image_name`         | String          | Nome original da imagem                |
| `prediction`         | String          | Classe prevista (aberta/fechada)       |
| `confidence`         | Float           | Nível de confiança da predição         |
| `timestamp`          | Datetime        | Data e hora da requisição              |
| `processing_time`    | Float           | Tempo de processamento em milissegundos|
| `user_ip`            | String          | Endereço IP do usuário (para logs)     |

### **2.2 Justificativa**
- **Cosmos DB** oferece escalabilidade horizontal com baixa latência.
- **NoSQL** é adequado devido à natureza não-relacional dos logs.

---

## **3. Monitoramento e Métricas**

### **3.1 KPIs**
- **Tempo de Resposta**: Tempo médio e máximo de processamento das requisições.
- **Uptime**: Disponibilidade da API.
- **Taxa de Erro**: Percentual de requisições que falham.
- **Uso de Recursos**: CPU, memória e quantidade de instâncias ativas.

### **3.2 Ferramentas de Monitoramento**
- **Azure Monitor**: Para logs de aplicação, métricas de CPU e uso de memória.
- **Azure Application Insights**: Para rastrear o desempenho e o tempo de resposta.
- **Dashboard Grafana** (opcional): Integre o Azure Monitor para visualização avançada.

---

## **4. Segurança**

### **4.1 Autenticação e Autorização**
1. **Autenticação Básica**:
   - Já configurada na aplicação com variáveis de ambiente `API_USERNAME` e `API_PASSWORD`.

2. **API Key** (melhoria proposta):
   - Implementar autenticação baseada em **API Keys** para endpoints críticos.

### **4.2 Rate Limiting**
- Implementar **Flask-Limiter** para evitar abusos:
   ```python
   from flask_limiter import Limiter
   limiter = Limiter(app, key_func=get_remote_address)
   @app.route("/predict")
   @limiter.limit("100 per minute")
   def predict():
       ...
   ```

### **4.3 Input Validation**
- Validar imagens enviadas para evitar ataques:
   ```python
   if not allowed_file(file.filename):
       return jsonify({"error": "Invalid file type"}), 400
   ```

---

## **5. Documentação**

### **5.1 Estratégia de Escalabilidade**
1. **Load Balancing**:
   - O **Azure App Service** gerencia automaticamente o balanceamento de carga.
2. **Auto Scaling**:
   - Configurado no Azure com base em uso de CPU e número de requisições.
3. **Caching**:
   - **Azure Cache for Redis** armazena previsões recentes.
4. **Armazenamento**:
   - Imagens recebidas são armazenadas no **Azure Blob Storage**.
5. **Logs e Banco de Dados**:
   - Logs de requisições são armazenados no **Azure Cosmos DB** para escalabilidade e análise.

---

## **6. Resumo do Fluxo**

1. **Requisição Enviada** → Azure Load Balancer distribui a carga entre instâncias.
2. **Armazenamento** → Imagem enviada ao Azure Blob Storage.
3. **Processamento** → API processa a imagem com YOLOv8.
4. **Cache** → Resultados armazenados no Azure Redis Cache.
5. **Banco de Dados** → Logs e resultados armazenados no Azure Cosmos DB.
6. **Monitoramento** → Métricas capturadas pelo Azure Monitor e Application Insights.

---

### **7. Diagrama de Arquitetura**

```plaintext
                  +---------------------------+
                  |       Usuários            |
                  +-------------+-------------+
                                |
                                v
                  +---------------------------+
                  | Azure Load Balancer       |
                  +-------------+-------------+
                                |
              +-----------------+-----------------+
              |                                   |
+-------------v-------------+       +-------------v-------------+
|   API Instance (1)        |       |   API Instance (2)        |
|   Azure App Service       |       |   Azure App Service       |
+-------------+-------------+       +-------------+-------------+
              |                                   |
              +-----------------+-----------------+
                                |
                +---------------v---------------+
                |     Azure Redis Cache         |
                +---------------+---------------+
                                |
                +---------------v---------------+
                |     Azure Blob Storage        |
                +---------------+---------------+
                                |
                +---------------v---------------+
                |       Azure Cosmos DB         |
                +-------------------------------+
                                |
                +---------------v---------------+
                |       Azure Monitor           |
                +-------------------------------+
```

---

## ✅ **Conclusão**

O plano proposto utiliza serviços gerenciados do **Azure** para escalabilidade, monitoramento e segurança da API YOLOv8. Ele oferece alta disponibilidade e desempenho, com recursos como balanceamento de carga, auto scaling, cache de resultados e armazenamento eficiente. 🚀


