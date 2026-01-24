# tests/test_difusao.py
import sys
import os
import copy

# --- CONFIGURAÇÃO DO CAMINHO DE IMPORTAÇÃO ---
# O Python precisa saber onde encontrar os módulos do projeto
# Adicionamos o diretório raiz ao sys.path para acessar a pasta 'src'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importamos as funções necessárias para o teste
from src.gen import GEN  # Gerador de chaves
from src.enc import ENC  # Função de encriptação
from src.utils import texto_para_binario, ajustar_tamanho_msg

def contar_bits_diferentes(lista1: list[int], lista2: list[int]) -> int:
    """Compara dois vetores de bits e retorna quantos bits são diferentes."""
    diferencas = 0
    for b1, b2 in zip(lista1, lista2):
        if b1 != b2:
            diferencas += 1
    return diferencas

def teste_difusao():
    print("=== INICIANDO TESTE DE DIFUSÃO ===")
    print("Objetivo: Avaliar quantos bits mudam na Cifra ao alterar 1 bit na Mensagem.\n")

    # ETAPA 1: GERAÇÃO DA CHAVE
    # Convertemos o texto da chave em uma sequência de bits
    seed_texto = "chave_mestra"
    seed_bits = texto_para_binario(seed_texto)
    # Usamos o gerador para expandir esses bits em uma chave maior
    chave = GEN(seed_bits)

    # ETAPA 2: PREPARAÇÃO DA MENSAGEM ORIGINAL
    # Convertemos o texto da mensagem em bits
    msg_texto = "Testando a difusao do algoritmo"
    msg_bits_original = texto_para_binario(msg_texto)
    # Ajustamos o tamanho para corresponder ao tamanho da chave
    msg_bits_original = ajustar_tamanho_msg(msg_bits_original, len(chave))

    # ETAPA 3: ENCRIPTAÇÃO DA MENSAGEM ORIGINAL
    # Geramos a cifra base sem nenhuma alteração na mensagem
    cifra_original = ENC(chave, msg_bits_original)

    # ETAPA 4: CONFIGURAÇÃO DO TESTE DE DIFUSÃO
    total_bits = len(msg_bits_original)  # Total de bits na mensagem
    soma_diferencas = 0  # Acumulador para calcular a média
    bits_testados = 0    # Contador de bits testados
    limite_teste = min(50, total_bits)  # Testamos até 50 bits (ou menos se houver menos)

    print(f"Testando alteração de 1 bit (nos primeiros {limite_teste} bits da mensagem)...")
    print("-" * 60)
    print(f"{'Bit Alterado':<15} | {'Bits Mudados na Cifra':<25} | {'% Mudança':<10}")
    print("-" * 60)

    # ETAPA 5: LOOP DE TESTE
    # Para cada bit, fazemos: alterar → encriptar → comparar
    for i in range(limite_teste):
        # Criamos uma cópia da mensagem original
        msg_alterada = copy.deepcopy(msg_bits_original)
        # Alteramos o bit na posição i (inverte 0→1 ou 1→0)
        msg_alterada[i] = 1 - msg_alterada[i]

        # Encriptamos a mensagem alterada com a mesma chave
        cifra_nova = ENC(chave, msg_alterada)
        # Contamos quantos bits mudaram na cifra
        diff = contar_bits_diferentes(cifra_original, cifra_nova)
        
        # Acumulamos os resultados
        soma_diferencas += diff
        bits_testados += 1
        
        # Calculamos a porcentagem de bits que mudaram
        porcentagem = (diff / total_bits) * 100
        print(f"Índice {i:<8} | {diff:<25} | {porcentagem:.2f}%")

    # ETAPA 6: CÁLCULO E EXIBIÇÃO DOS RESULTADOS
    # Calculamos a média de bits alterados por teste
    media_difusao = soma_diferencas / bits_testados
    print("-" * 60)
    print(f"Média de bits alterados na cifra: {media_difusao:.2f}")
    # A taxa de difusão indica o quanto a cifra se altera (quanto maior, melhor)
    print(f"Taxa de Difusão Média: {(media_difusao/total_bits)*100:.2f}%")

if __name__ == "__main__":
    teste_difusao()