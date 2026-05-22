import pytest
from ip_validator import es_ip_valida

def test_ipv4_valida():
    assert es_ip_valida("192.168.1.1") is True

def test_ip_invalida():
    assert es_ip_valida("999.999.999.999") is False
    assert es_ip_valida("esto_no_es_ip") is False

def test_ip_vacia_o_mal_formato():
    assert es_ip_valida("") is False
    assert es_ip_valida("  10.0.0.1  ") is True  # si usas .strip()