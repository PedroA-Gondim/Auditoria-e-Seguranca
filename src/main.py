# src/main.py
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


TFT_SBOX = [12, 5, 6, 11, 9, 0, 10, 13, 3, 14, 15, 8, 4, 7, 1, 2]
INV_SBOX = [5, 14, 15, 8, 12, 1, 2, 13, 11, 4, 6, 3, 0, 7, 9, 10]


TFT_CHAMPIONS = [
    "Bardo", "Graves", "Orianna", "Poppy", "Tryndamere", "Yorick",
    "Darius", "Gwen", "Kennen", "Kobuko", "BaronNashor", "LeBlanc",
    "Diana", "Fizz", "KaiSa", "Kalista", "Nasus", "Nidalee",
    "Renekton", "Skarner", "Veigar", "Warwick", "Yone", "Aatrox",
    "Galio", "Mel", "Sett", "TahmKench", "Thresh", "Volibear",
    "Xerath", "Ziggs", "AurelionSol", "Ryze", "Sylas", "Zaahen",
    "Ashe", "Viego", "Draven", "Arauto",
]


def obter_campeao(input_usuario):
    """Converte entrada em índice válido (0-39) usando módulo."""
    indice_seguro = (input_usuario - 1) % len(TFT_CHAMPIONS)
    return indice_seguro


def obter_estrelas(input_usuario):
    """Normaliza entrada em nível de estrela válido (1-4)."""
    indice = (input_usuario - 1) % 4
    return indice + 1


def gerar_bits_tft(champ_id, stars):
    """Converte campeão e estrelas em sequência de bits."""
    if not (1 <= champ_id <= len(TFT_CHAMPIONS)):
        raise ValueError("ID do campeão deve estar entre 1 e 40.")
    if not (1 <= stars <= 4):
        raise ValueError("Nível de estrelas deve estar entre 1 e 4.")

    nome_campeao = TFT_CHAMPIONS[champ_id - 1]
    bits_nome = texto_para_binario(nome_campeao)
    bits_estrelas = [int(b) for b in format(stars, "03b")]

    return bits_nome + bits_estrelas


