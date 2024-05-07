from fastapi import FastAPI
from pydantic import BaseModel



class Item(BaseModel):
    nombre: str
    descripcion: str | None = None
    precio: float
    impuesto: float | None = None


app = FastAPI()

@app.get("/")
def saludo():
    return {'saludo' : 'Hola a Todos!!!!'}

@app.post("/items/")
async def crear_item(item: Item):
    item_dic = item.dict()
    if item.impuesto:
        precio_con_impuesto = item.precio + item.impuesto
        item_dic.update(
            {"precion_con_impuesto" : precio_con_impuesto}
        )
    return item