# src/utils.py

def texto_para_binario(texto: str) -> list[int]:
    """Converte string para lista de bits (ASCII 8 bits)."""
    bits = []
    for char in texto:
        # Converte para binário, remove o '0b' e preenche com zeros à esquerda
        bin_val = bin(ord(char))[2:].zfill(8)
        bits.extend([int(b) for b in bin_val])
    return bits

def binario_para_texto(bits: list[int]) -> str:
    """Converte lista de bits para string."""
    chars = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        # Se sobrar bits quebrados no final (menos de 8), ignora
        if len(byte) < 8: break
        str_val = "".join(str(b) for b in byte)
        chars.append(chr(int(str_val, 2)))
    return "".join(chars)

def xor_listas(lista_a: list[int], lista_b: list[int]) -> list[int]:
    """Aplica XOR bit a bit."""
    # O zip corta no tamanho da menor lista, então garantimos tamanhos iguais antes
    return [a ^ b for a, b in zip(lista_a, lista_b)]

def ajustar_tamanho_msg(msg: list[int], tamanho_alvo: int) -> list[int]:
    """
    Ajusta a mensagem para ter EXATAMENTE o tamanho da chave (tamanho_alvo).
    - Se for menor: Preenche com zeros (padding).
    - Se for maior: Corta (truncamento) - para simplificação do trabalho.
    """
    tamanho_atual = len(msg)
    
    if tamanho_atual == tamanho_alvo:
        return msg
    
    if tamanho_atual < tamanho_alvo:
        # Adiciona zeros ao final
        padding = [0] * (tamanho_alvo - tamanho_atual)
        return msg + padding
    else:
        # Corta o excesso
        return msg[:tamanho_alvo]