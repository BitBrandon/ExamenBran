from sqlmodel import create_engine, SQLModel, Session
from src.models.ropa import Ropa

db_user: str = "brandon"  
db_password: str =  "1234"
db_server: str = "localhost" 
db_port: int = 3306  
db_name: str = "ropadb"  

DATABASE_URL = f"mysql+pymysql://{db_user}:{db_password}@{db_server}:{db_port}/{db_name}"
engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

def init_db():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        session.add(Ropa(id="1", tamaño="S", tipo="camiseta"))
        session.add(Ropa(id="2", tamaño="M", tipo="top"))
        session.add(Ropa(id="3", tamaño="L", tipo="pantalones"))
        session.commit()
        #session.refresh_all()