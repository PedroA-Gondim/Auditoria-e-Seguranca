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
    
    # ETAPA 1: ENTRADA DE DADOS
    # Solicita ao usuário a seed (chave inicial em formato texto)
    # A seed será convertida para binário para gerar a chave criptográfica
    texto_seed = input("Digite a seed (texto): ")
    seed_bits = texto_para_binario(texto_seed)
    
    # Solicita a mensagem que será criptografada
    # Esta mensagem será convertida para binário para aplicar o XOR
    texto_msg = input("Digite a mensagem a ser criptografada: ")
    msg_bits_original = texto_para_binario(texto_msg)

    # ETAPA 2: GERAÇÃO DA CHAVE CRIPTOGRÁFICA
    # A função GEN expande a seed em uma chave maior (4x o tamanho)
    # Isso aumenta a segurança ao distribuir os bits da seed
    K = GEN(seed_bits)
    
    # ETAPA 3: AJUSTE DE TAMANHO DA MENSAGEM (PADDING)
    # Para o XOR funcionar corretamente (bit a bit), mensagem e chave
    # devem ter o mesmo tamanho. Se a mensagem é menor, adiciona-se
    # bits de preenchimento (padding) ao final
    msg_bits_pad = ajustar_tamanho_msg(msg_bits_original, len(K))

    # EXIBIÇÃO DE INFORMAÇÕES SOBRE O PROCESSAMENTO
    # Mostra os tamanhos em bits de cada etapa para entender a transformação
    print("1. Resumo dos Tamanhos:")
    print(f"   Seed: {len(seed_bits)} bits")
    print(f"   Chave (4x Seed): {len(K)} bits")
    print(f"   Msg Original: {len(msg_bits_original)} bits")
    print(f"   Msg Ajustada: {len(msg_bits_pad)} bits")

    # ETAPA 4: CRIPTOGRAFIA (CIFRAGEM)
    # Aplica a operação XOR entre a chave e a mensagem
    # Resultado: texto cifrado que parece aleatório sem a chave
    C = ENC(K, msg_bits_pad)
    print("\n2. Cifra gerada (primeiros 50 bits):")
    print(''.join(map(str, C[:50])) + "...")

    # ETAPA 5: DESCRIPTOGRAFIA (DECIFRAGEM)
    # Aplica o XOR novamente com a mesma chave para recuperar a mensagem original
    # Propriedade do XOR: (A XOR B) XOR B = A
    M_recuperada_bits = DEC(K, C)
    texto_recuperado = binario_para_texto(M_recuperada_bits)
    
    print("\n3. Resultado:")
    print(f"   Texto Recuperado: '{texto_recuperado}'")
    # Observação: Podem haver caracteres nulos (bytes de padding) no final,
    # mas o texto original estará no início e será legível.

if __name__ == "__main__":
    main()