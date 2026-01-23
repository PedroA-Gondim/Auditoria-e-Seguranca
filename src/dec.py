# src/dec.py

def DEC(K: list[int], C: list[int]) -> list[int]:
    """
    Descriptografia com Feedback.
    M[i] = C[i] XOR K[i] XOR C[i-1]
    """
    mensagem = []
    bit_anterior_cifra = 0 # Mesmo IV usado no ENC
    
    for c_bit, k_bit in zip(C, K):
        # Para recuperar M, fazemos XOR do C atual com K e o C anterior
        m_bit = c_bit ^ k_bit ^ bit_anterior_cifra
        
        mensagem.append(m_bit)
        
        # Importante: O "anterior" que usamos para o próximo passo é o Cifra (C),
        # não a mensagem recuperada.
        bit_anterior_cifra = c_bit
        
    return mensagem