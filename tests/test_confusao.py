# tests/test_confusao.py
import sys
import os
import copy

# Adiciona o diretório pai ao caminho para importar módulos do projeto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.gen import GEN
from src.enc import ENC
from src.utils import texto_para_binario, ajustar_tamanho_msg

def contar_bits_diferentes(lista1: list[int], lista2: list[int]) -> int:
    """Compara duas listas de bits e retorna quantos bits são diferentes"""
    diferencas = 0
    for b1, b2 in zip(lista1, lista2):
        if b1 != b2:
            diferencas += 1
    return diferencas

def teste_confusao():
    """
    Teste de Confusão: Verifica se pequenas mudanças na SEED (chave) 
    causam grandes mudanças na cifra gerada (propriedade desejada em criptografia)
    """
    print("=== INICIANDO TESTE DE CONFUSÃO ===")
    print("Objetivo: Manter MENSAGEM fixa, alterar 1 bit da SEED e ver impacto na Cifra.\n")

    # ============ ETAPA 1: PREPARAÇÃO DA MENSAGEM ============
    # Define uma mensagem que será usada em TODOS os testes (nunca muda)
    msg_texto = "Mensagem fixa para teste de confusao"
    msg_bits = texto_para_binario(msg_texto)  # Converte texto em bits
    
    # ============ ETAPA 2: PREPARAÇÃO DA SEED ORIGINAL ============
    # Define a seed (senha) inicial que será ligeiramente alterada nos testes
    seed_texto = "segredo"
    seed_bits_original = texto_para_binario(seed_texto)  # Converte em bits
    
    # ============ ETAPA 3: PRIMEIRA CRIPTOGRAFIA (com seed original) ============
    # Usa a função GEN para gerar uma chave a partir da seed
    chave1 = GEN(seed_bits_original)
    
    # Ajusta a mensagem para o tamanho da chave gerada
    msg_bits_ajustada = ajustar_tamanho_msg(msg_bits, len(chave1))
    
    # Criptografa a mensagem com a chave 1
    cifra1 = ENC(chave1, msg_bits_ajustada)

    # ============ ETAPA 4: PREPARAÇÃO PARA TESTES MÚLTIPLOS ============
    # Armazena o tamanho da cifra para calcular porcentagens depois
    total_bits_cifra = len(cifra1)
    soma_diferencas = 0  # Acumula o total de bits diferentes
    bits_testados = 0  # Conta quantos testes foram feitos
    
    # Limita o teste aos primeiros 50 bits da seed (ou menos se a seed for pequena)
    limite_teste = min(50, len(seed_bits_original))

    print(f"Testando alteração de 1 bit na SEED (nos primeiros {limite_teste} bits)...")
    print("-" * 65)
    print(f"{'Bit Seed Alt.':<15} | {'Bits Mudados na Cifra':<25} | {'% Mudança':<10}")
    print("-" * 65)

    # ============ ETAPA 5: LOOP PRINCIPAL - TESTE DE CADA BIT ============
    for i in range(limite_teste):
        # Cria uma cópia da seed original
        seed_alterada = copy.deepcopy(seed_bits_original)
        
        # Altera exatamente 1 bit desta seed (inverte: 0→1 ou 1→0)
        seed_alterada[i] = 1 - seed_alterada[i]

        # Gera uma NOVA chave usando a seed alterada
        chave2 = GEN(seed_alterada)
        
        # Criptografa a MESMA mensagem com a NOVA chave
        # (Isso mostra o impacto de apenas 1 bit alterado na seed)
        cifra2 = ENC(chave2, msg_bits_ajustada)

        # Compara a cifra original (cifra1) com a nova cifra (cifra2)
        # Conta quantos bits mudaram
        diff = contar_bits_diferentes(cifra1, cifra2)
        
        # Acumula os resultados
        soma_diferencas += diff
        bits_testados += 1
        
        # Calcula a porcentagem de bits que mudaram em relação ao total
        porcentagem = (diff / total_bits_cifra) * 100
        print(f"Índice {i:<8} | {diff:<25} | {porcentagem:.2f}%")

    # ============ ETAPA 6: ANÁLISE DOS RESULTADOS ============
    # Calcula a média de bits alterados entre todos os testes
    media_confusao = soma_diferencas / bits_testados
    
    print("-" * 65)
    print(f"\nRESULTADO FINAL DE CONFUSÃO:")
    print(f"Média de bits alterados na cifra: {media_confusao:.2f}")
    print(f"Taxa de Confusão Média: {(media_confusao/total_bits_cifra)*100:.2f}%")
    
    # ============ ETAPA 7: INTERPRETAÇÃO ============
    # Se a média for alta, significa que pequenas mudanças na seed
    # causam grandes mudanças na cifra (propriedade desejada!)
    if media_confusao > 1:
        print("\n[ANÁLISE]: Boa confusão!")
        print("Mudar a seed alterou drasticamente a chave e, consequentemente, a cifra.")
    else:
        print("\n[ANÁLISE]: Confusão baixa. Verifique sua função GEN.")

if __name__ == "__main__":
    teste_confusao()