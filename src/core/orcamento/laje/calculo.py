"""Módulo com funções de cálculo para lajes."""

from .tipos_laje import CM_TO_M, TipoLaje, carregar_tipos_laje

# Carrega os tipos de laje
TIPOS_LAJE = carregar_tipos_laje()


def calcular_volume_laje(comprimento: float, largura: float, espessura: float, tipo_laje: str) -> float:
    """
    Calcula o volume da laje de acordo com o tipo selecionado.

    Args:
        comprimento: Comprimento da laje em metros
        largura: Largura da laje em metros
        espessura: Espessura da laje em centímetros (convertida para metros internamente)
        tipo_laje: Tipo de laje (MACICA, NERVURADA ou PRE_MOLDADA)

    Returns:
        Volume da laje em metros cúbicos
    """
    # Converte espessura de cm para m
    espessura_m = espessura * CM_TO_M

    if tipo_laje == TipoLaje.MACICA.name:
        # Cálculo para laje maciça: comprimento x largura x espessura
        return comprimento * largura * espessura_m

    elif tipo_laje == TipoLaje.NERVURADA.name:
        # Dados da laje nervurada
        dados_laje = TIPOS_LAJE.get("Laje Nervurada", {})
        esp_mesa = dados_laje.get("espessura_mesa", 5.0) * CM_TO_M
        dist_nervuras = dados_laje.get("dist_nervuras", 50.0) * CM_TO_M

        # Cálculo para laje nervurada: área da mesa + volume das nervuras
        area_mesa = comprimento * largura
        volume_mesa = area_mesa * esp_mesa

        # Cálculo do número de nervuras (aproximado)
        num_nervuras_x = comprimento / dist_nervuras
        num_nervuras_y = largura / dist_nervuras

        # Volume das nervuras (altura da nervura = espessura total - espessura da mesa)
        altura_nervura = espessura_m - esp_mesa
        volume_nervuras = (num_nervuras_x * largura + num_nervuras_y * comprimento) * 0.1 * altura_nervura

        return volume_mesa + volume_nervuras

    elif tipo_laje == TipoLaje.PRE_MOLDADA.name:
        # Dados da laje pré-moldada
        dados_laje = TIPOS_LAJE.get("Laje Pré-Moldada", {})
        tamanho_padrao = dados_laje.get("tamanho_padrao", {"largura": 1.25, "comprimento": 5.0})

        # Cálculo para laje pré-moldada
        # Simplificação: consideramos que cada placa tem um volume uniforme
        area_laje = comprimento * largura
        area_placa = tamanho_padrao["largura"] * tamanho_padrao["comprimento"]
        num_placas = area_laje / area_placa

        return num_placas * area_placa * espessura_m

    # Caso não seja nenhum tipo conhecido, usa o cálculo padrão
    return comprimento * largura * espessura_m


def calcular_custo_laje(volume: float, valor_m3: float) -> float:
    """
    Calcula o custo total da laje com base no volume e valor por m³.

    Args:
        volume: Volume da laje em metros cúbicos
        valor_m3: Valor por metro cúbico em reais

    Returns:
        Custo total da laje em reais
    """
    return volume * valor_m3


def calcular_peso_laje(volume: float, tipo_laje: str) -> float:
    """
    Calcula o peso aproximado da laje com base no volume e tipo.

    Args:
        volume: Volume da laje em metros cúbicos
        tipo_laje: Tipo de laje

    Returns:
        Peso da laje em kg
    """
    # Obtém a densidade do tipo de laje
    densidade = 2500  # Densidade padrão do concreto (kg/m³)

    if tipo_laje == TipoLaje.MACICA.name:
        densidade = TIPOS_LAJE.get("Laje Maciça", {}).get("densidade", 2500)
    elif tipo_laje == TipoLaje.NERVURADA.name:
        densidade = TIPOS_LAJE.get("Laje Nervurada", {}).get("densidade", 1800)
    elif tipo_laje == TipoLaje.PRE_MOLDADA.name:
        densidade = TIPOS_LAJE.get("Laje Pré-Moldada", {}).get("densidade", 1600)

    return volume * densidade


def calcular_materiais_laje(volume: float, tipo_laje: str) -> dict:
    """
    Calcula a quantidade aproximada de materiais necessários para a laje.

    Args:
        volume: Volume da laje em metros cúbicos
        tipo_laje: Tipo de laje

    Returns:
        Dicionário com as quantidades de materiais
    """
    # Valores aproximados de consumo de materiais por m³ de concreto
    consumo_aco = 80.0  # kg/m³ para laje maciça
    consumo_cimento = 350.0  # kg/m³
    consumo_areia = 0.8  # m³/m³
    consumo_brita = 0.8  # m³/m³

    # Ajusta o consumo de aço de acordo com o tipo de laje
    if tipo_laje == TipoLaje.NERVURADA.name:
        consumo_aco = 60.0  # kg/m³
    elif tipo_laje == TipoLaje.PRE_MOLDADA.name:
        consumo_aco = 40.0  # kg/m³

    return {
        "aco": volume * consumo_aco,  # kg
        "cimento": volume * consumo_cimento,  # kg
        "areia": volume * consumo_areia,  # m³
        "brita": volume * consumo_brita,  # m³
    }
