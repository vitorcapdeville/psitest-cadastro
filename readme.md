# Serviço de cadastro

Este serviço é responsável por disponibilizar as informações pessoais de cada usuário. Disponibiliza rotas para cadastrar e recuperar as informações de um usuário, utilizando JWT para autenticação. Neste serviço não são armazenadas as senhas dos usuários. Quando um novo usuário é cadastrado, o cadastro chega neste serviço e mantém apenas as informações pessoais. As informações de login são enviadas para o serviço de autenticação.

> NOTA: É necessário que o serviço de autenticação esteja disponível para a utilização deste serviço.

## Instalação local

A utilização local do serviço requer que seja criada uma variável de ambiente PSITEST_AUTH com a URL do serviço de autenticação. Para isso, execute o seguinte comando no PowerShell:

```bash
$env:PSITEST_AUTH="http://localhost:8000"
```

> NOTA: Caso o serviço de autenticação esteja em outro endereço, substitua o endereço acima pelo endereço correto.

Para utilizar o serviço localmente, é recomendado a criação de um ambiente virtual.

```bash
python -m venv .venv
.venv/scripts/activate
```

Após a criação do ambiente virtual, instale as dependências do projeto.

```bash
pip install -r requirements.txt
```

### Execução

Para executar o servidor, utilize o comando:

```bash
fastapi run app --port 8001
```

O servidor estará disponível em `http://localhost:8001`.

## Utilizando via Docker

Para executar via Docker, é necessário ter o Docker instalado e em execução. Também é necessário que exista uma rede chamada `psitest`. A rede deve ser criada uma única vez com o seguinte comando:

```bash
docker network create psitest
```

Após a criação da rede, execute o seguinte comando para criar a imagem do serviço:

```bash
docker compose up
```

O serviço estará disponível em `http://localhost:8003`.

