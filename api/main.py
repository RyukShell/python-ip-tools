import ipaddress
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator

# Asegurar que Python encuentre los módulos de la raíz
sys.path.insert(0, str(Path(__file__).parent.parent))

from ip_validator import es_ip_valida
from logger_config import configurar_logger
from subnet_analyzer import analizar_subred

# Cargar variables de entorno desde .env
load_dotenv()

# Configuración desde entorno
API_HOST = os.getenv("API_HOST", "127.0.0.1")
API_PORT = int(os.getenv("API_PORT", 8000))

logger = configurar_logger("api_gateway")

app = FastAPI(
    title="IP Tools API",
    description="API segura para validación y análisis de redes",
    version="1.0.0",
    docs_url="/docs",  # Swagger UI
)


# ── Modelos Pydantic (Validación estricta de inputs) ───
class IPRequest(BaseModel):
    ip: str = Field(..., min_length=7, max_length=45)

    @field_validator("ip")
    @classmethod
    def limpiar_y_validar(cls, v):
        v = v.strip()
        if not es_ip_valida(v):
            raise ValueError("Formato de IP inválido")
        return v


class CIDRRequest(BaseModel):
    cidr: str = Field(..., min_length=9, max_length=49)

    @field_validator("cidr")
    @classmethod
    def validar_cidr(cls, v):
        v = v.strip()
        try:
            ipaddress.ip_network(v, strict=False)
        except ValueError as e:
            raise ValueError(f"CIDR inválido: {e}") from None


class IPResponse(BaseModel):
    ip: str
    valido: bool
    version: int | None = None
    es_privada: bool | None = None


class SubnetResponse(BaseModel):
    network_address: str
    broadcast_address: str
    netmask: str
    usable_hosts_count: int


# ─── Endpoints ───
@app.get("/")
def root():
    return {"app": "IP Tools API", "status": "operational"}


@app.post("/validate", response_model=IPResponse)
def validar_ip(body: IPRequest):
    """Valida una IP y retorna metadatos de seguridad."""
    logger.info(f"[VALIDATE] IP recibida: {body.ip}")
    ip_obj = ipaddress.ip_address(body.ip)
    return IPResponse(
        ip=body.ip, valido=True, version=ip_obj.version, es_privada=ip_obj.is_private
    )


@app.post("/analyze", response_model=SubnetResponse)
def analizar_red(body: CIDRRequest):
    """Analiza una red CIDR de forma segura."""
    logger.info(f"[ANALYZE] CIDR recibido: {body.cidr}")
    try:
        data = analizar_subred(body.cidr)
        return SubnetResponse(**data)
    except ValueError as e:
        logger.error(f"[ANALYZE] Error: {e}")
        raise HTTPException(status_code=400, detail=str(e)) from None


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "timestamp": logger.handlers[0].formatter.formatTime(
            logger.makeRecord("", 0, "", 0, "", (), None), "%Y-%m-%dT%H:%M:%S"
        ),
    }
