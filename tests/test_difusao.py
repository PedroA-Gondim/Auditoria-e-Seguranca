import sys
import os

# Adiciona o caminho do diretório pai ao sistema para importar módulos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.gen import GEN
from src.enc import ENC


# Função para contar quantos bits são diferentes entre duas listas de bits
def contar_bits_diferentes(lista1, lista2):
    return sum(1 for b1, b2 in zip(lista1, lista2) if b1 != b2)


def run():
    print("\n>>> [3/4] Executando Teste de Difusão (Avalanche na Mensagem)\n")

    # Passo 1: Geração da Chave
    seed = "chaveMestraDifusao"  # Semente para gerar a chave
    K = GEN(seed, 10, 3)[
        0
    ]  # Gera a chave usando a semente, com 10 como champ e 3 estrelas

    # Passo 2: Mensagem Base
    msg_base = "TesteDeDifusaoTFT123"  # Mensagem original a ser cifrada
    cifra_base = ENC(K, msg_base)  # Cifra a mensagem base usando a chave gerada
    total_bits = len(cifra_base)  # Total de bits na cifra resultante

    print(f"Mensagem Base: '{msg_base}'")
    print(f"Total bits cifra: {total_bits}")
    print("-" * 60)
    print(f"{'Alteração':<20} | {'Bits Mudados':<15} | {'% Difusão':<12}")
    print("-" * 60)

    soma_diff = 0  # Acumulador para a soma de bits alterados
    testes = 0  # Contador de testes realizados

    # Testamos mudando cada caractere da mensagem
    lista_chars = list(msg_base)  # Converte a mensagem em uma lista de caracteres

    for i in range(len(lista_chars)):
        # Cria uma cópia da lista de caracteres e altera o caractere na posição i
        chars_temp = lista_chars[:]

        # Altera o caractere: 'A' se torna 'B', etc.
        char_original = chars_temp[i]
        chars_temp[i] = chr(
            ord(char_original) + 1
        )  # Incrementa o valor ASCII do caractere

        msg_alterada = "".join(
            chars_temp
        )  # Junta os caracteres alterados em uma nova mensagem

        cifra_nova = ENC(K, msg_alterada)  # Cifra a nova mensagem alterada

        # Conta a diferença de bits entre a cifra original e a nova cifra
        diff = contar_bits_diferentes(cifra_base, cifra_nova)
        perc = (diff / total_bits) * 100  # Calcula a porcentagem de bits alterados

        soma_diff += diff  # Acumula a soma de bits alterados
        testes += 1  # Incrementa o contador de testes

        desc_alt = (
            f"Char[{i}] '{char_original}'->'{chars_temp[i]}'"  # Descrição da alteração
        )
        print(
            f"{desc_alt:<20} | {diff:<15} | {perc:>9.2f}%"
        )  # Exibe os resultados da alteração

    # Análise dos resultados
    print("-" * 60)
    media = soma_diff / testes  # Calcula a média de bits alterados
    perc_media = (media / total_bits) * 100  # Calcula a taxa média de difusão

    print(f"Média de bits alterados: {media:.2f}")
    print(f"Taxa de Difusão Média: {perc_media:.2f}%")

    # Interpretação dos resultados
    if 40 < perc_media < 60:
        print("\nINTERPRETAÇÃO: EXCELENTE. O efeito avalanche está próximo de 50%.")
    else:
        print("\nINTERPRETAÇÃO: ATENÇÃO. Valores longe de 50% indicam viés.")

    print("\n" + "=" * 60 + "\n")


if __name__ == "__main__":
    run()
