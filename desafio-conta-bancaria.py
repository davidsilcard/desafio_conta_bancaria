def main():
    # Estado inicial da conta
    saldo = 0.0
    extrato = ""             # string onde vamos acumular as linhas do extrato
    numero_saques = 0        # conta quantos saques já foram feitos hoje

    # Limites do sistema
    LIMITE_SAQUES = 3        # máximo de saques por dia
    LIMITE_POR_SAQUE = 500.0 # valor máximo por saque

    # Menu de opções
    menu = """
=== MENU ===
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair
Escolha uma opção: """

    while True:
        opcao = input(menu).strip().lower()

        if opcao == "d":
            # Depósito
            valor = float(input("Informe o valor do depósito: R$ "))
            if valor > 0:
                saldo += valor
                extrato += f"Depósito: R$ {valor:.2f}\n"
                print("Depósito realizado com sucesso!\n")
            else:
                print("Falha: valor inválido para depósito.\n")

        elif opcao == "s":
            # Saque
            valor = float(input("Informe o valor do saque: R$ "))

            if valor <= 0:
                print("Falha: valor inválido para saque.\n")
            elif valor > saldo:
                print("Falha: saldo insuficiente.\n")
            elif numero_saques >= LIMITE_SAQUES:
                print("Falha: número máximo de saques atingido hoje.\n")
            elif valor > LIMITE_POR_SAQUE:
                print(f"Falha: valor excede o limite de R$ {LIMITE_POR_SAQUE:.2f} por saque.\n")
            else:
                saldo -= valor
                numero_saques += 1
                extrato += f"Saque:    R$ {valor:.2f}\n"
                print("Saque realizado com sucesso!\n")

        elif opcao == "e":
            # Extrato
            print("\n------- EXTRATO -------")
            if not extrato:
                print("Não foram realizadas movimentações.")
            else:
                print(extrato, end="")
            print(f"Saldo atual: R$ {saldo:.2f}")
            print("-----------------------\n")

        elif opcao == "q":
            # Sair do programa
            print("Obrigado por usar o sistema. Até logo!")
            break

        else:
            print("Operação inválida, por favor escolha uma opção válida.\n")


if __name__ == "__main__":
    main()
