import logging
import os
from logging.handlers import RotatingFileHandler


def configurar_logger(
    nombre: str = "ip_tools", archivo_log: str = "logs/audit.log"
) -> logging.Logger:
    """Configura logging con rotación automática y formato forense."""
    os.makedirs("logs", exist_ok=True)

    logger = logging.getLogger(nombre)
    logger.setLevel(logging.INFO)

    # Evitar duplicar handlers si se importa varias veces
    if not logger.handlers:
        handler = RotatingFileHandler(
            archivo_log, maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
        )
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        # Opcional: mostrar también en consola
        console = logging.StreamHandler()
        console.setLevel(logging.WARNING)
        logger.addHandler(console)

    return logger
