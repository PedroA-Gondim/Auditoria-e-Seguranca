import random
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.gen import GEN
from src.enc import ENC


def run():
    """
    Teste de Colisões - Análise de Segurança de Chaves Equivalentes

    Conceito: Este teste verifica se diferentes chaves geram as mesmas cifras
    para uma mesma mensagem. Uma quantidade alta de colisões indicaria falhas
    graves na geração de chaves ou no algoritmo de encriptação.
    """
    print("\n>>> [2/4] Executando Teste de Colisões (Chaves Equivalentes)...")

    # ETAPA 1: Configuração dos parâmetros de teste
    n_chaves = 200000
    tamanho_padrao = 16  # bits - Tamanho fixo para garantir consistência nas seeds
    seed_base = "a" * tamanho_padrao

    # ETAPA 2: Preparação da mensagem fixa
    # Em um esquema seguro, diferentes chaves devem produzir diferentes cifras
    # para a mesma mensagem (propriedade de injetividade da função ENC)
    K_temp = GEN(seed_base)
    M = [random.randint(0, 1) for _ in range(len(K_temp))]

    print(f"   Testando {n_chaves} chaves aleatórias contra mensagem fixa...")

    # ETAPA 3: Teste de colisões
    # Mapa para rastrear cifras já encontradas: { Cifra : Seed_Geradora }
    mapa_cifras = {}
    colisoes = 0

    for i in range(n_chaves):
        # Gera seed sequencial com padding zero (ex: "0000000000000001")
        # Isso mantém o tamanho consistente, pois GEN depende de len(seed)
        current_seed = str(i).zfill(tamanho_padrao)

        # Gera chave a partir da seed
        K = GEN(current_seed)

        # Encripta a mensagem com a chave
        C = ENC(K, M)

        # Converte para tupla (tipo hashable) para usar como chave de dicionário
        C_tuple = tuple(C)

        # ETAPA 4: Análise de colisões
        if C_tuple in mapa_cifras:
            colisoes += 1
            # Exibe primeiras colisões para investigação
            if colisoes < 5:
                print(
                    f"   [COLISÃO DETECTADA] Seed '{current_seed}' e '{mapa_cifras[C_tuple]}' geram a mesma cifra!"
                )
        else:
            mapa_cifras[C_tuple] = current_seed

    # ETAPA 5: Relatório de resultados
    print(f"\n   Colisões encontradas: {colisoes}")

    if colisoes == 0:
        print("   → Resultado: APROVADO ✓")
        print("      O espaço de chaves apresenta comportamento seguro.")
    else:
        print(f"   → Resultado: REPROVADO ✗")
        print(f"      {colisoes} chaves equivalentes detectadas.")
        print("      Recomendação: Aumentar entropia em GEN ou revisar ENC.")
    print("\n" + "=" * 60 + "\n")



if __name__ == "__main__":
    run()
