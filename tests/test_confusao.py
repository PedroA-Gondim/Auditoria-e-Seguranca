# tests/test_confusao.py
import sys
import os
import copy

# Adiciona o diretório pai ao caminho para importar módulos do projeto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

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


def run():
    """
    TESTE DE CONFUSÃO -

    CONCEITO:
    A confusão é uma propriedade criptográfica fundamental que garante que
    pequenas alterações na chave (seed) causem mudanças significativas no texto
    cifrado. Isso dificulta ataques que tentam estabelecer relações entre a chave
    e o criptograma.

    METODOLOGIA:
    1. Fixa uma mensagem constante
    2. Altera 1 bit por vez na seed (chave)
    3. Compara o criptograma resultante com o criptograma original
    4. Calcula a taxa de bits alterados no criptograma
    5. Interpreta se a taxa indica boa confusão (idealmente > 50%)
    """
    print("\n>>> [4/4] Executando Teste de Confusão\n")
    print("Objetivo: Validar se alterações na chave geram criptogramas")
    print("          significativamente diferentes, mantendo a mensagem fixa.\n")

    # ========== Passo 1: PREPARAÇÃO DA MENSAGEM (FIXA) ==========
    print("[Passo 1] Preparação da Mensagem de Teste")
    print("-" * 60)
    msg_texto = "Mensagem fixa para teste de confusao"
    msg_bits = texto_para_binario(msg_texto)
    print(f"Mensagem: '{msg_texto}'")
    print(f"Convertida para: {len(msg_bits)} bits binários")

    # ========== Passo 2: PREPARAÇÃO DA SEED ORIGINAL ==========
    print("[Passo 2] Preparação da Seed")
    print("-" * 60)
    seed_texto = "segredo"
    seed_bits_original = texto_para_binario(seed_texto)
    print(f"Seed Original: '{seed_texto}'")
    print(f"Convertida para: {len(seed_bits_original)} bits binários\n")

    # ========== Passo 3: CRIPTOGRAFIA COM SEED ORIGINAL ==========
    print("[Passo 3] Geração da Chave e Criptografia Inicial")
    print("-" * 60)
    chave1 = GEN(seed_bits_original)
    msg_bits_ajustada = ajustar_tamanho_msg(msg_bits, len(chave1))
    cifra1 = ENC(chave1, msg_bits_ajustada)
    print(f"Chave derivada: {len(chave1)} bits")
    print(f"Cifra inicial: {len(cifra1)} bits")
    print("Status: Este será a cifra de referência\n")

    # ========== Passo 4: CONFIGURAÇÃO DOS TESTES ITERATIVOS ==========
    print("[Passo 4] Configuração dos Testes")
    print("-" * 60)
    total_bits_cifra = len(cifra1)
    soma_diferencas = 0
    bits_testados = 0
    limite_teste = min(50, len(seed_bits_original))

    print(f"Limites de teste: primeiros {limite_teste} bits da seed")
    print(f"Métrica: Contar bits diferentes no criptograma\n")

    # ========== Passo 5: BATERIA DE TESTES (CONFUSÃO) ==========
    print("[Passo 5] Execução dos Testes de Confusão")
    print("-" * 60)
    print(f"{'Posição Bit':<15} | {'Bits Alterados':<20} | {'Taxa (%)':<10}")
    print("-" * 60)

    for i in range(limite_teste):
        # Duplica a seed original
        seed_alterada = copy.deepcopy(seed_bits_original)

        # Inverte exatamente 1 bit (simula erro ou ataque de 1 bit)
        seed_alterada[i] = 1 - seed_alterada[i]

        # Regenera chave com seed alterada
        chave2 = GEN(seed_alterada)

        # Criptografa a MESMA mensagem com a NOVA chave
        # (Isolando o efeito da alteração da chave)
        cifra2 = ENC(chave2, msg_bits_ajustada)

        # Calcula o impacto: quantos bits mudaram no criptograma
        diff = contar_bits_diferentes(cifra1, cifra2)
        soma_diferencas += diff
        bits_testados += 1

        porcentagem = (diff / total_bits_cifra) * 100
        print(f"{i:<15} | {diff:<20} | {porcentagem:>8.2f}%")

    # ========== Passo 6: ANÁLISE ESTATÍSTICA DOS RESULTADOS ==========
    print("-" * 60)
    print("\n[Passo 6] Análise Estatística dos Resultados")
    print("-" * 60)

    media_confusao = soma_diferencas / bits_testados
    taxa_confusao_percentual = (media_confusao / total_bits_cifra) * 100

    print(f"Testes realizados: {bits_testados}")
    print(f"Média de bits alterados: {media_confusao:.2f} bits por teste")
    print(f"Taxa de Confusão Média: {taxa_confusao_percentual:.2f}%")
    print(f"Total de bits no criptograma: {total_bits_cifra}")

    # ========== Passo 7: INTERPRETAÇÃO E CONCLUSÃO ==========
    print("\n[Passo 7] Interpretação e Conclusão")
    print("-" * 60)
    print("CRITÉRIO DE AVALIAÇÃO (Ideal para boa confusão: > 50%)")
    print()

    if 45 <= taxa_confusao_percentual <= 55:
        print(
            f"[APROVADO] EXCELENTE! Taxa de {taxa_confusao_percentual:.2f}% está próxima do ideal (50%)."
        )
        print(
            "Interpretação: O algoritmo demonstra uma independência estatística quase perfeita"
        )
        print("               entre a chave e o criptograma.")
    elif 25 <= taxa_confusao_percentual < 45 or 55 < taxa_confusao_percentual <= 75:
        print("[ACEITÁVEL] Confusão satisfatória.")
        print(
            "Interpretação: Existe uma dispersão significativa, mas com ligeiro desvio estatístico."
        )
    else:
        print("[REPROVADO] Confusão insuficiente ou comportamento linear.")
        print(
            "Interpretação: A relação chave-cifra é muito previsível ou não altera bits suficientes."
        )
    print("\n" + "=" * 60 + "\n")


if __name__ == "__main__":
    run()
