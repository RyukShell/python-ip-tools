import ipaddress

from logger_config import configurar_logger

logger = configurar_logger("subnet_analyzer")


def analizar_subred(cidr: str) -> dict:
    """Analiza una red en formato CIDR y retorna métricas estructuradas."""
    try:
        network = ipaddress.ip_network(cidr, strict=False)
        usable_count = network.num_addresses - 2 if network.num_addresses > 2 else 0

        return {
            "network_address": str(network.network_address),
            "broadcast_address": str(network.broadcast_address),
            "netmask": str(network.netmask),
            "first_usable": str(network[1]) if usable_count > 0 else "N/A",
            "last_usable": str(network[-2]) if usable_count > 0 else "N/A",
            "total_hosts": network.num_addresses,
            "usable_hosts_count": usable_count,
            "is_private": network.is_private,
            "is_global": network.is_global,
        }
    except ValueError as e:
        logger.error(f"❌ CIDR inválido '{cidr}': {e}")
        raise


if __name__ == "__main__":
    import json

    ejemplos = ["192.168.1.0/24", "10.0.0.0/30", "172.16.0.1/16", "not_a_cidr"]
    for cidr in ejemplos:
        try:
            resultado = analizar_subred(cidr)
            logger.info(f"✅ Analizado: {cidr} -> {json.dumps(resultado, indent=2)}")
        except ValueError:
            logger.warning(f"⏭️ Saltado: {cidr}")
