from src.utils import xor_listas, texto_para_binario, ajustar_tamanho_msg

# Tabela de Substituição (S-Box) para a etapa de confusão
# Cada entrada de 4 bits (0-15) é substituída pelo valor correspondente
TFT_SBOX = [12, 5, 6, 11, 9, 0, 10, 13, 3, 14, 15, 8, 4, 7, 1, 2]


def aplicar_sbox(bits):
    """
    ETAPA DE CONFUSÃO: Substitui grupos de 4 bits (nibbles) usando a S-Box.
    Isso garante não-linearidade e dificulta ataques criptanalíticos.

    Processo:
    1. Pega 4 bits consecutivos e converte para um número (0-15)
    2. Substitui esse número pelo valor na tabela TFT_SBOX
    3. Converte o resultado de volta para 4 bits
    """
    novos_bits = bits[:]

    # Processa a lista em grupos de 4 bits
    for i in range(0, len(novos_bits), 4):
        if i + 4 <= len(novos_bits):
            # Converte 4 bits para um número decimal (0-15)
            nibble = (
                (novos_bits[i] << 3)
                | (novos_bits[i + 1] << 2)
                | (novos_bits[i + 2] << 1)
                | novos_bits[i + 3]
            )

            # Busca o substituto na S-Box
            substituido = TFT_SBOX[nibble]

            # Converte o resultado de volta para 4 bits
            novos_bits[i] = (substituido >> 3) & 1
            novos_bits[i + 1] = (substituido >> 2) & 1
            novos_bits[i + 2] = (substituido >> 1) & 1
            novos_bits[i + 3] = substituido & 1

    return novos_bits


def transposicao_colunar(bits, num_colunas=4):
    """
    ETAPA DE DIFUSÃO ESPACIAL: Reorganiza os bits lendo por coluna em vez de linha.
    Isso espalha a influência dos bits por toda a estrutura (difusão).

    Exemplo com 16 bits em 4 colunas:
    Entrada: [b0, b1, b2, b3, b4, b5, b6, b7, ...]
    Organiza em matriz 4x4 e lê por coluna
    """
    tamanho = len(bits)
    num_linhas = (tamanho + num_colunas - 1) // num_colunas
    saida = []

    # Lê coluna por coluna da matriz
    for coluna in range(num_colunas):
        for linha in range(num_linhas):
            idx = linha * num_colunas + coluna
            if idx < tamanho:
                saida.append(bits[idx])

    return saida


def ENC(K: list[int], mensagem_texto: str) -> list[int]:
    """
    ENCRIPTAÇÃO SPN FORTALECIDA com 2 Rodadas e Propagação Bidirecional.

    Estrutura:
    - Whitening inicial (XOR com chave)
    - 2 rodadas de: Confusão → Difusão Linear Bidirecional → Difusão Espacial
    - Eliminação de pontos cegos através de propagação ida e volta

    Parâmetros:
    - K: Chave em formato de lista de bits
    - mensagem_texto: Texto a ser encriptado

    Retorna: Lista de bits criptografados
    """
    # Converte o texto em bits
    M = texto_para_binario(mensagem_texto)

    # Ajusta o tamanho da mensagem para corresponder à chave
    M = ajustar_tamanho_msg(M, len(K))

    if len(K) != len(M):
        raise ValueError("Erro de tamanho: A mensagem ajustada deve igualar a chave.")

    # === ETAPA INICIAL: WHITENING ===
    # XOR entre mensagem e chave para misturar dados antes das rodadas
    estado = xor_listas(M, K)

    NUM_RODADAS = 2

    for num_rodada in range(NUM_RODADAS):
        # === ETAPA A: CONFUSÃO (S-Box) ===
        # Substitui grupos de bits para adicionar não-linearidade
        estado = aplicar_sbox(estado)

        # === ETAPA B: DIFUSÃO LINEAR (Ida / Forward) ===
        # Cada bit influencia o próximo (propagação para a direita)
        # Garante que mudanças se espalhem pela estrutura
        for i in range(1, len(estado)):
            estado[i] ^= estado[i - 1]

        # === ETAPA C: DIFUSÃO LINEAR (Volta / Backward) ===
        # Propagação inversa para eliminar pontos cegos
        # Bits do final influenciam o começo, melhorando a difusão
        for i in range(len(estado) - 2, -1, -1):
            estado[i] ^= estado[i + 1]

        # === ETAPA D: DIFUSÃO ESPACIAL (Transposição) ===
        # Reorganiza os bits para uma melhor distribuição
        estado = transposicao_colunar(estado, num_colunas=4)

    return estado
