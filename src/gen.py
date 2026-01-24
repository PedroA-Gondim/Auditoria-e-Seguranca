# src/gen.py
import random

def GEN(seed: list[int]) -> list[int]:
    """
    Recebe uma seed (lista binária) e gera uma chave K pseudo-aleatória.
    O tamanho de K será 4 vezes o tamanho da seed.
    """
    tamanho_alvo = 4 * len(seed)
    
    # ETAPA 1: CONVERTER A SEED EM UM NÚMERO INTEIRO
    # Exemplo: [1, 0, 1] → "101" → 5
    # Isso é importante porque transforma a lista binária em um valor único
    # que será usado para inicializar o gerador de números aleatórios.
    # Sem isso, [0, 1] e [1, 0] poderiam gerar a mesma chave (problema de colisão).
    seed_string = "".join(str(b) for b in seed)
    
    # Se a seed estiver vazia, usa 0 como valor padrão
    if not seed_string:
        seed_int = 0
    else:
        # int(seed_string, 2) converte a string binária para um inteiro
        # O parâmetro 2 indica que a string está em base binária
        seed_int = int(seed_string, 2)
    
    # ETAPA 2: INICIALIZAR O GERADOR ALEATÓRIO
    # A função random.seed() define o estado inicial do gerador
    # Com a mesma seed, sempre gera a mesma sequência (determinístico)
    random.seed(seed_int)
    
    # ETAPA 3: GERAR A CHAVE
    # Cria uma lista com 'tamanho_alvo' bits aleatórios (0 ou 1)
    # Cada elemento é escolhido aleatoriamente de [0, 1]
    key = [random.choice([0, 1]) for _ in range(tamanho_alvo)]
    
    return key