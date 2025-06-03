from fastapi import FastAPI
from modules.core.config import settings
from modules.shared.billing.router import router as billing_router
from modules.shared.chat.router import router as chat_router
from modules.legal.routers import router as legal_router
from modules.empresa.routers import router as empresa_router

app = FastAPI(title="ANIA API")

# Config global (DB, CORS, JWT…)
settings.configure_app(app)

# Routers compartidos
app.include_router(billing_router, prefix="/shared/billing")
app.include_router(chat_router,     prefix="/shared/chat")

# Rutas de cada vertical
app.include_router(legal_router,   prefix="/legal")
app.include_router(empresa_router, prefix="/empresa")
