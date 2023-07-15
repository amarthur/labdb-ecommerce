# Laboratório de Bancos de Dados - Ecommerce

## Sobre o projeto

#### Back-end
Este projeto é um protótipo de uma plataforma ecommerce e utiliza banco de dados (Postgres, Neo4j e MongoDB) como forma de armazenar e recuperar eficientemente os dados do sistema. O repositório está divido entre backend e frontend.

No backend, estão localizadas os data mappers, responsáveis por fornecer uma camada de mapeamento entre os objetos de domínio e a fonte de dados. Além disso, há também os Data Access Objects, que encapsulam a lógica de acesso aos dados, com operações como *create*, *read*, *update*, *delete*, *get*, *get all*, entre outros. Por fim, a API em Flask para realizar a integração com o frontend.\

Junto das APIs há um arquivo example.py que possui algumas operações exemplo do sistema, rodá-lo também popula o sistema com alguns dados exemplo. Também na pasta modelos há imagens dos modelos que usamos no projeto.

#### Front-end
Nosso front-end foi construido em VueJS e utiliza axios para fazer requisicoes para a nossa API, a ideia é que o sistema fosse um painel de controle onde um administrador consiga fazer queries basicas para o BD como criar, deletar e atualizar dados. Durante o desenvolvimento focamos mais na criação do back-end e menos no front-end, o que somado a grandes dificuldades no desenvolvimento do front (começamos com Django mas não conseguimos fazer progresso), fez com que tivessemos que deixar varias funcionalidades mockadas. Os comandos de get, update e delete estão mockados, consultam um json estatico apesar de a API ser 100% funcional e conseguir receber esses comandos, no momento o único comando funcional é o de create que envia um comando de criação para a API com sucesso.


## Instruções para execução

### Configurações iniciais
1. Certifique-se que Postgresql, Neo4j e MongoDB estejam configurados em seu ambiente
2. Configure as URLs em */backend/api/urls.json* para serem compatíveis com seu ambiente

### Execução com frontend
1. Abra um terminal de comando
2. Execute `make setup` para instalar todas as dependências necessárias
3. Execute `make run_back` inicializar o backend
4. Em outro terminal, execute `make run_front` para inicializar o frontend
5. Por fim, abra a URL em *"App running at: ..."*

### Outros comandos
- Execute `make example` para criar alguns exemplos
- Execute `make drop_all` para remover todos os dados dos bancos
- Execute `make clean` para remover as dependências instaladas
