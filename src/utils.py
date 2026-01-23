# src/utils.py
import random

def texto_para_binario(texto: str) -> list[int]:
    """Converte uma string de texto para uma lista de bits (0s e 1s)."""
    # Exemplo simples: converte cada char para binário de 8 bits
    bits = []
    for char in texto:
        bin_val = bin(ord(char))[2:].zfill(8)
        bits.extend([int(b) for b in bin_val])
    return bits

def binario_para_texto(bits: list[int]) -> str:
    """Converte uma lista de bits de volta para string."""
    chars = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        if len(byte) < 8: break
        str_val = "".join(str(b) for b in byte)
        chars.append(chr(int(str_val, 2)))
    return "".join(chars)

def xor_listas(lista_a: list[int], lista_b: list[int]) -> list[int]:
    """
    Aplica XOR bit a bit entre duas listas. 
    Essencial para criptografia simplificada.
    """
    return [a ^ b for a, b in zip(lista_a, lista_b)]