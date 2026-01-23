# src/enc.py
from src.utils import xor_listas

def ENC(K: list[int], M: list[int]) -> list[int]:
    """
    Recebe a chave K e a mensagem M. Retorna a cifra C.
    Requisito: K, M e C devem ter o mesmo tamanho.
    """
    if len(K) != len(M):
        raise ValueError(f"Tamanho da chave ({len(K)}) e mensagem ({len(M)}) devem ser iguais.")
    
    # --- LOGICA TEMPORARIA PARA O ESQUELETO ---
    # O jeito mais simples de criptografar (e que permite descriptografar fácil)
    # é fazer um XOR entre a Mensagem e a Chave.
    cifra = xor_listas(M, K)
    
    return cifra