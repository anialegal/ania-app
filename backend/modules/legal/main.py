# ── backend/modules/legal/main.py ──
from fastapi import FastAPI
from modules.core.config import settings
from modules.shared.billing.router import router as billing_router
from modules.shared.chat.router   import router as chat_router
from modules.legal.routers        import router as legal_router

app = FastAPI(title="ANIA Legal")

# Configuración global (Base de datos, CORS, JWT, etc.)
settings.configure_app(app)

# Routers compartidos
app.include_router(billing_router, prefix="/shared/billing")
app.include_router(chat_router,     prefix="/shared/chat")

# Routers específicos de Legal
app.include_router(legal_router, prefix="/legal")

@app.get("/health")
def health():
    return {"status": "ok"}

