# src/main.py
from gen import GEN
from enc import ENC
from dec import DEC
from utils import texto_para_binario, binario_para_texto


def main():
    print("=== Trabalho de Criptografia Simplificada ===")
    
    # 1. Definir Entrada
    texto_seed = "amor" # Seed pequena
    seed_bits = texto_para_binario(texto_seed)
    
    # O enunciado diz que a Chave é 4x a Seed.
    # LOGO, a Mensagem também precisa ter esse tamanho para o ENC funcionar (1:1).
    # Vamos criar uma mensagem dummy para testar o tamanho.
    tamanho_necessario = 4 * len(seed_bits)
    texto_msg = "ai  " * 4 # Ajuste grosseiro só para exemplo
    msg_bits = texto_para_binario(texto_msg)
    
    # Ajuste fino para garantir que msg tenha o mesmo tamanho da chave gerada
    # (No trabalho real, você talvez precise de padding na utils)
    msg_bits = msg_bits[:tamanho_necessario] 

    print(f"\n1. Dados Iniciais:")
    print(f"   Seed (texto): {texto_seed}")
    print(f"   Seed (bits):  {seed_bits} (Tam: {len(seed_bits)})")
    print(f"   Msg (bits):   {msg_bits} (Tam: {len(msg_bits)})")

    # 2. Geração de Chave (GEN)
    K = GEN(seed_bits)
    print(f"\n2. Chave Gerada (GEN):")
    print(f"   K: {K}")
    print(f"   Tamanho K: {len(K)} (Esperado: {4 * len(seed_bits)})")

    # 3. Criptografia (ENC)
    C = ENC(K, msg_bits)
    print(f"\n3. Criptografia (ENC):")
    print(f"   Cifra: {C}")

    # 4. Descriptografia (DEC)
    M_recuperada = DEC(K, C)
    print(f"\n4. Descriptografia (DEC):")
    print(f"   Recuperado: {M_recuperada}")
    
    # Validação
    if msg_bits == M_recuperada:
        print("\nSUCESSO: A mensagem descriptografada é igual a original!")
        print(f"Texto recuperado: {binario_para_texto(M_recuperada)}")
    else:
        print("\nFALHA: A mensagem recuperada é diferente.")

if __name__ == "__main__":
    main()