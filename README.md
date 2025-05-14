# 2025.1-EasyCrit-auth

## Auth
Esse modulo é responsável por autenticar o usuário e verificar se ele tem permissão para acessar as funcionalidades do sistema.

## Executar o projeto
### Requisitos
- Docker
- Docker Compose

## Inicializar o projeto
1. Clone o repositório:
```bash
git clone https://github.com/fga-eps-mds/2025.1-EasyCrit-auth.git
cd 2025.1-EasyCrit-auth
```
2. Crie um arquivo `.env` na raiz do projeto com as variáveis de ambiente necessárias.

3. É possível executar o projeto pelo Docker Compose presente no repositório de documentação do EasyCrit.
```bash
cd 2025.1-EasyCrit-docs
docker-compose up -d auth
```

## Variáveis de ambiente
| Variável de ambiente | Descrição |
|----------------------|-----------|
| `AUTH_PORT`          | Porta que o serviço irá rodar. |

## Documentação
É possível acessar a documentação do projeto através do Swagger, que está disponível na seguinte URL:
```
http://localhost:{AUTH_PORT}/docs
```
A documentação é gerada automaticamente a partir dos comentários do código, utilizando o Swagger UI. Para mais informações sobre como utilizar o Swagger, consulte a [documentação oficial](https://swagger.io/docs/).