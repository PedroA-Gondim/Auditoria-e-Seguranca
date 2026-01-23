# src/main.py
import sys
import os

# Correção de caminho
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.gen import GEN
from src.enc import ENC
from src.dec import DEC
from src.utils import texto_para_binario, binario_para_texto, ajustar_tamanho_msg

def main():
    print("=== Trabalho de Criptografia Simplificada ===\n")
    
    # 1. Entrada
    texto_seed = "gsi035" # Exemplo
    seed_bits = texto_para_binario(texto_seed)
    
    texto_msg = "Teste de mensagem para criptografia"
    msg_bits_original = texto_para_binario(texto_msg)

    # 2. Gera Chave
    # Pela regra: Chave = 4x Seed
    K = GEN(seed_bits)
    
    # 3. Prepara Mensagem (Padding)
    # A mensagem TEM que ter o tamanho da chave para o XOR funcionar 1:1
    msg_bits_pad = ajustar_tamanho_msg(msg_bits_original, len(K))

    print(f"1. Resumo dos Tamanhos:")
    print(f"   Seed: {len(seed_bits)} bits")
    print(f"   Chave (4x Seed): {len(K)} bits")
    print(f"   Msg Original: {len(msg_bits_original)} bits")
    print(f"   Msg Ajustada: {len(msg_bits_pad)} bits")

    # 4. Criptografia
    C = ENC(K, msg_bits_pad)
    print(f"\n2. Cifra gerada (primeiros 50 bits): {C[:50]}...")

    # 5. Descriptografia
    M_recuperada_bits = DEC(K, C)
    texto_recuperado = binario_para_texto(M_recuperada_bits)
    
    print(f"\n3. Resultado:")
    print(f"   Texto Recuperado: '{texto_recuperado}'") 
    # Nota: O texto recuperado pode ter caracteres nulos (padding) no final, 
    # mas o começo deve estar legível.

if __name__ == "__main__":
    main()