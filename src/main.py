# src/main.py
import sys
import os

# Adiciona o diretório raiz ao caminho
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


TFT_SBOX = [12, 5, 6, 11, 9, 0, 10, 13, 3, 14, 15, 8, 4, 7, 1, 2]
# Tabela de Substituição (S-Box): mapeia valores de 4 bits (0-15) para outros valores
# Propósito: Confusão - torna a relação entre chave e texto cifrado complexa
# Exemplo: entrada 5 → saída 6 (embaralha os bits de forma não-linear)


TFT_CHAMPIONS = [
    "Bardo",
    "Graves",
    "Orianna",
    "Poppy",
    "Tryndamere",
    "Yorick",
    "Darius",
    "Gwen",
    "Kennen",
    "Kobuko",
    "BaronNashor",
    "LeBlanc",
    "Diana",
    "Fizz",
    "KaiSa",
    "Kalista",
    "Nasus",
    "Nidalee",
    "Renekton",
    "Skarner",
    "Veigar",
    "Warwick",
    "Yone",
    "Aatrox",
    "Galio",
    "Mel",
    "Sett",
    "TahmKench",
    "Thresh",
    "Volibear",
    "Xerath",
    "Ziggs",
    "AurelionSol",
    "Ryze",
    "Sylas",
    "Zaahen",
    "Ashe",
    "Viego",
    "Draven",
    "Arauto",
]


def obter_campeao(input_usuario):
    """
    Converte a entrada do usuário em um índice válido (0 a 39).

    Usa operação módulo para garantir que qualquer número (positivo, negativo, ou maior que 40)
    sempre retorne um índice dentro dos limites da lista.

    Exemplo:
    - input: 41 → índice: 0 (volta ao início)
    - input: -5 → índice: 34 (volta ao final)
    """
    indice_seguro = (input_usuario - 1) % len(TFT_CHAMPIONS)
    return indice_seguro


def obter_estrelas(input_usuario):
    """
    Normaliza a entrada em um nível de estrela válido (1 a 4).

    Transforma qualquer entrada inteira em um valor cíclico entre 1-4.
    Útil para garantir que o entrada sempre seja um nível de estrela válido.

    Exemplo:
    - input: 5 → output: 1 (cicla)
    - input: 10 → output: 2 (cicla)
    """
    indice = (input_usuario - 1) % 4
    return indice + 1


def gerar_bits_tft(champ_id, stars):
    """
    Converte campeão e nível de estrelas em uma sequência de bits.

    Processo:
    1. Nome do campeão → bits (cada caractere tem seu código binário ASCII)
    2. Estrelas → 3 bits (suficiente para 1-4: 001, 010, 011, 100)

    Resultado: sequência de bits que representa uma chave parcial específica
    """
    if not (1 <= champ_id <= len(TFT_CHAMPIONS)):
        raise ValueError("O ID do campeão deve estar entre 1 e 40.")
    if not (1 <= stars <= 4):
        raise ValueError("O nível de estrelas deve estar entre 1 e 4.")

    nome_campeao = TFT_CHAMPIONS[champ_id - 1]
    bits_nome = texto_para_binario(nome_campeao)
    bits_estrelas = [int(b) for b in format(stars, "03b")]

    return bits_nome + bits_estrelas


