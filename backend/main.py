from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import router

# Cria a aplicação FastAPI
app = FastAPI()

# Configura o CORS (permite o frontend falar com o backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registra as rotas
app.include_router(router, prefix="/api")

# Rota de teste
@app.get("/")
def root():
    return {"mensagem": "🚀 Servidor funcionando!"}