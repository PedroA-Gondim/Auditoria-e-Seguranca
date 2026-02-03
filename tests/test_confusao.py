import sys
import os

# Adiciona o caminho do diretório pai ao sistema para permitir importações
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.gen import GEN
from src.enc import ENC
# Removemos ajustar_tamanho_msg e texto_para_binario da importação direta pois ENC cuida disso


def contar_bits_diferentes(lista1, lista2):
    # Conta o número de bits diferentes entre duas listas de bits
    return sum(1 for b1, b2 in zip(lista1, lista2) if b1 != b2)


def run():
    print("\n>>> [4/4] Executando Teste de Confusão (Refatorado)\n")
    print(
        "Objetivo: Verificar se mudanças mínimas nos inputs (Seed, Campeão, Estrelas)"
    )
    print("          geram cifras totalmente diferentes.\n")

    msg_texto = "MensagemFixaParaConfusao"

    # Parâmetros Base para a geração da cifra
    seed_base = "segredoTFT"  # Semente inicial
    champ_base = 5  # Campeão inicial
    stars_base = 2  # Nível de estrelas inicial

    # Gera a cifra base usando os parâmetros iniciais
    K_base = GEN(seed_base, champ_base, stars_base)[0]
    cifra_base = ENC(K_base, msg_texto)
    total_bits = len(cifra_base)

    print(
        f"Cifra Base gerada com: Seed='{seed_base}', Champ={champ_base}, Stars={stars_base}"
    )
    print(f"Tamanho da Cifra: {total_bits} bits")
    print("-" * 60)

    # --- TESTE 1: Mudança na Seed (String) ---
    print("\n[Teste 1] Alterando 1 caractere da Seed")
    seed_alt = "segredoTFU"  # Mudou T -> U (1 bit de diferença no ASCII)
    K_alt = GEN(seed_alt, champ_base, stars_base)[0]
    cifra_alt = ENC(K_alt, msg_texto)

    # Calcula a diferença em bits entre a cifra base e a cifra alterada
    diff = contar_bits_diferentes(cifra_base, cifra_alt)
    perc = (diff / total_bits) * 100
    print(f"Seed: '{seed_base}' -> '{seed_alt}'")
    print(f"Diferença: {diff} bits ({perc:.2f}%)")

    # --- TESTE 2: Mudança no Campeão ---
    print("\n[Teste 2] Alterando Campeão (Input + 1)")
    champ_alt = champ_base + 1  # Aumenta o campeão em 1
    K_alt2 = GEN(seed_base, champ_alt, stars_base)[0]
    cifra_alt2 = ENC(K_alt2, msg_texto)

    # Calcula a diferença em bits
    diff2 = contar_bits_diferentes(cifra_base, cifra_alt2)
    perc2 = (diff2 / total_bits) * 100
    print(f"Champ: {champ_base} -> {champ_alt}")
    print(f"Diferença: {diff2} bits ({perc2:.2f}%)")

    # --- TESTE 3: Mudança nas Estrelas ---
    print("\n[Teste 3] Alterando Nível de Estrelas")
    stars_alt = stars_base + 1  # Aumenta o nível de estrelas em 1
    K_alt3 = GEN(seed_base, champ_base, stars_alt)[0]
    cifra_alt3 = ENC(K_alt3, msg_texto)

    # Calcula a diferença em bits
    diff3 = contar_bits_diferentes(cifra_base, cifra_alt3)
    perc3 = (diff3 / total_bits) * 100
    print(f"Stars: {stars_base} -> {stars_alt}")
    print(f"Diferença: {diff3} bits ({perc3:.2f}%)")

    # Avaliação Geral da média de confusão
    media_confusao = (perc + perc2 + perc3) / 3
    print("\n" + "-" * 60)
    print(f"Média de Confusão Global: {media_confusao:.2f}%")

    print("=" * 60 + "\n")


if __name__ == "__main__":
    run()
