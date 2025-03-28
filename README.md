# Previsão do Tempo

Aplicativo simples de previsão do tempo desenvolvido em Python, utilizando a API WeatherAPI para obter informações meteorológicas em tempo real e o MongoDB Atlas para armazenar dados.

## Tecnologias Utilizadas

- **Python**: Linguagem principal do projeto
- **Tkinter**: Interface gráfica
- **Requests**: Para fazer requisições HTTP à API
- **WeatherAPI**: Fonte dos dados meteorológicos
- **MongoDB Atlas**: Banco de dados na nuvem para armazenar informações


## Funcionalidades

- Permite inserir o nome de uma cidade e obter dados climáticos atuais.
- Exibe temperatura, umidade, condição do tempo e velocidade do vento.
- Interface simples e intuitiva usando Tkinter.
- Armazena informações meteorológicas no MongoDB Atlas.


## Como Executar o Projeto

### 1. Clonar o repositório

```bash
git clone https://github.com/joao-kern/Previsao_Tempo.git
cd Previsao_Tempo
```

### 2. Instalar Dependências

Certifique-se de que possui o Python instalado. Em seguida, instale os pacotes necessários:

```bash
pip install requests pymongo python-dotenv
```

### 3. Configurar Variáveis de Ambiente

O projeto requer uma chave de acesso ao **MongoDB Atlas** e uma API Key da **WeatherAPI**.

#### 3.1 Criar uma Conta no MongoDB Atlas

Se ainda não tem uma conta no MongoDB Atlas, crie uma gratuitamente em [MongoDB Atlas](https://www.mongodb.com/cloud/atlas).

1. Crie um cluster e um usuário para acessar o banco de dados.
2. No painel do MongoDB Atlas, acesse o cluster criado e clique em **Connect**.
3. Selecione **Connect your application** e copie a string de conexão.
   - O formato da string será:
     ```
     mongodb+srv://<username>:<password>@cluster0.mongodb.net/<dbname>?retryWrites=true&w=majority
     ```
   - Substitua `<username>`, `<password>` e `<dbname>` pelas credenciais do seu banco.

#### 3.2 Criar Conta e Obter a API Key da WeatherAPI

1. Acesse [WeatherAPI](https://www.weatherapi.com/).
2. Cadastre-se e acesse o painel da API.
3. Copie sua **API Key** para usar no projeto.

#### 3.3 Criar o Arquivo `.env`

Na raiz do projeto, crie um arquivo chamado `.env` e adicione as seguintes variáveis:

```env
MONGO_URI="mongodb+srv://<username>:<password>@cluster0.mongodb.net/<dbname>?retryWrites=true&w=majority"
API_KEY="sua_chave_da_WeatherAPI"
```

> **Importante:** O arquivo `.env` não deve ser compartilhado no GitHub. Ele está configurado para ser ignorado no `.gitignore`.

### 4. Executar o Programa

```bash
python main.py
```
