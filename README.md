# Implementação de Esquema Criptográfico Simplificado

Este projeto apresenta a implementação de um algoritmo de criptografia simplificado, desenvolvido como requisito para a avaliação do Trabalho 1. O sistema implementa funções de geração de chaves, cifragem e decifragem, operando sobre listas binárias.

## 📋 Sobre o Projeto

O objetivo principal é demonstrar conceitos fundamentais de criptografia, focando em propriedades de **Confusão** e **Difusão**. O algoritmo foi desenhado para garantir que pequenas alterações na entrada (chave ou mensagem) resultem em grandes alterações na saída (efeito avalanche).

### Funcionalidades Implementadas
* **GEN(seed):** Gera uma chave binária pseudoaleatória com tamanho $4 \times len(seed)$.
* **ENC(K, M):** Cifra uma mensagem binária utilizando operações de permutação e XOR.
* **DEC(K, C):** Recupera a mensagem original a partir da cifra e da chave.

---

## 🛠️ Requisitos

* **Linguagem:** Python 3.10.11.
* **Bibliotecas:** Nenhuma biblioteca externa é necessária (apenas bibliotecas padrão como `random`, `time`, `statistics`).

---

## 🚀 Como Executar

### 1. Clonar o Repositório
```bash
git clone https://github.com/PedroA-Gondim/Auditoria-e-Seguranca
cd src
```
---

### 2. Execução Básica
Para verificar o funcionamento básico (Geração -> Encriptação -> Decriptação):

```Bash
python main.py
```
Isso executará um cenário de demonstração validando se a mensagem descriptografada é idêntica à original.

---

### 📊 Testes e Métricas de Avaliação
O projeto inclui um script automatizado (testes.py) para validar os critérios de qualidade exigidos na especificação.

Para rodar os testes detalhados:
```Bash
python testes.py
```
O script gerará relatórios no terminal cobrindo os seguintes pontos:
 1. **Tempo de Execução:** Mede o tempo médio de processamento das funções ENC e DEC em múltiplas execuções, visando a eficiência do algoritmo.
 2. **Análise de Colisões (Chaves Equivalentes):** Verifica a integridade do espaço de chaves, garantindo que chaves diferentes ($K_1 \neq K_2$) não gerem a mesma cifra para uma mesma mensagem ($ENC(M, K_1) \neq ENC(M, K_2)$).
 3. **Teste de Difusão (Avalanche na Mensagem):** Avalia o impacto da alteração de 1 bit na mensagem original ($M$).Métrica: Percentual de bits alterados na cifra ($C$).Objetivo: Aproximar-se de 50% de alteração para máxima difusão.
 4. **Teste de Confusão (Avalanche na Seed/Chave):** Avalia o impacto da alteração de 1 bit na seed geradora da chave.Métrica: Percentual de bits alterados na cifra ($C$) mantendo a mensagem fixa.
---

### 📂 Estrutura de Arquivos
* **src**: Contém os códigos com a lógica core (GEN, ENC, DEC) e funções auxiliares.
* **tests**: scripts para testes de desempenho e qualidade.
* **docs**: documentos para apresentação.

---

### 📝 Autoria

* **Alunos**: Pedro Alexandre Gondim Neto e Dyany Cristine Garcia da Silva

* **Disciplina**: Segurança e Auditoria de Sistemas

* **Data**: 04/02/2026

---
