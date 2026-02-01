from src.utils import xor_listas, binario_para_texto

# Tabela S-Box inversa para recuperar valores originais durante a descriptografia
INV_SBOX = [5, 14, 15, 8, 12, 1, 2, 13, 11, 4, 6, 3, 0, 7, 9, 10]


def aplicar_sbox_inversa(bits):
    """
    Aplica a S-Box inversa para reverter a substituição de bits.

    Processa 4 bits (1 nibble) por vez:
    - Converte os 4 bits em um índice de 0 a 15
    - Busca o valor original na tabela INV_SBOX
    - Decompõe o valor recuperado de volta em 4 bits

    Args:
        bits: Lista de bits a serem processados

    Returns:
        Lista de bits após reverter a substituição
    """
    novos_bits = bits[:]

    # Processa cada grupo de 4 bits (nibble)
    for i in range(0, len(novos_bits), 4):
        if i + 4 <= len(novos_bits):
            # PASSO 1: Converter 4 bits em um índice (0-15)
            # Exemplo: [1,0,1,1] → 1*8 + 0*4 + 1*2 + 1*1 = 11
            nibble = (
                (novos_bits[i] << 3)
                | (novos_bits[i + 1] << 2)
                | (novos_bits[i + 2] << 1)
                | novos_bits[i + 3]
            )

            # PASSO 2: Buscar o valor original na tabela de substituição inversa
            recuperado = INV_SBOX[nibble]

            # PASSO 3: Decompor o valor recuperado de volta em 4 bits
            # Exemplo: 11 → [1,0,1,1]
            novos_bits[i] = (recuperado >> 3) & 1  # Bit mais significativo
            novos_bits[i + 1] = (recuperado >> 2) & 1
            novos_bits[i + 2] = (recuperado >> 1) & 1
            novos_bits[i + 3] = recuperado & 1  # Bit menos significativo

    return novos_bits


def reverter_transposicao(bits, num_colunas=4):
    """
    Reverte a transposição de bits que foi aplicada na criptografia.

    A transposição original reordena os bits lendo coluna por coluna.
    Para reverter, lemos coluna por coluna novamente para recuperar
    a ordem original dos bits.

    Args:
        bits: Lista de bits transpostos
        num_colunas: Número de colunas da matriz de transposição (padrão: 4)

    Returns:
        Lista de bits na ordem original (antes da transposição)
    """
    tamanho = len(bits)
    num_linhas = (tamanho + num_colunas - 1) // num_colunas
    saida = [0] * tamanho
    contador = 0

    # PROCESSO: Reconstroem a matriz original lendo coluna por coluna
    # Exemplo com 16 bits e 4 colunas:
    #   Lemos: bits[0,4,8,12], depois [1,5,9,13], etc.
    #   E reconstruímos a ordem original: [0,1,2,3,4,5,...]
    for c in range(num_colunas):
        for linha in range(num_linhas):
            idx_original = linha * num_colunas + c
            if idx_original < tamanho:
                saida[idx_original] = bits[contador]
                contador += 1

    return saida


def DEC(K: list[int], C: list[int]) -> str:
    """
    Descriptografa um texto criptografado usando o algoritmo de Feistel.

    O processo inverte todas as etapas da criptografia em ordem reversa:

    Ordem de descriptografia (reversa):
    1. Remover whitening (XOR com chave)
    2. Aplicar S-Box inversa
    3. Reverter difusão para trás (XOR regressivo)
    4. Reverter difusão para frente (XOR progressivo)
    5. Reverter transposição de bits

    Args:
        K: Chave de criptografia (lista de bits)
        C: Criptograma a descriptografar (lista de bits)

    Returns:
        Texto descriptografado como string
    """
    estado = C[:]
    NUM_RODADAS = 2

    # Executa 2 rodadas de descriptografia (mesmo número da criptografia)
    for rodada in range(NUM_RODADAS):
        # ETAPA 4: Reverter a transposição de bits
        # Retorna os bits para sua posição original
        estado = reverter_transposicao(estado, num_colunas=4)

        # ETAPA 3: Reverter a difusão progressiva (XOR da esquerda para direita)
        # Reverte o padrão: M[i] = M[i] XOR M[i+1]
        for i in range(len(estado) - 1):
            estado[i] ^= estado[i + 1]

        # ETAPA 2: Reverter a difusão regressiva (XOR da direita para esquerda)
        # Reverte o padrão: M[i] = M[i] XOR M[i-1]
        for i in range(len(estado) - 1, 0, -1):
            estado[i] ^= estado[i - 1]

        # ETAPA 1: Reverter a substituição de bits com S-Box inversa
        estado = aplicar_sbox_inversa(estado)

    # ETAPA FINAL: Remover o whitening aplicando XOR novamente com a chave original
    # (XOR é reversível: A XOR B XOR B = A)
    texto_bits = xor_listas(estado, K)

    # Converter bits para texto legível e remover caracteres nulos
    return binario_para_texto(texto_bits).strip("\x00")
