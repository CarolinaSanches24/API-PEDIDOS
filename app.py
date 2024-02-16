from fastapi import FastAPI, HTTPException, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from typing import List
import uuid
from models import Cliente, Usuario, Pedido, Produto

app = FastAPI()

db_users: List[Usuario]=[]
db_clients :List[Cliente]=[]
db_pedidos :List[Pedido]=[]
db_produtos :List[Produto]=[]

@app.get("/")
async def inicio():
    return {"message":"Bem-vindo a Api Pedidos!"}

@app.get("/usuarios")
async def listar_usuarios():
    if len(db_users)==0:
        raise HTTPException(status_code=404, detail="Não foi encontrado nenhum usuário")
    return db_users

@app.get("/clientes")
async def listar_clientes():
    if len(db_clients)==0:
        raise HTTPException(status_code=404, detail="Não foi encontrado nenhum cliente")
    return db_clients 

@app.get("/produtos")
async def listar_produtos():
    if len(db_produtos)==0:
        raise HTTPException(status_code=404, detail="Não foi encontrado nenhum produto")
    return db_produtos

@app.get("/pedidos")
async def listar_pedidos():
    if len(db_pedidos)==0:
        raise HTTPException(status_code=404, detail="Não foi encontrado nenhum pedido")
    return db_pedidos

@app.post("/Usuario", status_code=status.HTTP_201_CREATED)
async def cadastrar_usuario(usuario: Usuario):
    
    # Se o ID estiver vazio, preenche com id randomico
    if not usuario.id:
        usuario.id = str(uuid.uuid4())
        
    #Verifica se os campos estão vazios
    if not usuario.name or not usuario.email or not usuario.senha:
        raise HTTPException(status_code=400, detail = "O preenchimento dos campos é obrigátorio")
    db_users.append(usuario);
    
    return {"message": "Usuário cadastrado com sucesso!"}

@app.post("/Cliente", status_code=status.HTTP_201_CREATED)
async def cadastrar_cliente(cliente: Cliente):
    
    #Verifica se os campos estão vazios
    if not cliente.name or not cliente.telephone or not cliente.address:
        raise HTTPException(status_code=400, detail="O preenchimento dos campos é obrigátorio")
    
    cliente_format = {
        "id":len(db_clients)+1,
        "nome":cliente.name,
        "telefone":cliente.telephone,
        "endereço":cliente.address
    }
    db_clients.append(cliente_format);
    
    return {"message": "Cliente cadastrado com sucesso!"}

@app.post("/Produto", status_code=status.HTTP_201_CREATED)
async def cadastrar_produto(produto:Produto):
   
    if not produto.descricao or not produto.quantidade_estoque or not produto.preco_unitario:
        raise HTTPException(status_code=400, detail = "O preenchimento dos campos é obrigátorio")
    
    produto_format = {
        "id":len(db_produtos)+1,
        "descricao":produto.descricao,
        "quantidade_estoque":produto.quantidade_estoque,
        "preco_unitario":produto.preco_unitario
    }
    
    db_produtos.append(produto_format);
    
    return {"message":"Produto cadastrado com sucesso!"}

@app.post("/Pedido", status_code=status.HTTP_201_CREATED)
async def cadastrar_pedido(pedido: Pedido):
    if pedido.id_cliente<1 or pedido.id_produto<1 or pedido.quantidade<1:
        raise HTTPException(status_code=400, detail= "O campo deve receber valores positivos e diferentes de 0")
   
    if not pedido.id_cliente or not pedido.id_produto or not pedido.quantidade:
        raise HTTPException(status_code=400, detail="O preenchimento dos campos é obrigátorio")
    
    # verificar se o produto existe
    produto_encontrado = None
    
    for produto in db_produtos:
        if produto["id"] == pedido.id_produto:
            produto_encontrado= produto
            break
    
    if not produto_encontrado:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    #verificar se o cliente existe 
    cliente_encontrado = False
    
    for cliente in db_clients:
        if cliente["id"]==pedido.id_cliente:
            cliente_encontrado=True
            break
    if not cliente_encontrado:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    # calculo valor total
    valor_total = produto_encontrado['preco_unitario']*pedido.quantidade
    
    pedido = {
        "id":len(db_pedidos)+1,
        "id_cliente":pedido.id_cliente,
        "id_produto":pedido.id_produto,
        "valor_total":valor_total
    }
    
    db_pedidos.append(pedido)
    
    return {"message":"Pedido Criado com Sucesso"}

# Torna todos os campos do corpo requisicao obrigatorios
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={"detail": "Todos os campos são obrigatórios"}
    )