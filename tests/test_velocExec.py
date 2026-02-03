import time
import os
import sys
import string
import random

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.gen import GEN  # Gera a chave criptográfica
from src.enc import ENC  # Criptografa uma mensagem
from src.dec import DEC  # Descriptografa uma mensagem


def gerar_string_aleatoria(tamanho=16):
    """Cria uma string aleatória com letras e números"""
    letras = string.ascii_letters + string.digits
    return "".join(random.choice(letras) for _ in range(tamanho))


def run():
    print("\n>>> [1/4] Executando Teste de Velocidade de Execução...")

    # Configuração do benchmark
    n_repeticoes = 10000
    seed = "BenchmarkSeed"

    # Parâmetros para geração da chave
    input_champ = 1
    input_stars = 2

    print("\n   [Passo 1] Preparação dos dados")
    print(f"   - Seed: {seed}")
    print(f"   - Iterações: {n_repeticoes}")

    # Gera a chave a partir da seed (retorna tupla: K, campeão, estrelas)
    resultado_gen = GEN(seed, input_champ, input_stars)
    K = resultado_gen[0]

    print(
        f"   - Chave gerada (Campeão: {resultado_gen[1]}, Estrelas: {resultado_gen[2]})"
    )
    print(f"   - Tamanho da chave: {len(K)} bits")

    # Cria a mensagem a ser criptografada
    M_str = gerar_string_aleatoria(16)
    print(f"   - Mensagem: '{M_str}'")

    # Mede o tempo de criptografia em múltiplas iterações
    print("\n   [Passo 2] Medindo tempo de criptografia (ENC)...")
    inicio_enc = time.perf_counter()
    for _ in range(n_repeticoes):
        C = ENC(K, M_str)
    fim_enc = time.perf_counter()

    # Mede o tempo de descriptografia em múltiplas iterações
    print("   [Passo 3] Medindo tempo de descriptografia (DEC)...")
    inicio_dec = time.perf_counter()
    for _ in range(n_repeticoes):
        _ = DEC(K, C)
    fim_dec = time.perf_counter()

    # Calcula a média de tempo por operação
    media_enc = (fim_enc - inicio_enc) / n_repeticoes
    media_dec = (fim_dec - inicio_dec) / n_repeticoes

    print("\n   [Passo 4] Resultados do Benchmark")
    print(f"   Tempo Médio ENC: {media_enc * 1000:.6f} ms")
    print(f"   Tempo Médio DEC: {media_dec * 1000:.6f} ms")
    print(f"   Tempo Total: {(media_enc + media_dec) * 1000:.6f} ms")

    print("\n" + "=" * 60 + "\n")


if __name__ == "__main__":
    run()