def combinar_seed(seed_bits_usuario, bits_tft):
    """Combina senha com dados do campeão usando XOR."""
    len_seed = len(seed_bits_usuario)
    len_tft = len(bits_tft)

    if len_seed == 0:
        return []

    fator_multiplicacao = (len_seed // len_tft) + 1
    tft_extendido = (bits_tft * fator_multiplicacao)[:len_seed]

    seed_combinada = [
        b_seed ^ b_tft for b_seed, b_tft in zip(seed_bits_usuario, tft_extendido)
    ]

    return seed_combinada


def aplicar_sbox(bits):
    """Aplica confusão usando S-Box em grupos de 4 bits."""
    novos_bits = bits[:]
    for i in range(0, len(novos_bits), 4):
        if i + 4 <= len(novos_bits):
            nibble = (
                (novos_bits[i] << 3)
                | (novos_bits[i + 1] << 2)
                | (novos_bits[i + 2] << 1)
                | novos_bits[i + 3]
            )

            substituido = TFT_SBOX[nibble]

            novos_bits[i] = (substituido >> 3) & 1
            novos_bits[i + 1] = (substituido >> 2) & 1
            novos_bits[i + 2] = (substituido >> 1) & 1
            novos_bits[i + 3] = substituido & 1
    return novos_bits


def rotacionar_bits(bits, n):
    """Rotaciona bits n posições para a esquerda (difusão)."""
    n = n % len(bits)
    return bits[n:] + bits[:n]


def GEN(seed_frase: list[int], input_champ=0, input_stars=1):
    """Gera chave final K usando confusão e difusão."""
    champ_index = obter_campeao(input_champ)
    stars_val = obter_estrelas(input_stars)
    nome_champ = TFT_CHAMPIONS[champ_index]

    seed_bits = seed_frase
    tft_bits = gerar_bits_tft(champ_index + 1, stars_val)
    seed_final = combinar_seed(seed_bits, tft_bits)

    if not seed_final:
        return [], nome_champ, stars_val

    tamanho_chave = 4 * len(seed_bits)

    estado = []
    while len(estado) < tamanho_chave:
        estado.extend(seed_final)
    estado = estado[:tamanho_chave]

    numero_rodadas = 3

    for round_num in range(numero_rodadas):
        constante_round = (champ_index * (round_num + 1) + stars_val) % 255
        bits_constante = [int(b) for b in format(constante_round, "08b")]

        for i in range(len(estado)):
            estado[i] ^= bits_constante[i % 8]

        estado = aplicar_sbox(estado)

        rotacao = stars_val * 7 + round_num * 11
        estado = rotacionar_bits(estado, rotacao)

        novo_estado = estado[:]
        for i in range(len(estado)):
            novo_estado[i] ^= estado[(i - 1) % len(estado)]
        estado = novo_estado

    K = estado
    return K


def transposicao_colunar(bits, num_colunas=4):
    """Reorganiza bits por transposição colunar."""
    tamanho = len(bits)
    num_linhas = (tamanho + num_colunas - 1) // num_colunas
    saida = []

    for coluna in range(num_colunas):
        for linha in range(num_linhas):
            idx = linha * num_colunas + coluna
            if idx < tamanho:
                saida.append(bits[idx])

    return saida


def ENC(K: list[int], M: list[int]) -> list[int]:
    """Encripta mensagem usando 2 rodadas com difusão bidirecional."""
    M = ajustar_tamanho_msg(M, len(K))

    if len(K) != len(M):
        raise ValueError("Erro de tamanho: mensagem deve igualar chave.")

    estado = xor_listas(M, K)

    NUM_RODADAS = 2

    for _ in range(NUM_RODADAS):
        estado = aplicar_sbox(estado)

        for i in range(1, len(estado)):
            estado[i] ^= estado[i - 1]

        for i in range(len(estado) - 2, -1, -1):
            estado[i] ^= estado[i + 1]

        estado = transposicao_colunar(estado, num_colunas=4)

    return estado


def aplicar_sbox_inversa(bits):
    """Reverte substituição da S-Box."""
    novos_bits = bits[:]

    for i in range(0, len(novos_bits), 4):
        if i + 4 <= len(novos_bits):
            nibble = (
                (novos_bits[i] << 3)
                | (novos_bits[i + 1] << 2)
                | (novos_bits[i + 2] << 1)
                | novos_bits[i + 3]
            )

            recuperado = INV_SBOX[nibble]

            novos_bits[i] = (recuperado >> 3) & 1
            novos_bits[i + 1] = (recuperado >> 2) & 1
            novos_bits[i + 2] = (recuperado >> 1) & 1
            novos_bits[i + 3] = recuperado & 1

    return novos_bits


def reverter_transposicao(bits, num_colunas=4):
    """Reverte transposição colunar."""
    tamanho = len(bits)
    num_linhas = (tamanho + num_colunas - 1) // num_colunas
    saida = [0] * tamanho
    contador = 0

    for c in range(num_colunas):
        for linha in range(num_linhas):
            idx_original = linha * num_colunas + c
            if idx_original < tamanho:
                saida[idx_original] = bits[contador]
                contador += 1

    return saida


def DEC(K: list[int], C: list[int]) -> str:
    """Descriptografa texto criptografado (ordem reversa da criptografia)."""
    estado = C[:]
    NUM_RODADAS = 2

    for _ in range(NUM_RODADAS):
        estado = reverter_transposicao(estado, num_colunas=4)

        for i in range(len(estado) - 1):
            estado[i] ^= estado[i + 1]

        for i in range(len(estado) - 1, 0, -1):
            estado[i] ^= estado[i - 1]

        estado = aplicar_sbox_inversa(estado)

    texto_bits = xor_listas(estado, K)
    return binario_para_texto(texto_bits).strip("\x00")


def texto_para_binario(texto: str) -> list[int]:
    """Converte string para bits (ASCII 8 bits)."""
    bits = []
    for char in texto:
        bin_val = bin(ord(char))[2:].zfill(8)
        bits.extend([int(b) for b in bin_val])
    return bits


def binario_para_texto(bits: list[int]) -> str:
    """Converte bits para string."""
    chars = []
    for i in range(0, len(bits), 8):
        byte = bits[i : i + 8]
        if len(byte) < 8:
            break
        str_val = "".join(str(b) for b in byte)
        chars.append(chr(int(str_val, 2)))
    return "".join(chars)


def xor_listas(lista_a: list[int], lista_b: list[int]) -> list[int]:
    """Aplica XOR bit a bit entre duas listas."""
    return [a ^ b for a, b in zip(lista_a, lista_b)]


def ajustar_tamanho_msg(msg: list[int], tamanho_alvo: int) -> list[int]:
    """Ajusta mensagem para ter exatamente tamanho_alvo bits."""
    tamanho_atual = len(msg)

    if tamanho_atual == tamanho_alvo:
        return msg

    if tamanho_atual < tamanho_alvo:
        padding = [0] * (tamanho_alvo - tamanho_atual)
        return msg + padding
    else:
        return msg[:tamanho_alvo]
