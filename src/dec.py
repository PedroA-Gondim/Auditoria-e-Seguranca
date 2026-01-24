# src/dec.py

def DEC(K: list[int], C: list[int]) -> list[int]:
    """
    Descriptografia com Feedback (CFB - Cipher Feedback Mode).
    
    Recupera a mensagem original usando:
    M[i] = C[i] XOR K[i] XOR C[i-1]
    
    Onde:
    - C[i]: bit cifrado atual
    - K[i]: bit da chave de stream (gerada pela cifra)
    - C[i-1]: bit cifrado anterior (feedback)
    """
    mensagem = []
    # Inicializa com IV (Vetor de Inicialização) = 0, mesmo usado na encriptação
    bit_anterior_cifra = 0
    
    for c_bit, k_bit in zip(C, K):
        # Etapa 1: Recupera o bit original fazendo XOR triplo
        # - XOR com K[i] (remove a chave de stream)
        # - XOR com C[i-1] (remove o feedback do bit anterior)
        m_bit = c_bit ^ k_bit ^ bit_anterior_cifra
        
        # Etapa 2: Armazena o bit recuperado da mensagem
        mensagem.append(m_bit)
        
        # Etapa 3: Atualiza o feedback para a próxima iteração
        # IMPORTANTE: Usa C[i] (bit cifrado), não M[i] (bit recuperado)
        # Isso garante sincronização com o processo de encriptação
        bit_anterior_cifra = c_bit
        
    return mensagem