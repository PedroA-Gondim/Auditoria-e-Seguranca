# tests/test_difusao.py
import sys
import os
import copy

# --- CORREÇÃO DE IMPORTAÇÃO ---
# Adiciona a pasta raiz do projeto ao caminho do Python
# Isso permite que o script encontre a pasta 'src'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Agora importamos de 'src.arquivo'
from src.gen import GEN
from src.enc import ENC
from src.utils import texto_para_binario, ajustar_tamanho_msg

def contar_bits_diferentes(lista1: list[int], lista2: list[int]) -> int:
    """Compara duas listas binárias e conta quantos bits são diferentes."""
    diferencas = 0
    for b1, b2 in zip(lista1, lista2):
        if b1 != b2:
            diferencas += 1
    return diferencas

def teste_difusao():
    print("=== INICIANDO TESTE DE DIFUSÃO ===")
    print("Objetivo: Avaliar quantos bits mudam na Cifra ao alterar 1 bit na Mensagem.\n")

    # 1. Configuração
    seed_texto = "chave_mestra"
    seed_bits = texto_para_binario(seed_texto)
    chave = GEN(seed_bits)

    msg_texto = "Testando a difusao do algoritmo"
    msg_bits_original = texto_para_binario(msg_texto)
    msg_bits_original = ajustar_tamanho_msg(msg_bits_original, len(chave))

    # 2. Cifra Base
    cifra_original = ENC(chave, msg_bits_original)

    # 3. Teste
    total_bits = len(msg_bits_original)
    soma_diferencas = 0
    bits_testados = 0
    limite_teste = min(50, total_bits)

    print(f"Testando alteração de 1 bit (nos primeiros {limite_teste} bits da mensagem)...")
    print("-" * 60)
    print(f"{'Bit Alterado':<15} | {'Bits Mudados na Cifra':<25} | {'% Mudança':<10}")
    print("-" * 60)

    for i in range(limite_teste):
        msg_alterada = copy.deepcopy(msg_bits_original)
        msg_alterada[i] = 1 - msg_alterada[i] # Flip bit

        cifra_nova = ENC(chave, msg_alterada)
        diff = contar_bits_diferentes(cifra_original, cifra_nova)
        
        soma_diferencas += diff
        bits_testados += 1
        
        porcentagem = (diff / total_bits) * 100
        print(f"Índice {i:<8} | {diff:<25} | {porcentagem:.2f}%")

    # 4. Resultados
    media_difusao = soma_diferencas / bits_testados
    print("-" * 60)
    print(f"Média de bits alterados na cifra: {media_difusao:.2f}")
    print(f"Taxa de Difusão Média: {(media_difusao/total_bits)*100:.2f}%")

if __name__ == "__main__":
    teste_difusao()