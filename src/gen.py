# src/gen.py
import random

def GEN(seed: list[int]) -> list[int]:
    """
    Recebe uma seed (lista binária) e gera uma chave K.
    Requisito: len(K) deve ser 4 * len(seed).
    """
    tamanho_alvo = 4 * len(seed)
    key = []
    
    # --- LOGICA TEMPORARIA PARA O ESQUELETO ---
    # TODO: Implementar sua lógica determinística aqui.
    # Por enquanto, vamos apenas repetir a seed e preencher o resto
    # Nota: Para o trabalho final, use algo que dependa da seed matematicamente,
    # senão o teste de confusão vai falhar.
    
    random.seed(sum(seed)) # Inicializa o random com a soma da seed (simples)
    key = [random.choice([0, 1]) for _ in range(tamanho_alvo)]
    
    return key