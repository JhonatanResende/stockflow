from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from database import get_connection

router = APIRouter()

# Modelo do produto (equivalente ao req.body do Node.js)
class Produto(BaseModel):
    nome: str
    descricao: Optional[str] = ""
    quantidade: int
    preco: float

# ========================================
# ROTA 1: LISTAR TODOS OS PRODUTOS
# ========================================
@router.get("/produtos")
def listar_produtos():
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM produtos ORDER BY id DESC")
        rows = cur.fetchall()

        # Converte as linhas em lista de dicionários
        produtos = []
        for row in rows:
            produtos.append({
                "id":            row[0],
                "nome":          row[1],
                "descricao":     row[2],
                "quantidade":    row[3],
                "preco":         float(row[4]),
                "data_cadastro": str(row[5])
            })

        cur.close()
        conn.close()
        return produtos

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ========================================
# ROTA 2: BUSCAR PRODUTO POR ID
# ========================================
@router.get("/produtos/{id}")
def buscar_produto(id: int):
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM produtos WHERE id = %s", (id,))
        row = cur.fetchone()

        cur.close()
        conn.close()

        if not row:
            raise HTTPException(status_code=404, detail="Produto não encontrado")

        return {
            "id":            row[0],
            "nome":          row[1],
            "descricao":     row[2],
            "quantidade":    row[3],
            "preco":         float(row[4]),
            "data_cadastro": str(row[5])
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ========================================
# ROTA 3: CRIAR PRODUTO
# ========================================
@router.post("/produtos")
def criar_produto(produto: Produto):
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """INSERT INTO produtos (nome, descricao, quantidade, preco)
               VALUES (%s, %s, %s, %s) RETURNING id""",
            (produto.nome, produto.descricao, produto.quantidade, produto.preco)
        )

        id_criado = cur.fetchone()[0]
        conn.commit() # Salva no banco

        cur.close()
        conn.close()

        return {"mensagem": "Produto cadastrado com sucesso!", "id": id_criado}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ========================================
# ROTA 4: ATUALIZAR PRODUTO
# ========================================
@router.put("/produtos/{id}")
def atualizar_produto(id: int, produto: Produto):
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """UPDATE produtos
               SET nome = %s, descricao = %s, quantidade = %s, preco = %s
               WHERE id = %s""",
            (produto.nome, produto.descricao, produto.quantidade, produto.preco, id)
        )

        conn.commit()

        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Produto não encontrado")

        cur.close()
        conn.close()

        return {"mensagem": "Produto atualizado com sucesso!"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ========================================
# ROTA 5: DELETAR PRODUTO
# ========================================
@router.delete("/produtos/{id}")
def deletar_produto(id: int):
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("DELETE FROM produtos WHERE id = %s", (id,))
        conn.commit()

        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Produto não encontrado")

        cur.close()
        conn.close()

        return {"mensagem": "Produto deletado com sucesso!"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))