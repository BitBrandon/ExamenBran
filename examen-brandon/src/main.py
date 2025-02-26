from typing import Annotated
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select, func

from src.models.ropa import Ropa
from src.data.db import init_db, get_session


@asynccontextmanager
async def lifespan(application: FastAPI):
    init_db()
    yield


SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI(lifespan=lifespan)


@app.get("/ropa", response_model=list[Ropa])
def lista_ropa(session: SessionDep):
    ropa = session.exec(select(Ropa)).all()
    return ropa


@app.get("/ropa/{tipo}", response_model=Ropa)
def buscar_coche(tipo: str, session: SessionDep):
    tipo_encontrado = session.get(Ropa, tipo)
    if not tipo_encontrado:
        raise HTTPException(status_code=404, detail="Tipo no encontrado")
    return tipo_encontrado

@app.post("/ropa", response_model=Ropa)
def nuevo_coche(ropa: Ropa, session: SessionDep):
    ropa_encontrado = session.get(Ropa, ropa.id)
    if ropa_encontrado:
        raise HTTPException(status_code=400, detail="Ropa ya existe")
    session.add(ropa)
    session.commit()
    session.refresh(ropa)
    return ropa

@app.delete("/ropa/{id}")
def borrar_ropa(id: str, session: SessionDep):
    ropa_encontrada = session.get(Ropa, id)
    if not ropa_encontrada:
        raise HTTPException(status_code=404, detail="Ropa no encontrado")
    session.delete(ropa_encontrada)
    session.commit()
    return {"mensaje": "Ropa eliminado"}


@app.put("/ropa", response_model=Ropa)
def reemplaza_ropa(ropa: Ropa, session: SessionDep):
    ropa_encontrado = session.get(Ropa, ropa.id)
    if not ropa_encontrado:
        raise HTTPException(status_code=404, detail="Ropa no encontrado")
    ropa_data = ropa.model_dump()
    ropa_encontrado.sqlmodel_update(ropa_data)
    session.add(ropa_encontrado)
    session.commit()
    session.refresh(ropa_encontrado)
    return ropa_encontrado
