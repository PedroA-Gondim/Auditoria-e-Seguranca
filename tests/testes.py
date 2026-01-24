import test_velocExec
import test_Colis
import test_confusao
import test_difusao


def main():
    print("\n" + "=" * 60 + "\n")
    print("   INICIANDO BATERIA DE TESTES AUTOMATIZADOS")
    print("\n" + "=" * 60 + "\n")

    # 1. Teste de Tempo
    test_velocExec.run()

    # 2. Teste de Colisões (Chaves Equivalentes)
    test_Colis.run()

    # 3. Teste de Difusão
    test_difusao.run()

    # 4. Teste de Confusão
    test_confusao.run()

    print("\n" + "=" * 60 + "\n")
    print("   TODOS OS TESTES FINALIZADOS")
    print("\n" + "=" * 60 + "\n")


if __name__ == "__main__":
    main()
