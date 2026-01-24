# src/enc.py

def ENC(K: list[int], M: list[int]) -> list[int]:
    """
    Criptografia com Feedback (Chaining).
    
    Cada bit cifrado depende de:
    1. O bit da mensagem original (M[i])
    2. O bit da chave (K[i])
    3. O bit cifrado anterior (C[i-1])
    
    Fórmula: C[i] = M[i] XOR K[i] XOR C[i-1]
    
    Vantagem: Uma mudança em qualquer bit da mensagem se propaga para todos os bits
    posteriores da cifra (propriedade de Difusão).
    """
    
    # Valida se chave e mensagem têm o mesmo comprimento
    if len(K) != len(M):
        raise ValueError(f"Erro de tamanho: Chave={len(K)}, Msg={len(M)}")
    
    cifra = []
    
    # Inicialização: o bit "anterior" começa em 0
    # Em sistemas reais, isso seria um Vetor de Inicialização (IV) aleatório e secreto
    # Para este exercício, usamos 0 como valor inicial fixo
    bit_anterior_cifra = 0 
    
    # Processa cada bit da mensagem com seu correspondente na chave
    for m_bit, k_bit in zip(M, K):
        # Calcula o bit cifrado atual aplicando XOR com três operandos:
        # - m_bit: bit da mensagem original
        # - k_bit: bit da chave
        # - bit_anterior_cifra: bit cifrado da posição anterior
        c_bit = m_bit ^ k_bit ^ bit_anterior_cifra
        
        # Armazena o bit cifrado no resultado final
        cifra.append(c_bit)
        
        # Prepara para a próxima iteração: o bit que acabamos de cifrar
        # será usado como "anterior" para o próximo bit
        bit_anterior_cifra = c_bit
        
    return cifra