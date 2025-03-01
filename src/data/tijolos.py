import json
import os

ARQUIVO_TIJOLOS = os.path.join(os.path.dirname(__file__), "tijolos.json")

TIJOLOS_PADRAO = {
    "Tijolo 8 Furos (9x19x19)": {"nome": "Tijolo 8 Furos", "largura": 0.19, "altura": 0.19, "profundidade": 0.09, "preco_unitario": 1.20},
    "Tijolo 6 Furos (9x14x24)": {"nome": "Tijolo 6 Furos", "largura": 0.24, "altura": 0.14, "profundidade": 0.09, "preco_unitario": 0.90},
    "Bloco Cerâmico (14x19x29)": {"nome": "Bloco Cerâmico", "largura": 0.29, "altura": 0.19, "profundidade": 0.14, "preco_unitario": 1.50},
}


def carregar_tijolos():
    """Carrega os dados dos tijolos do arquivo JSON"""
    try:
        if not os.path.exists(ARQUIVO_TIJOLOS):
            salvar_tijolos(TIJOLOS_PADRAO)
            return TIJOLOS_PADRAO

        with open(ARQUIVO_TIJOLOS, encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except Exception as e:
        print(f"Erro ao carregar tijolos: {e}")
        return TIJOLOS_PADRAO


def salvar_tijolos(tijolos):
    """Salva os dados dos tijolos no arquivo JSON"""
    try:
        with open(ARQUIVO_TIJOLOS, "w", encoding="utf-8") as arquivo:
            json.dump(tijolos, arquivo, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Erro ao salvar tijolos: {e}")
        return False
