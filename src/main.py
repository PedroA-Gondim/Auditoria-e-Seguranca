# src/main.py
import sys
import os

# Correção de caminho
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.gen import GEN
from src.enc import ENC
from src.dec import DEC
from src.utils import texto_para_binario, binario_para_texto, ajustar_tamanho_msg


def main():
    print("=== Trabalho de Criptografia Simplificada ===\n")

    # ETAPA 1: ENTRADA DE DADOS E CONVERSÃO PARA REPRESENTAÇÃO BINÁRIA
    texto_seed = input("Digite a seed (texto): ")
    seed_bits = texto_para_binario(texto_seed)

    # A mensagem a ser protegida é convertida para binário.
    # Esta é a informação sensível que será cifrada usando XOR.
    texto_msg = input("Digite a mensagem a ser criptografada: ")
    msg_bits_original = texto_para_binario(texto_msg)

    # ETAPA 2: GERAÇÃO DA CHAVE
    K = GEN(seed_bits)

    # ETAPA 3: PREENCHIMENTO DA MENSAGEM (PADDING)
    # Conceito: Para aplicar XOR bit a bit, mensagem e chave devem ter tamanho igual.
    # Caso contrário, não há bits de chave suficientes para cifrar toda a mensagem.
    # Solução: Adicionar bits de preenchimento (padding) ao final da mensagem.
    msg_bits_pad = ajustar_tamanho_msg(msg_bits_original, len(K))

    # EXIBIÇÃO DE INFORMAÇÕES SOBRE O PROCESSAMENTO
    print("1. Resumo dos Tamanhos em Bits:")
    print(f"   Seed: {len(seed_bits)} bits")
    print(f"   Chave Expandida (4x): {len(K)} bits")
    print(f"   Mensagem Original: {len(msg_bits_original)} bits")
    print(f"   Mensagem com Padding: {len(msg_bits_pad)} bits")

    # ETAPA 4: CIFRA (ENCRYPTION) - APLICAÇÃO DO ALGORITMO XOR
    C = ENC(K, msg_bits_pad)
    print("\n2. Texto Cifrado (primeiros 50 bits):")
    print("".join(map(str, C[:50])) + "...")

    # ETAPA 5: DECIFRAGEM (DECRYPTION) - RECUPERAÇÃO DA MENSAGEM ORIGINAL
    M_recuperada_bits = DEC(K, C)
    texto_recuperado = binario_para_texto(M_recuperada_bits)

    print("\n3. Resultado da Decifragem:")
    print(f"   Mensagem Recuperada: '{texto_recuperado}'")
    print("\nNota: Bytes de padding (nulos) podem aparecer no final da mensagem.")


if __name__ == "__main__":
    main()
