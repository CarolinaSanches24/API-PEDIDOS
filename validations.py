import uuid
from fastapi import HTTPException

def verificar_lista_vazia(lista, mensagem):
    if len(lista) == 0:
        raise HTTPException(status_code=404, detail=mensagem)
    else:
        return lista
    
def validar_pedido(pedido, db_produtos, db_clients):
    if pedido.id_cliente<1 or pedido.id_produto<1 or pedido.quantidade<1:
        return False , "O campo deve receber valores positivos e diferentes de 0"
   
    if not pedido.id_cliente or not pedido.id_produto or not pedido.quantidade:
        return False, "O preenchimento dos campos é obrigátorio"
    
    # verificar se o produto existe
    produto_encontrado = None
    
    for produto in db_produtos:
        if produto["id"] == pedido.id_produto:
            produto_encontrado= produto
            break
    
    if not produto_encontrado:
        return False, "Produto não encontrado"
    
    #verificar se o cliente existe 
    cliente_encontrado = False
    
    for cliente in db_clients:
        if cliente["id"]==pedido.id_cliente:
            cliente_encontrado=True
            break
    if not cliente_encontrado:
       return False, "Cliente não encontrado"
   

    return True, ""
    
def validar_dados_usuario(usuario):
    # Se o ID estiver vazio, preenche com id randomico
    if not usuario.id:
        usuario.id = str(uuid.uuid4())
    #Verifica se os campos estão vazios
    if not usuario.name or not usuario.email or not usuario.senha:
        return False, "O preenchimento dos campos é obrigátorio"
    
    return True, ""