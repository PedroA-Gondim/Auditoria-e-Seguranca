# src/dec.py
from src.utils import xor_listas

def DEC(K: list[int], C: list[int]) -> list[int]:
    """
    Recebe a chave K e a cifra C. Retorna a mensagem original M.
    """
    # --- LOGICA TEMPORARIA PARA O ESQUELETO ---
    # Se usarmos XOR na encriptação, a decriptação é exatamente a mesma operação:
    # (M XOR K) XOR K = M
    mensagem = xor_listas(C, K)
    
    return mensagem