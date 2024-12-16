

# Teste de Carga com Locust 🚀

Neste repositório, apresentamos uma solução para realizar testes de carga em APIs. Embora você possa utilizar a **interface da Azure** para gerenciar e executar testes de carga em sua infraestrutura na nuvem, este **script local** oferece uma forma prática e personalizável de realizar testes diretamente em sua máquina de desenvolvimento, sem necessidade de recursos adicionais na nuvem. 

A seguir, explicamos como configurar e rodar o **Locust** localmente para realizar testes de carga em sua API, simulando usuários virtuais que enviam requisições HTTP, como se fossem usuários reais interagindo com a aplicação.

## Por que usar o Locust localmente? 🤔

Utilizar este **script local** com o **Locust** permite que você:

- **Economize custos** com testes em nuvem (como Azure) quando não é necessário realizar uma carga massiva.
- **Desenvolva e teste rapidamente** a API ou a aplicação no seu ambiente local.
- **Tenha total controle** sobre o ambiente de testes e a configuração do número de usuários virtuais, o tempo de espera entre as requisições e outros parâmetros.

Se você deseja escalar para uma análise mais robusta e em larga escala, pode sempre usar a interface da Azure para gerenciar os testes, porém este script local oferece uma alternativa simples e eficaz para a maioria das necessidades de teste.

---

## Passo 1: Preparar o Ambiente ⚙️

### 1.1. Navegar até a Pasta de Scripts 🗂️

Antes de executar o Locust, você precisa estar dentro da pasta onde o arquivo `locustfile.py` está localizado. Abra o terminal e navegue até a pasta `scripts`:

```bash
cd /caminho/para/o/repositorio/scripts
```

### 1.2. Configurar o Arquivo `.env` 🔧

Você precisa criar um arquivo `.env` dentro da pasta `scripts` para configurar as variáveis de ambiente necessárias para o teste. Crie o arquivo `.env` com o seguinte conteúdo:

```
LOCUST_HOST=http://localhost:5000
LOCUST_USERNAME=admin
LOCUST_PASSWORD=password123
LOCUST_IMAGE=1715279936313.jpg
```

Essas variáveis são usadas pelo script `locustfile.py` para acessar a API, autenticar e enviar a imagem para o endpoint `/classify`.

- **LOCUST_HOST**: URL da sua API (exemplo: `http://localhost:5000`).
- **LOCUST_USERNAME**: Nome de usuário para autenticação básica (exemplo: `admin`).
- **LOCUST_PASSWORD**: Senha para autenticação básica (exemplo: `password123`).
- **LOCUST_IMAGE**: Caminho para a imagem que será enviada durante o teste (exemplo: `1715279936313.jpg`).

## Passo 2: Executar o Teste de Carga 🚦

### 2.1. Rodar o Locust 🖥️

Com a pasta correta e o arquivo `.env` configurado, execute o comando para iniciar o teste de carga:

```bash
locust -f locustfile.py 
```

### 2.2. Acessar a Interface de Controle do Locust 🌐

Após executar o comando acima, você pode acessar a interface de controle do Locust em seu navegador. Abra o navegador e acesse o seguinte endereço:

```
http://localhost:8089/
```

Nessa interface, você poderá configurar o número de usuários virtuais, o tempo de espera entre as requisições e visualizar os resultados do teste em tempo real.

## Passo 3: Resultados do Teste 📊

Durante a execução do teste, o Locust irá exibir informações sobre o número de requisições feitas, a taxa de falhas, o tempo de resposta, etc. Você poderá monitorar esses dados diretamente na interface web do Locust.

### Exemplo de Saída:

- **GET /health**: Exibe o status da API.
- **POST /classify**: Envia uma imagem para o endpoint de predição da API.

Os dados de resposta incluirão informações como o tempo médio de resposta, o tempo mínimo e máximo, entre outras métricas.

---

## Observações 🔍

- **Requisitos**: Certifique-se de ter o Locust instalado e as dependências necessárias configuradas corretamente. Se necessário, instale as dependências do projeto utilizando:

  ```bash
  pip install -r requirements.txt
  ```

- **Resultado do Teste**: Durante o teste, você poderá acompanhar o desempenho da API, o tempo de resposta das requisições e o número de falhas, tudo em tempo real na interface do Locust.

---

Com isso, você tem tudo o que precisa para executar o teste de carga na sua API utilizando o Locust localmente! 💻🔥

