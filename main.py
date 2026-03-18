from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
import psycopg2
import os
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env sempre atualizadas
load_dotenv(override=True)

app = FastAPI()

# Pega a URL de conexão do arquivo .env de forma segura
DB_URL = os.getenv("DATABASE_URL")

@app.get("/")
def test_db():
    try:
        conn = psycopg2.connect(DB_URL)
        conn.close()
        return {"mensagem": "Conectou ao Supabase com sucesso usando variáveis de ambiente!"}
    except Exception as erro:
        return {"erro": str(erro)}

# Rota para renderizar a TELA HTML
@app.get("/tela/")
def render_tela():
    return FileResponse("index.html")

# Classe para validar os dados que chegam
class Usuario(BaseModel):
    nome: str
    email: str

@app.post("/usuarios/")
def criar_usuario(usuario: Usuario):
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        
        # Garante que a tabela existe (para você não ter erro se o banco estiver vazio!)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id SERIAL PRIMARY KEY,
                nome VARCHAR(100),
                email VARCHAR(100) UNIQUE
            );
        """)
        
        # Insere a pessoa na tabela
        cur.execute(
            "INSERT INTO usuarios (nome, email) VALUES (%s, %s) RETURNING id;",
            (usuario.nome, usuario.email)
        )
        novo_id = cur.fetchone()[0]
        
        conn.commit()
        cur.close()
        conn.close()
        
        return {"mensagem": "Usuário salvo no banco com sucesso!", "id": novo_id, "dados": usuario}
    except Exception as erro:
        return {"erro": str(erro)}

@app.get("/usuarios/")
def listar_usuarios():
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        
        # Pega todos os usuários da tabela ordenados pelo ID
        cur.execute("SELECT id, nome, email FROM usuarios ORDER BY id;")
        registros = cur.fetchall()
        
        # Transforma os dados numa lista bonitinha (Dicionários JSON)
        lista_de_usuarios = []
        for linha in registros:
            lista_de_usuarios.append({
                "id": linha[0],
                "nome": linha[1],
                "email": linha[2]
            })
            
        cur.close()
        conn.close()
        
        return {"total": len(lista_de_usuarios), "usuarios": lista_de_usuarios}
    except Exception as erro:
        return {"erro": str(erro)}

@app.put("/usuarios/{usuario_id}")
def atualizar_usuario(usuario_id: int, usuario: Usuario):
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        
        # Verifica se o usuário existe antes de atualizar
        cur.execute("SELECT id FROM usuarios WHERE id = %s;", (usuario_id,))
        if not cur.fetchone():
            return {"erro": "Usuário não encontrado"}
            
        # Atualiza os dados
        cur.execute(
            "UPDATE usuarios SET nome = %s, email = %s WHERE id = %s;",
            (usuario.nome, usuario.email, usuario_id)
        )
        
        conn.commit()
        cur.close()
        conn.close()
        
        return {"mensagem": f"Usuário {usuario_id} atualizado com sucesso!"}
    except Exception as erro:
        return {"erro": str(erro)}


@app.delete("/usuarios/{usuario_id}")
def deletar_usuario(usuario_id: int):
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        
        # Verifica se o usuário existe antes de deletar
        cur.execute("SELECT id FROM usuarios WHERE id = %s;", (usuario_id,))
        if not cur.fetchone():
            return {"erro": "Usuário não encontrado"}
            
        # Deleta permanentemente
        cur.execute("DELETE FROM usuarios WHERE id = %s;", (usuario_id,))
        
        conn.commit()
        cur.close()
        conn.close()
        
        return {"mensagem": f"Usuário {usuario_id} deletado com sucesso!"}
    except Exception as erro:
        return {"erro": str(erro)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
