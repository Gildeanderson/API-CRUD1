# API CRUD Simples com FastAPI e Supabase

Esta é uma API simples criada com **FastAPI** que se conecta ao seu banco de dados **PostgreSQL** no **Supabase** utilizando o SQLAlchemy.

## Como usar

### 1. Pré-requisitos
Certifique-se de ter o Python instalado na sua máquina (versão 3.8+ recomendada).

### 2. Edite o código para colocar a sua senha
Abra o arquivo `main.py` e procure a linha onde a URL do banco de dados está definida. Substitua `[YOUR-PASSWORD]` pela sua senha real do Supabase.

```python
# No arquivo main.py:
SQLALCHEMY_DATABASE_URL = "SUA SENHA"
```

### 3. Instale as dependências
Abra o terminal na pasta onde os arquivos estão e rode o seguinte comando:
```bash
pip install -r requirements.txt
```

### 4. Rode a API
Para iniciar o servidor da API (com recarregamento automático a cada vez que você altera o código), use o Uvicorn:
```bash
uvicorn main:app --reload
```

### 5. Acesse a Documentação Interativa
O Swagger UI, que permite testar toda a sua API diretamente do navegador, está disponível em:
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

Lá você vai poder criar (POST), listar (GET), atualizar (PUT) e deletar (DELETE) os *Items*, e tudo será refletido diretamente no seu banco de dados Supabase! Se não houver a tabela, foi configurado para que a API crie assim que rodar.
