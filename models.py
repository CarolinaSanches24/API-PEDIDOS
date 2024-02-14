from pydantic import BaseModel
from typing import Union # tipagem 

class Usuario(BaseModel):
    name:str;
    email:str;
    senha:str;



