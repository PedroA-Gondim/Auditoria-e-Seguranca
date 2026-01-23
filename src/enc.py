# src/enc.py

def ENC(K: list[int], M: list[int]) -> list[int]:
    """
    Criptografia com Feedback (Chaining).
    C[i] = M[i] XOR K[i] XOR C[i-1]
    Isso garante que uma mudança no início da mensagem se propague até o fim (Difusão).
    """
    if len(K) != len(M):
        raise ValueError(f"Erro de tamanho: Chave={len(K)}, Msg={len(M)}")
    
    cifra = []
    # Vetor de Inicialização (IV) virtual para o primeiro bit (pode ser 0 ou 1)
    # Em sistemas reais, o IV deve ser aleatório e enviado junto. Aqui usamos 0 fixo.
    bit_anterior_cifra = 0 
    
    for m_bit, k_bit in zip(M, K):
        # O bit cifrado depende do bit da msg, da chave E do resultado anterior
        c_bit = m_bit ^ k_bit ^ bit_anterior_cifra
        
        cifra.append(c_bit)
        
        # Atualiza o "anterior" para a próxima iteração
        bit_anterior_cifra = c_bit
        
    return cifra