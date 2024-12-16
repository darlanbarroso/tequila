# Guia para Deploy de Aplicação Flask com Docker e Azure

Este guia descreve como criar e implantar uma aplicação Flask utilizando Docker e Azure.

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

