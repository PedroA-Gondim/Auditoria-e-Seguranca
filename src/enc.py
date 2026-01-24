import random
from src.utils import xor_listas

def ENC(K: list[int], M: list[int]) -> list[int]:
    """
    Função de Encriptação com Difusão e Confusão.
    Implementa um esquema de encriptação simétrica que combina operações de 
    confusão (XOR) e difusão (propagação e permutação) para garantir que 
    alterações em um bit de entrada afetem múltiplos bits da saída.
    Passos do Algoritmo:
    1. XOR Inicial (Confusão):
       - Realiza XOR entre a mensagem M e a chave K
       - Introduz a chave no estado inicial, aplicando o princípio de Confusão:
         cada bit da saída depende de bits da entrada e da chave de forma 
         complexa e não-linear
    2. Propagação (Difusão em Cascata):
       - Propaga a influência de cada bit para os bits subsequentes
       - Cada bit do estado é combinado (XOR) com o bit anterior
       - Garante o princípio de Difusão: uma mudança em um bit de entrada 
         afeta aproximadamente metade dos bits de saída
       - Cria dependência entre posições, impedindo análise de bits isolados
    3. Permutação Determinística (Difusão Posicional):
       - Embaralha as posições dos bits usando gerador pseudo-aleatório 
         seeded pela chave K
       - Aumenta a difusão espacial, distribuindo bits correlatos em 
         posições não-adjacentes
       - Garante determinismo: mesma chave sempre produz mesma permutação
    Args:
        K (list[int]): Chave de encriptação (lista de bits)
        M (list[int]): Mensagem a ser encriptada (lista de bits)
    Returns:
        list[int]: Mensagem encriptada (lista de bits permutada)
    Raises:
        ValueError: Se o tamanho de K e M forem diferentes
    Conceitos de Segurança Aplicados:
        - Confusão: Torna a relação entre chave e criptograma complexa
        - Difusão: Dispersa a redundância da mensagem original
        - Determinismo: Permite decodificação consistente com a mesma chave
    """
    if len(K) != len(M):
        raise ValueError("Erro de tamanho")
    
    # 1. XOR Inicial
    estado = xor_listas(M, K)
    
    # 2. PROPAGAÇÃO (A mágica da difusão)
    # Fazemos com que cada bit dependa do bit anterior (Efeito Cascata)
    for i in range(1, len(estado)):
        estado[i] = estado[i] ^ estado[i-1]
        
    # 3. Permutação Determinística
    semente = int("".join(map(str, K)), 2)
    rng = random.Random(semente)
    indices = list(range(len(estado)))
    rng.shuffle(indices)
    
    return [estado[i] for i in indices]