import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.gen import GEN
from src.enc import ENC


def run():
    print("\n>>> [2/4] Executando Teste de Colisões (Chaves Equivalentes)...")

    # Número de chaves aleatórias a testar
    n_chaves = 50000
    tamanho_padrao = 16

    # Mensagem fixa que será usada para todos os testes de encriptação
    msg_fixa = "TesteColisaoTFT"

    print(f"   Testando {n_chaves} chaves aleatórias contra mensagem fixa...")

    # Dicionário para armazenar cifras já encontradas e sua seed de origem
    mapa_cifras = {}
    colisoes = 0

    # Valores fixos para champ e stars, para isolar apenas o teste da seed
    champ_fixo = 1
    stars_fixo = 2

    # Itera sobre todas as sementes de teste
    for i in range(n_chaves):
        # Gera uma seed padronizada com zeros à esquerda
        current_seed = str(i).zfill(tamanho_padrao)

        # Gera a chave criptográfica usando a seed e os parâmetros fixos
        K = GEN(current_seed, champ_fixo, stars_fixo)[0]

        # Encripta a mensagem fixa com a chave gerada
        C = ENC(K, msg_fixa)

        # Converte o resultado para tupla para permitir usar como chave do dicionário
        C_tuple = tuple(C)

        # Verifica se a cifra já foi encontrada anteriormente
        if C_tuple in mapa_cifras:
            colisoes += 1
            # Exibe apenas as primeiras 5 colisões encontradas
            if colisoes < 5:
                print(
                    f"   [COLISÃO] Seed '{current_seed}' colidiu com '{mapa_cifras[C_tuple]}'"
                )
        else:
            # Armazena a cifra e sua seed original
            mapa_cifras[C_tuple] = current_seed

    # Exibe o resultado final do teste
    print(f"\n   Colisões encontradas: {colisoes}")

    if colisoes == 0:
        print("   → Resultado: APROVADO ✓")
    else:
        print(f"   → Resultado: REPROVADO ✗ ({colisoes} colisões)")
    print("\n" + "=" * 60 + "\n")


if __name__ == "__main__":
    run()
