import ipaddress

def es_ip_valida(ip: str) -> bool:
    """Valida si un string es una dirección IPv4 o IPv6 correcta."""
    ip = ip.strip()
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    
    pruebas = ["192.168.1.1", "2001:db8::1", "999.999.999.999", "hola"]
    for ip in pruebas:
        resultado = es_ip_valida(ip)
        logging.info(f"IP: {ip:<20} | Válida: {resultado}")