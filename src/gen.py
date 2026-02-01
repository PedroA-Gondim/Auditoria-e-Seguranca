from src.utils import texto_para_binario

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


def GEN(seed_frase, input_champ, input_stars):
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
    seed_bits = texto_para_binario(seed_frase)
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

    # ETAPA 3: Rodadas de processamento (4 rodadas)
    numero_rodadas = 4

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
