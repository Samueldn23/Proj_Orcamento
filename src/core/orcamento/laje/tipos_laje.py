"""Módulo para definição dos tipos de laje e suas constantes."""

import json
import os
from enum import Enum

# Constantes
CM_TO_M = 0.01
MIN_COMPRIMENTO = 1.0  # Comprimento mínimo em metros
MAX_COMPRIMENTO = 50.0  # Comprimento máximo em metros
MIN_LARGURA = 1.0  # Largura mínima em metros
MAX_LARGURA = 50.0  # Largura máxima em metros
MIN_ESPESSURA = 1.0  # Espessura mínima em centímetros
MAX_ESPESSURA = 50.0  # Espessura máxima em centímetros
MIN_VALOR_M3 = 1.0  # Valor mínimo por m³ em reais
MAX_VALOR_M3 = 10000.0  # Valor máximo por m³ em reais

ARQUIVO_LAJES = os.path.join(os.path.dirname(__file__), "tipos_laje.json")


class TipoLaje(Enum):
    """Enum para representar os tipos de laje."""

    MACICA = "Laje Maciça"
    NERVURADA = "Laje Nervurada"
    PRE_MOLDADA = "Laje Pré-Moldada"


LAJES_PADRAO = {
    "Laje Maciça": {
        "nome": "Laje Maciça",
        "descricao": "Laje de concreto armado maciço",
        "densidade": 2500,  # kg/m³
        "espessura_recomendada": 10.0,  # cm
        "preco_medio_m3": 500.0,  # R$/m³
    },
    "Laje Nervurada": {
        "nome": "Laje Nervurada",
        "descricao": "Laje com nervuras e elementos de enchimento",
        "densidade": 1800,  # kg/m³
        "espessura_recomendada": 25.0,  # cm
        "preco_medio_m3": 450.0,  # R$/m³
        "espessura_mesa": 5.0,  # cm
        "dist_nervuras": 50.0,  # cm
    },
    "Laje Pré-Moldada": {
        "nome": "Laje Pré-Moldada",
        "descricao": "Laje com vigotas pré-moldadas e elementos de enchimento",
        "densidade": 1600,  # kg/m³
        "espessura_recomendada": 12.0,  # cm
        "preco_medio_m3": 400.0,  # R$/m³
        "tamanho_padrao": {"largura": 1.25, "comprimento": 5.0},  # m
    },
}


def carregar_tipos_laje():
    """Carrega os dados dos tipos de laje do arquivo JSON"""
    try:
        if not os.path.exists(ARQUIVO_LAJES):
            salvar_tipos_laje(LAJES_PADRAO)
            return LAJES_PADRAO

        with open(ARQUIVO_LAJES, encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except Exception as e:
        print(f"Erro ao carregar tipos de laje: {e}")
        return LAJES_PADRAO


def salvar_tipos_laje(tipos_laje):
    """Salva os dados dos tipos de laje no arquivo JSON"""
    try:
        with open(ARQUIVO_LAJES, "w", encoding="utf-8") as arquivo:
            json.dump(tipos_laje, arquivo, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Erro ao salvar tipos de laje: {e}")
        return False
