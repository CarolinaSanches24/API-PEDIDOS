from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from models import Usuario

app = FastAPI()

@app.post("/cadastrarUsuario")
async def cadastrar_usuario(usuario: Usuario):
    #Verifica se os campos estão vazios
    if not usuario.name or not usuario.email or not usuario.senha:
        raise HTTPException(status_code=400, detail="O preenchimento dos campos é obrigátorio")
    
    return {"message": "Usuário cadastrado com sucesso!"}

# Torna todos os campos do corpo requisicao obrigatorios
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={"detail": "Todos os campos são obrigatórios"}
    )