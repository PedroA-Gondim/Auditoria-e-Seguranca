import random
import hashlib


def GEN(seed) -> list[int]:
    """
    Gerador de chave pseudoaleatória baseado em seed.

    Implementa um gerador de chave criptográfica que recebe uma seed
    (string ou lista de bits) e expande para uma chave K com tamanho
    4 vezes maior que a entrada.

    Args:
        seed: Uma string ou lista de bits [0, 1] que serve como valor inicial

    Returns:
        list[int]: Sequência de bits (0 e 1) representando a chave gerada
    """

    # PASSO 1: Normalizar a entrada para representação de string
    # Justificativa: Padroniza a entrada para processamento uniforme,
    # transformando [0, 1, 0] em "010" se necessário.
    if isinstance(seed, list):
        seed_str = "".join(str(b) for b in seed)
    else:
        seed_str = str(seed)

    # PASSO 2: Aplicar função Hash criptográfica (SHA-256)
    # Justificativa: Atende ao princípio de CONFUSÃO de Shannon.
    # O hash garante que pequenas mudanças na seed (ex: "seed1" vs "seed2")
    # resultem em saídas completamente diferentes e imprevisíveis.
    # Isso amplifica a separação estatística entre chaves derivadas de seeds similares.
    hash_objeto = hashlib.sha256(seed_str.encode())
    seed_hex = hash_objeto.hexdigest()
    seed_int = int(seed_hex, 16)  # Converte valor hexadecimal para inteiro de 256 bits

    # PASSO 3: Calcular tamanho da chave conforme especificação
    # Justificativa: Expansão de 4x o tamanho da seed fornece
    # comprimento de chave adequado para aplicações criptográficas.
    tamanho_alvo = 4 * len(seed)

    # PASSO 4: Inicializar o gerador pseudoaleatório (PRNG)
    # Justificativa: O PRNG determinístico usa o hash como estado inicial,
    # garantindo que a mesma seed sempre gera a mesma chave (reprodutibilidade).
    random.seed(seed_int)

    # PASSO 5: Gerar sequência de bits pseudoaleatória
    # Justificativa: Produz a saída binária expandida usando o PRNG
    # inicializado, aplicando o princípio de DIFUSÃO (alterações na entrada
    # se propagam para toda a saída).
    key = [random.choice([0, 1]) for _ in range(tamanho_alvo)]

    return key
