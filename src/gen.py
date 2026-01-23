# src/gen.py
import random

def GEN(seed: list[int]) -> list[int]:
    """
    Recebe uma seed (lista binária) e gera uma chave K pseudo-aleatória.
    O tamanho de K será 4 vezes o tamanho da seed.
    """
    tamanho_alvo = 4 * len(seed)
    
    # CONVERSÃO ROBUSTA: 
    # Transforma a lista de bits [1, 0, 1] na string "101" e depois no inteiro 5.
    # Isso evita que [0, 1] e [1, 0] gerem a mesma chave (colisão).
    seed_string = "".join(str(b) for b in seed)
    if not seed_string:
        seed_int = 0
    else:
        seed_int = int(seed_string, 2)
    
    # Inicializa o gerador com esse inteiro único
    random.seed(seed_int)
    
    # Gera a chave
    key = [random.choice([0, 1]) for _ in range(tamanho_alvo)]
    
    return key