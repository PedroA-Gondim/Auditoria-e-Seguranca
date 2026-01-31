import random
from sr.utils import binario_para_int

# Lista de 40 Campeões (Exemplo baseada em Sets recentes/mistos para ilustrar)
TFT_CHAMPIONS = [
    "Aatrox", "Ahri", "Akali", "Amumu", "Annie", "Aphelios", "Ashe", "Bard",
    "Blitzcrank", "Caitlyn", "Camille", "Corki", "Darius", "Diana", "Draven", "Ekko",
    "Ezreal", "Fiora", "Galio", "Garen", "Gnar", "Gragas", "Graves", "Hecarim",
    "Illaoi", "Irelia", "Janna", "JarvanIV", "Jax", "Jayce", "Jhin", "Jinx",
    "Kaisa", "Kalista", "Karma", "Karthus", "Kassadin", "Katarina", "Kayle", "Kayn"
]


def obter_campeao_seguro(input_usuario):
    """
    Recebe qualquer número inteiro e o mapeia para um índice válido
    de campeão (0 a 39) de forma determinística.
    """
    # Se o usuário digitar 40, (40-1) % 40 = 39 (último da lista).
    # Se digitar 1, (1-1) % 40 = 0 (primeiro da lista).
    # O abs() garante que números negativos também funcionem.
    indice_seguro = abs(input_usuario - 1) % len(TFT_CHAMPIONS)
    return indice_seguro

def obter_estrelas_seguro(input_usuario):
    """
    Mapeia qualquer entrada para 1, 2, 3 ou 4.
    """
    # Mapeia para 0, 1, 2, 3
    indice = abs(input_usuario - 1) % 4
    # Retorna o valor ajustado (1 a 4)
    return indice + 1

def gerar_bits_tft(champ_id, stars):
    """
    Converte o campeão e estrelas em bits.
    champ_id: 1 a 40
    stars: 1 a 4
    """
    # Validação simples
    if not (1 <= champ_id <= 40):
        raise ValueError("O ID do campeão deve ser entre 1 e 40.")
    if not (1 <= stars <= 4):
        raise ValueError("O nível de estrela deve ser entre 1 e 4.")

    # 1. Pegar o nome do campeão (ajustando índice 0-39)
    nome_campeao = TFT_CHAMPIONS[champ_id - 1]
    bits_nome = binario_para_int(nome_campeao)

    # 2. Converter estrelas para bits (usando 3 bits é suficiente para o número 4 -> 100)
    # Ex: 3 estrelas -> '011' -> [0, 1, 1]
    bits_estrelas = [int(b) for b in format(stars, '03b')]

    # 3. Concatenar: A "semente temática" é o Nome + Estrelas
    return bits_nome + bits_estrelas

def combinar_com_tema(seed_bits_usuario, bits_tft):
    """
    Adapta os bits do tema para terem o mesmo tamanho da seed do usuário
    e aplica XOR.
    """
    len_seed = len(seed_bits_usuario)
    len_tft = len(bits_tft)

    if len_seed == 0:
        return []

    # ADAPTAÇÃO: Esticar ou cortar os bits do TFT para casar com a seed
    # Ex: Se seed tem 50 bits e TFT tem 20, repetimos TFT até 50.
    fator_multiplicacao = (len_seed // len_tft) + 1
    tft_extendido = (bits_tft * fator_multiplicacao)[:len_seed]

    # FUSÃO: XOR bit a bit
    seed_combinada = []
    for b_seed, b_tft in zip(seed_bits_usuario, tft_extendido):
        seed_combinada.append(b_seed ^ b_tft)

    return seed_combinada

def GEN(seed_frase, input_champ, input_stars):
    """
    Gera a chave K tolerando qualquer input numérico.
    """
    # 1. Tratamento Determinístico dos Inputs (A Melhoria)
    # Não importa se digitaram 999, vai virar um campeão válido.
    champ_index = obter_campeao_seguro(input_champ)
    stars_val = obter_estrelas_seguro(input_stars)
    
    # Recupera nome para log/debug (Opcional)
    nome_champ = TFT_CHAMPIONS[champ_index]
    
    # 2. Processo normal de geração (igual ao anterior)
    seed_bits = binario_para_int(seed_frase)
    
    # Aqui passamos champ_index + 1 porque a função auxiliar esperava 1-40
    tft_bits = gerar_bits_tft(champ_index + 1, stars_val) 
    
    seed_final = combinar_com_tema(seed_bits, tft_bits)
    
    # Geração da chave
    seed_int = int("".join(map(str, seed_final)), 2)
    random.seed(seed_int)
    
    tamanho_chave = 4 * len(seed_bits)
    K = [random.randint(0, 1) for _ in range(tamanho_chave)]
    
    # Retornamos também os metadados para você ver o que foi escolhido
    return K, nome_champ, stars_val