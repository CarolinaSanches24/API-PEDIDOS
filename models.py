from pydantic import BaseModel, Field
from typing import List # tipagem 
import uuid

class Usuario(BaseModel):
    #gerar um valor padrão para o campo. 
    #lambda gera um UUID aleatorio
    id: str = Field(default_factory=lambda: str(uuid.uuid4())),
    name:str;
    email:str;
    senha:str;

class Cliente(BaseModel):
    name:str;
    telephone:str;
    address:str;
    
class Produto(BaseModel):
    descricao:str;
    quantidade_estoque:int;
    preco_unitario:float;
class Pedido(BaseModel):
    id_produto:int;
    id_cliente:int;
    quantidade :int;
