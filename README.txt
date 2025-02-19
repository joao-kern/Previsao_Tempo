Requisitos
Antes de rodar o projeto, você precisará configurar uma variável de ambiente que contém a chave de acesso ao MongoDB e uma que contenha a API Key da WeatherAPI. O projeto utiliza o MongoDB Atlas (banco de dados na nuvem) para armazenar informações e utiliza a WeatherAPI para obter os dados meteorológicos.

Passos para Configurar
1- Criar uma Conta no MongoDB Atlas

Se você ainda não tem uma conta no MongoDB Atlas, crie uma gratuitamente em https://www.mongodb.com/cloud/atlas.
Após criar sua conta, crie um cluster (banco de dados na nuvem) e um usuário para acessar o banco de dados.
Obter a Chave de Conexão

Dentro do painel do MongoDB Atlas, vá até o cluster que você criou e clique em Connect.
Selecione Connect your application e copie a string de conexão. A string estará no formato:
mongodb+srv://<username>:<password>@cluster0.mongodb.net/<dbname>?retryWrites=true&w=majority
Substitua <username>, <password>, e <dbname> com as credenciais do seu banco de dados.

2. Criar Conta e Obter a API Key da WeatherAPI

Para utilizar os serviços meteorológicos, é necessário criar uma conta na WeatherAPI e obter uma chave de API.

Acesse WeatherAPI.

Cadastre-se e acesse o painel da API.

Copie sua API Key, pois ela será usada no projeto.

3- Criar o Arquivo .env

Na raiz do projeto, crie um arquivo chamado .env e adicione a variável de ambiente MONGO_URI e API_KEY com o valor da string de conexão do MongoDB Atlas e da API Key, respectivamente. O arquivo .env deve ficar assim:
MONGO_URI="mongodb+srv://<username>:<password>@cluster0.mongodb.net/<dbname>?retryWrites=true&w=majority"
API_KEY="sua_chave_da_WeatherAPI"

Não adicione seu arquivo .env no GitHub. Ele deve ser mantido localmente para garantir que a chave de acesso não seja compartilhada. O arquivo .env está configurado para ser ignorado no .gitignore.