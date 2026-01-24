"""
Teste de Velocidade de Execução - Criptografia Simétrica
Disciplina: GSI035 - Auditoria e Segurança da Informação

Objetivo: Avaliar o desempenho (throughput) dos algoritmos de
criptografia e descriptografia através de múltiplas iterações.
"""

import time
import random
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.gen import GEN  # Gerador de chave de sessão
from src.enc import ENC  # Algoritmo de criptografia
from src.dec import DEC  # Algoritmo de descriptografia


def run():
    print("\n>>> [1/4] Executando Teste de Velocidade de Execução...")

    # PASSO 1: Configuração dos parâmetros
    n_repeticoes = 10000
    seed = "BenchmarkSeed"

    print("\n   [Passo 1] Preparação dos dados")
    print(f"   - Seed: {seed}")
    print(f"   - Iterações: {n_repeticoes}")

    # PASSO 2: Geração da chave de sessão
    # Conceito: A chave K é derivada do seed através de GEN (Key Derivation Function)
    K = GEN(seed)

    # PASSO 3: Geração de mensagem aleatória
    # Conceito: A mensagem M é um vetor binário com tamanho compatível com a chave
    M = [random.randint(0, 1) for _ in range(len(K))]
    print(f"   - Tamanho da chave: {len(K)} bits")
    print(f"   - Tamanho da mensagem: {len(M)} bits")

    # PASSO 4: Medição do tempo de criptografia (ENC)
    # Conceito: Mede o tempo de processamento para encriptar múltiplas vezes
    # sem I/O para evitar distorção dos resultados
    print("\n   [Passo 2] Medindo tempo de criptografia (ENC)...")
    inicio_enc = time.perf_counter()
    for _ in range(n_repeticoes):
        C = ENC(K, M)
    fim_enc = time.perf_counter()

    # PASSO 5: Medição do tempo de descriptografia (DEC)
    # Conceito: Usa o criptograma C da última iteração para medir DEC
    # Garante que o texto cifrado é válido e consistente
    print("   [Passo 3] Medindo tempo de descriptografia (DEC)...")
    inicio_dec = time.perf_counter()
    for _ in range(n_repeticoes):
        _ = DEC(K, C)
    fim_dec = time.perf_counter()

    # PASSO 6: Cálculo das médias
    media_enc = (fim_enc - inicio_enc) / n_repeticoes
    media_dec = (fim_dec - inicio_dec) / n_repeticoes

    # PASSO 7: Apresentação dos resultados
    print("\n   [Passo 4] Resultados do Benchmark")
    print(f"   Tempo Médio ENC: {media_enc * 1000:.6f} ms")
    print(f"   Tempo Médio DEC: {media_dec * 1000:.6f} ms")
    print(f"   Tempo Total: {(media_enc + media_dec) * 1000:.6f} ms")

    # PASSO 8: Avaliação qualitativa
    # Conceito: Define critérios de desempenho para criptografia prática
    if media_enc < 0.01:
        classificacao = "EXCELENTE"
    elif media_enc < 0.05:
        classificacao = "BOM"
    else:
        classificacao = "ACEITÁVEL"

    print(f"   -> Classificação: Desempenho {classificacao}.")
    print("\n" + "=" * 60 + "\n")



if __name__ == "__main__":
    run()
