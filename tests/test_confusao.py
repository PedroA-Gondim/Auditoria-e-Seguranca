# tests/test_confusao.py
import sys
import os
import copy

# Correção de caminho
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.gen import GEN
from src.enc import ENC
from src.utils import texto_para_binario, ajustar_tamanho_msg

def contar_bits_diferentes(lista1: list[int], lista2: list[int]) -> int:
    diferencas = 0
    for b1, b2 in zip(lista1, lista2):
        if b1 != b2: diferencas += 1
    return diferencas

def teste_confusao():
    print("=== INICIANDO TESTE DE CONFUSÃO ===")
    print("Objetivo: Manter MENSAGEM fixa, alterar 1 bit da SEED e ver impacto na Cifra.\n")

    # 1. Configuração Fixa
    msg_texto = "Mensagem fixa para teste de confusao"
    msg_bits = texto_para_binario(msg_texto)
    
    # 2. Seed Original
    seed_texto = "segredo"
    seed_bits_original = texto_para_binario(seed_texto)
    
    # Gera Chave 1 e Cifra 1
    chave1 = GEN(seed_bits_original)
    
    # Ajustar mensagem ao tamanho da chave (que depende da seed)
    msg_bits_ajustada = ajustar_tamanho_msg(msg_bits, len(chave1))
    cifra1 = ENC(chave1, msg_bits_ajustada)

    # 3. Loop de Teste (Alterando a Seed)
    total_bits_cifra = len(cifra1)
    soma_diferencas = 0
    bits_testados = 0
    
    # Vamos alterar cada bit da seed
    limite_teste = min(50, len(seed_bits_original))

    print(f"Testando alteração de 1 bit na SEED (nos primeiros {limite_teste} bits)...")
    print("-" * 65)
    print(f"{'Bit Seed Alt.':<15} | {'Bits Mudados na Cifra':<25} | {'% Mudança':<10}")
    print("-" * 65)

    for i in range(limite_teste):
        # Altera 1 bit da seed
        seed_alterada = copy.deepcopy(seed_bits_original)
        seed_alterada[i] = 1 - seed_alterada[i]

        # Gera NOVA chave com a seed alterada
        chave2 = GEN(seed_alterada)
        
        # Criptografa a MESMA mensagem com a NOVA chave
        cifra2 = ENC(chave2, msg_bits_ajustada)

        # Mede a diferença entre Cifra 1 e Cifra 2
        diff = contar_bits_diferentes(cifra1, cifra2)
        
        soma_diferencas += diff
        bits_testados += 1
        
        porcentagem = (diff / total_bits_cifra) * 100
        print(f"Índice {i:<8} | {diff:<25} | {porcentagem:.2f}%")

    # 4. Resultados
    media_confusao = soma_diferencas / bits_testados
    print("-" * 65)
    print(f"\nRESULTADO FINAL DE CONFUSÃO:")
    print(f"Média de bits alterados na cifra: {media_confusao:.2f}")
    print(f"Taxa de Confusão Média: {(media_confusao/total_bits_cifra)*100:.2f}%")
    
    if media_confusao > 1:
        print("\n[ANÁLISE]: Boa confusão!")
        print("Mudar a seed alterou drasticamente a chave e, consequentemente, a cifra.")
    else:
        print("\n[ANÁLISE]: Confusão baixa. Verifique sua função GEN.")

if __name__ == "__main__":
    teste_confusao()