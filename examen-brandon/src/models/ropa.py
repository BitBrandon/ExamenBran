from sqlmodel import Field, SQLModel

class Ropa(SQLModel, table=True):
    id: str | None = Field(default=None, primary_key=True)
    tamaño: str = Field(index=True, max_length=5)
    tipo: str = Field(index=True, max_length=50)