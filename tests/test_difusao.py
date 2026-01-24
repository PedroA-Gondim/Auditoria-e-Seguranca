# tests/test_difusao.py
import sys
import os
import copy

# --- CONFIGURAÇÃO DO CAMINHO DE IMPORTAÇÃO ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.gen import GEN
from src.enc import ENC
from src.utils import texto_para_binario, ajustar_tamanho_msg


def contar_bits_diferentes(lista1: list[int], lista2: list[int]) -> int:
    """Compara dois vetores de bits e retorna quantos bits são diferentes."""
    diferencas = 0
    for b1, b2 in zip(lista1, lista2):
        if b1 != b2:
            diferencas += 1
    return diferencas


def run():
    print("\n>>> [3/4] Executando Teste de Difusão\n")

    # Passo 1: GERAÇÃO DA CHAVE CRIPTOGRÁFICA
    print("[Passo 1] Geração da Chave")
    print("-" * 60)
    seed_texto = "chave_mestra"
    seed_bits = texto_para_binario(seed_texto)
    chave = GEN(seed_bits)
    print(f"Chave gerada com {len(chave)} bits\n")

    # Passo 2: PREPARAÇÃO DA MENSAGEM ORIGINAL
    print("[Passo 2] Conversão e Padronização da Mensagem")
    print("-" * 60)
    msg_texto = "Testando a difusao do algoritmo"
    msg_bits_original = texto_para_binario(msg_texto)
    msg_bits_original = ajustar_tamanho_msg(msg_bits_original, len(chave))
    print(f"Mensagem original: '{msg_texto}'")
    print(f"Tamanho padronizado: {len(msg_bits_original)} bits\n")

    # Passo 3: ENCRIPTAÇÃO DA MENSAGEM ORIGINAL
    print("[Passo 3] Encriptação da Mensagem Base")
    print("-" * 60)
    cifra_original = ENC(chave, msg_bits_original)
    print(f"Cifra original gerada\n")

    # Passo 4: CONFIGURAÇÃO DO TESTE DE DIFUSÃO
    print("[Passo 4] Configuração do Teste de Difusão")
    print("-" * 60)
    total_bits = len(msg_bits_original)
    soma_diferencas = 0
    bits_testados = 0
    limite_teste = min(50, total_bits)
    print(f"Serão testados {limite_teste} bits da mensagem")
    print("Para cada bit: alteramo-lo, encriptamos e comparamos com a cifra original\n")

    # Passo 5: LOOP DE TESTE - ANÁLISE DE SENSIBILIDADE BIT A BIT
    print("[Passo 5] Teste de Sensibilidade Bit a Bit")
    print("-" * 60)
    print(f"{'Bit Alterado':<15} | {'Bits Mudados':<15} | {'% Difusão':<12}")
    print("-" * 60)

    for i in range(limite_teste):
        # Criamos uma cópia e invertemos o bit na posição i
        msg_alterada = copy.deepcopy(msg_bits_original)
        msg_alterada[i] = 1 - msg_alterada[i]

        # Encriptamos a mensagem modificada com a mesma chave
        cifra_nova = ENC(chave, msg_alterada)

        # Contamos as diferenças entre as duas cifras (Distância de Hamming)
        diff = contar_bits_diferentes(cifra_original, cifra_nova)
        soma_diferencas += diff
        bits_testados += 1

        porcentagem = (diff / total_bits) * 100
        print(f"Posição {i:<8} | {diff:<15} | {porcentagem:>10.2f}%")

    # Passo 6: ANÁLISE DOS RESULTADOS
    print("-" * 60)
    media_difusao = soma_diferencas / bits_testados
    print(f"\n[Passo 6]: Análise dos Resultados")
    print("-" * 60)
    print(f"Média de bits alterados por teste: {media_difusao:.2f} bits")
    print(f"Taxa de Difusão Média: {(media_difusao / total_bits) * 100:.2f}%")
    print(
        "\nINTERPRETAÇÃO: Uma taxa de difusão próxima a 50% indica uma boa distribuição"
    )
    print("de alterações, garantindo segurança contra ataques diferenciais e análises")
    print("de padrões. Cifras com baixa difusão são vulneráveis a criptoanálise.\n")
    print("\n" + "=" * 60 + "\n")


if __name__ == "__main__":
    run()
