# src/main.py
import sys
import os

# Adiciona o diretório raiz ao caminho
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.gen import GEN
from src.enc import ENC
from src.dec import DEC


def main():
    print("=== Trabalho de Criptografia Baseada em Campeões do TFT ===\n")

    # Entrada de dados
    texto_seed = input("Digite a seed (texto): ")
    num1_seed = input("Digite um número inteiro para a escolha do campeão: ")
    num2_seed = input("Digite outro número inteiro para a quantidade de estrelas: ")
    texto_msg = input("Digite a mensagem a ser criptografada: ")

    champ_val = int(num1_seed) if num1_seed.strip() else 0
    stars_val = int(num2_seed) if num2_seed.strip() else 1

    # Geração da chave
    K, nome, estrelas = GEN(texto_seed, int(champ_val), int(stars_val))

    # Exibição de informações
    print(f"Entrada Usuário: Campeão={champ_val}, Estrelas={stars_val}")
    print(f"Sistema Interpretou: Campeão='{nome}', Estrelas={estrelas}")
    print("Chave gerada com sucesso!")
    print(f"   Tamanho original da seed: {len(texto_seed) * 8} bits")
    print(f"   Chave expandida (4x): {len(K)} bits")
    print(f"   Mensagem original: {texto_msg}")

    # Criptografia
    C = ENC(K, texto_msg)
    print("\nTexto cifrado:")
    print("".join(map(str, C)))

    # Descriptografia
    M_recuperada = DEC(K, C)
    print("\nResultado da descriptografia:")
    print(f"   Mensagem recuperada: '{M_recuperada}'")


if __name__ == "__main__":
    main()