def combinar_seed(seed_bits_usuario, bits_tft):
    """
    Combina a senha do usuário com os dados do campeão usando XOR.

    Processo:
    1. Se tamanhos diferentes: expande o TFT repetindo-o para igualar tamanho
    2. XOR cada bit: 1⊕1=0, 1⊕0=1, 0⊕1=1, 0⊕0=0

    Efeito: dados do campeão/estrelas modificam a senha sem perder informação
    Resultado: mesma senha + campeão diferente = chave completamente diferente
    """
    len_seed = len(seed_bits_usuario)
    len_tft = len(bits_tft)

    if len_seed == 0:
        return []

    # Expande TFT para ter tamanho ≥ seed
    fator_multiplicacao = (len_seed // len_tft) + 1
    tft_extendido = (bits_tft * fator_multiplicacao)[:len_seed]

    # XOR bit a bit
    seed_combinada = [
        b_seed ^ b_tft for b_seed, b_tft in zip(seed_bits_usuario, tft_extendido)
    ]

    return seed_combinada


def aplicar_sbox(bits):
    """
    Aplica confusão usando a S-Box.

    Processo:
    1. Divide os bits em grupos de 4 (chamados "nibbles")
    2. Converte cada nibble para número (0-15)
    3. Substitui pela tabela TFT_SBOX
    4. Converte de volta para 4 bits

    Propósito: Operação não-linear que embaralha os bits
    → Impossível deduzir a entrada a partir da saída sem conhecer a S-Box

    Exemplo: nibble 0101 (5) → TFT_SBOX[5] = 6 → 0110
    """
    novos_bits = bits[:]
    for i in range(0, len(novos_bits), 4):
        if i + 4 <= len(novos_bits):
            # Converte 4 bits para número (0-15)
            nibble = (
                (novos_bits[i] << 3)
                | (novos_bits[i + 1] << 2)
                | (novos_bits[i + 2] << 1)
                | novos_bits[i + 3]
            )

            # Substitui pela tabela
            substituido = TFT_SBOX[nibble]

            # Converte de volta para 4 bits
            novos_bits[i] = (substituido >> 3) & 1
            novos_bits[i + 1] = (substituido >> 2) & 1
            novos_bits[i + 2] = (substituido >> 1) & 1
            novos_bits[i + 3] = substituido & 1
    return novos_bits


def rotacionar_bits(bits, n):
    """
    Rotaciona (desliza) todos os bits n posições para a esquerda.

    Processo: pega os n primeiros bits e move para o final

    Propósito: Difusão - espalha a influência de cada bit por toda sequência
    → Uma mudança em um bit afeta bits distantes após rotação

    Exemplo: [1,0,1,0] rotacionado 1 → [0,1,0,1]
    """
    n = n % len(bits)
    return bits[n:] + bits[:n]


def GEN(seed_frase:list[int], input_champ=0, input_stars=1):
    """
    Gera a chave final K usando princípios de Confusão e Difusão (como no DES).

    PRINCÍPIOS CRIPTOGRÁFICOS:
    - Confusão: torna a relação entre chave e saída complexa (S-Box)
    - Difusão: espalha o efeito de cada bit para todo o resultado (Rotação + Feedback)

    ETAPAS:
    1. Prepara: converte senha em bits + combina com dados do campeão
    2. Expande: multiplica por 4 para aumentar tamanho (segurança)
    3. 4 Rodadas de processamento:
       a) XOR com constante que muda por rodada e campeão
       b) Aplica S-Box (confusão)
       c) Rotaciona (difusão)
       d) Feedback com bit vizinho (difusão adicional)

    Resultado: chave de 128+ bits bem misturada e segura
    """
    champ_index = obter_campeao(input_champ)
    stars_val = obter_estrelas(input_stars)
    nome_champ = TFT_CHAMPIONS[champ_index]

    # ETAPA 1: Prepara a seed inicial
    seed_bits = seed_frase
    tft_bits = gerar_bits_tft(champ_index + 1, stars_val)
    seed_final = combinar_seed(seed_bits, tft_bits)

    if not seed_final:
        return [], nome_champ, stars_val

    # ETAPA 2: Expande a seed
    # Aumenta 4x o tamanho para ter mais bits na chave final
    tamanho_chave = 4 * len(seed_bits)

    estado = []
    while len(estado) < tamanho_chave:
        estado.extend(seed_final)
    estado = estado[:tamanho_chave]

    # ETAPA 3: Rodadas de processamento (2 rodadas)
    numero_rodadas = 2

    for round_num in range(numero_rodadas):
        # PASSO A: Mistura com constante que varia a cada rodada
        # Constante depende do campeão e estrelas → campeão diferente = chave diferente
        constante_round = (champ_index * (round_num + 1) + stars_val) % 255
        bits_constante = [int(b) for b in format(constante_round, "08b")]

        for i in range(len(estado)):
            estado[i] ^= bits_constante[i % 8]

        # PASSO B: CONFUSÃO - S-Box embaralha os bits
        estado = aplicar_sbox(estado)

        # PASSO C: DIFUSÃO - Rotação espalha a influência dos bits
        # Rotação diferente a cada rodada para evitar padrões
        rotacao = stars_val * 7 + round_num * 11
        estado = rotacionar_bits(estado, rotacao)

        # PASSO D: DIFUSÃO ADICIONAL - Feedback com bits vizinhos
        # Cada bit é XORado com o anterior, criando dependência entre bits
        novo_estado = estado[:]
        for i in range(len(estado)):
            novo_estado[i] ^= estado[(i - 1) % len(estado)]
        estado = novo_estado

    K = estado
    return K, nome_champ, stars_val

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


def ENC(K: list[int],M: list[int]  ) -> list[int]:
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
    #M = texto_para_binario(mensagem_texto)

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

    # src/utils.py


def texto_para_binario(texto: str) -> list[int]:

    """Converte string para lista de bits (ASCII 8 bits)."""

    bits = []

    for char in texto:

        # Converte para binário, remove o '0b' e preenche com zeros à esquerda

        bin_val = bin(ord(char))[2:].zfill(8)

        bits.extend([int(b) for b in bin_val])

    return bits





def binario_para_texto(bits: list[int]) -> str:

    """Converte lista de bits para string."""

    chars = []

    for i in range(0, len(bits), 8):

        byte = bits[i : i + 8]

        # Se sobrar bits quebrados no final (menos de 8), ignora

        if len(byte) < 8:

            break

        str_val = "".join(str(b) for b in byte)

        chars.append(chr(int(str_val, 2)))

    return "".join(chars)





def xor_listas(lista_a: list[int], lista_b: list[int]) -> list[int]:

    """Aplica XOR bit a bit."""

    # O zip corta no tamanho da menor lista, então garantimos tamanhos iguais antes

    return [a ^ b for a, b in zip(lista_a, lista_b)]





def ajustar_tamanho_msg(msg: list[int], tamanho_alvo: int) -> list[int]:

    """

    Ajusta a mensagem para ter EXATAMENTE o tamanho da chave (tamanho_alvo).

    - Se for menor: Preenche com zeros (padding).

    - Se for maior: Corta (truncamento) - para simplificação do trabalho.

    """

    tamanho_atual = len(msg)



    if tamanho_atual == tamanho_alvo:

        return msg



    if tamanho_atual < tamanho_alvo:

        # Adiciona zeros ao final

        padding = [0] * (tamanho_alvo - tamanho_atual)

        return msg + padding

    else:

        # Corta o excesso

        return msg[:tamanho_alvo]



