# Laboratório de Bancos de Dados - Ecommerce

## Projeto
Este projeto é um protótipo de uma plataforma ecommerce e utiliza banco de dados (Postgres, Neo4j e MongoDB) como forma de armazenar e recuperar eficientemente os dados do sistema. O repositório está divido entre backend e frontend.

No backend, estão localizadas os data mappers, responsáveis por fornecer uma camada de mapeamento entre os objetos de domínio e a fonte de dados. Além disso, há também os Data Access Objects, que encapsulam a lógica de acesso aos dados, com operações como *create*, *read*, *update*, *delete*, *get*, *get all*, entre outros. Por fim, a API em Flask para realizar a integração com o frontend.


## Backend
Para executar os comandos do backend:

1. Abra um terminal de comando e navegue até o /backend/

2. Execute `make setup` para criar ambiente virtual do python e instalar as dependências necessárias

3.
  - Execute `make run` para rodar a api do Flask
  - Execute `make example` para criar alguns exemplos
