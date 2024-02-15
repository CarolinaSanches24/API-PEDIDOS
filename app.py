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

@app.get("/")
async def inicio():
    return {"message":"Bem-vindo a Api Pedidos!"}

@app.get("/usuarios")
async def listar_usuarios():
    return db_users

@app.get("/clientes")
async def listar_clientes():
    return db_clients 

@app.post("/cadastrarUsuario", status_code=status.HTTP_201_CREATED)
async def cadastrar_usuario(usuario: Usuario):
    
    # Se o ID estiver vazio, preenche com id randomico
    if not usuario.id:
        usuario.id = str(uuid.uuid4())
        
    #Verifica se os campos estão vazios
    if not usuario.name or not usuario.email or not usuario.senha:
        raise HTTPException(status_code=400, detail="O preenchimento dos campos é obrigátorio")
    db_users.append(usuario);
    
    return {"message": "Usuário cadastrado com sucesso!"}

@app.post("/cadastrarCliente", status_code=status.HTTP_201_CREATED)
async def cadastrar_cliente(cliente: Cliente):
    
    # Se o ID estiver vazio, preenche com id randomico
    if not cliente.id:
        cliente.id = str(uuid.uuid4())
        
    #Verifica se os campos estão vazios
    if not cliente.name or not cliente.telephone or not cliente.address:
        raise HTTPException(status_code=400, detail="O preenchimento dos campos é obrigátorio")
    db_clients.append(cliente);
    
    return {"message": "Cliente cadastrado com sucesso!"}

@app.post("/Pedido", status_code=status.HTTP_201_CREATED)
async def cadastrar_pedido(pedido: Pedido):
   
    if pedido.id is None:
        pedido.id = len(db_pedidos) + 1  
        
    if not pedido.id_cliente or not pedido.id_produto or not pedido.quantidade or not pedido.valor_total:
        raise HTTPException(status_code=400, detail="O preenchimento dos campos é obrigátorio")
    db_clients.append(pedido);
    
    return {"message": "Pedido cadastrado com sucesso!"}

# Torna todos os campos do corpo requisicao obrigatorios
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={"detail": "Todos os campos são obrigatórios"}
    )