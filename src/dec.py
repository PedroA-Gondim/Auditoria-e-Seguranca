import random
from src.utils import xor_listas


def DEC(K: list[int], C: list[int]) -> list[int]:
    """
    Descriptografa uma mensagem cifrada utilizando o algoritmo DEC (Decryption).
    Este algoritmo implementa a descriptografia através da reversão dos passos
    realizados na cifra, seguindo o princípio de Kerckhoffs onde a segurança
    depende apenas da chave secreta.
    Passos da Descriptografia (ordem inversa da cifra):
    1. REVERSÃO DA PERMUTAÇÃO (Shuffle):
       - Utiliza a chave K como semente para inicializar um gerador de números
         pseudo-aleatórios (PRNG - Pseudo-Random Number Generator).
       - Reconstrói a mesma sequência de permutação determinística que foi
         aplicada durante a cifra.
       - Reverte a permutação do criptograma C, restaurando a ordem original
         das posições dos caracteres.
       - Conceito: A permutação é uma operação transposicional que modifica a
         posição dos elementos, mas não os altera.
    2. REVERSÃO DA PROPAGAÇÃO (XOR em Cascata Reverso):
       - Desfaz a operação de difusão que propaga a mudança de cada bit para
         os bits subsequentes.
       - Processa o vetor de trás para frente (ordem inversa) aplicando XOR
         entre elementos consecutivos: M[i] = C[i] ^ M[i+1].
       - Conceito: A operação XOR é autoinversa (A ^ B ^ B = A), permitindo
         reversibilidade. A propagação aumenta a difusão criptográfica.
    3. REVERSÃO DO XOR INICIAL (Subtração de Chave):
       - Aplica XOR entre o resultado da propagação reversa e a chave K.
       - Desfaz o pré-processamento que combinou a mensagem com a chave.
       - Conceito: O XOR é comutativo e associativo, garantindo que a
         operação inversa recupere a mensagem original.
    Args:
        K (list[int]): Chave criptográfica (lista de bits: 0 ou 1).
        C (list[int]): Criptograma a ser descriptografado (lista de bits: 0 ou 1).
    Returns:
        list[int]: Mensagem original em forma de lista de bits.
    Nota: Esta função assume que C foi cifrado com a mesma chave K usando
    o algoritmo de cifra correspondente (ENC).
    """
    semente = int("".join(map(str, K)), 2)
    rng = random.Random(semente)

    # 1. Reverter Permutação
    indices = list(range(len(C)))
    rng.shuffle(indices)
    permutado = [0] * len(C)
    for i, idx_orig in enumerate(indices):
        permutado[idx_orig] = C[i]

    # 2. Reverter PROPAGAÇÃO (Ordem inversa)
    for i in range(len(permutado) - 1, 0, -1):
        permutado[i] = permutado[i] ^ permutado[i - 1]

    # 3. Reverter XOR Inicial
    return xor_listas(permutado, K)
