#### sistema_bancario_modular.py
# Sistema bancário modularizado com funções: saques, depósitos, extrato,
# criação de usuário e criação de conta. Agora operações filtram por CPF e depois por conta.

# Lista de usuários e contas
usuarios = []  # cada usuário: dict(nome, data_nascimento, cpf, endereco)
contas   = []  # cada conta: dict(agencia, numero, cpf, saldo, extrato, numero_saques)

# Função de saque: keyword-only e retorna saldo, extrato e numero_saques
def saque(*, saldo, valor, extrato, numero_saques, limite_saques, limite):
    if valor <= 0:
        print("Falha: valor inválido para saque.")
    elif valor > saldo:
        print("Falha: saldo insuficiente.")
    elif numero_saques >= limite_saques:
        print("Falha: limite de saques diários atingido.")
    elif valor > limite:
        print(f"Falha: excede o limite de R$ {limite:.2f} por saque.")
    else:
        saldo -= valor
        numero_saques += 1
        extrato += f"Saque:    R$ {valor:.2f}\n"
        print("Saque realizado com sucesso!")
    return saldo, extrato, numero_saques

# Função de depósito: positional-only e retorna saldo e extrato
def deposito(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
        print("Depósito realizado com sucesso!")
    else:
        print("Falha: valor inválido para depósito.")
    return saldo, extrato

# Função de extrato: saldo posicional, extrato nomeado
def exibir_extrato(saldo, /, *, extrato):
    print("\n======= EXTRATO =======")
    if not extrato:
        print("Não foram realizadas movimentações.")
    else:
        print(extrato, end="")
    print(f"Saldo atual: R$ {saldo:.2f}")
    print("=======================\n")

# Função para cadastrar usuário na lista
def criar_usuario(usuarios, nome, data_nascimento, cpf, endereco):
    cpf_nums = ''.join(filter(str.isdigit, cpf))
    if any(u['cpf'] == cpf_nums for u in usuarios):
        print("Falha: CPF já cadastrado.")
        return False
    usuarios.append({
        'nome': nome,
        'data_nascimento': data_nascimento,
        'cpf': cpf_nums,
        'endereco': endereco
    })
    print(f"Usuário {nome} cadastrado com sucesso!")
    return True

# Função para criar conta vinculada a um CPF existente
def criar_conta(contas, usuarios, agencia, numero, cpf):
    cpf_nums = ''.join(filter(str.isdigit, cpf))
    usuario = next((u for u in usuarios if u['cpf'] == cpf_nums), None)
    if not usuario:
        print("Falha: CPF não encontrado.")
        return False
    # não há conflito de número entre contas de um mesmo usuário
    contas.append({
        'agencia': agencia,
        'numero': numero,
        'cpf': cpf_nums,
        'saldo': 0.0,
        'extrato': "",
        'numero_saques': 0
    })
    print(f"Conta {numero} criada para {usuario['nome']}.")
    return True

# Menu e entradas intermediárias para operações
MENU = '''
[u] Cadastrar Usuário
[c] Criar Conta
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair
Escolha: '''

# Auxiliar: selecionar conta de um usuário
def selecionar_conta(contas, cpf_nums):
    # filtra contas do usuário
    minhas_contas = [c for c in contas if c['cpf'] == cpf_nums]
    if not minhas_contas:
        print("Nenhuma conta para este CPF.")
        return None
    # se só uma conta, retorna ela
    if len(minhas_contas) == 1:
        return minhas_contas[0]
    # se múltiplas, lista e escolhe
    print("Contas disponíveis:")
    for c in minhas_contas:
        print(f"- Agência: {c['agencia']} | Conta: {c['numero']}")
    numero = input("Informe o número da conta desejada: ")
    conta = next((c for c in minhas_contas if c['numero'] == numero), None)
    if not conta:
        print("Conta inválida.")
    return conta

# Função principal
def main():
    AGENCIA_PADRAO = '0001'
    while True:
        opc = input(MENU).strip().lower()
        if opc == 'u':
            nome = input("Nome: ")
            data_nasc = input("Data de nascimento (DD/MM/AAAA): ")
            cpf = input("CPF (com pontuação ou números): ")
            endereco = input("Endereço (logradouro, nro - bairro - cidade/UF): ")
            criar_usuario(usuarios, nome, data_nasc, cpf, endereco)

        elif opc == 'c':
            cpf = input("CPF do titular: ")
            numero = input("Número da conta: ")
            criar_conta(contas, usuarios, AGENCIA_PADRAO, numero, cpf)

        elif opc in ('d', 's', 'e'):
            cpf = input("CPF do titular: ")
            cpf_nums = ''.join(filter(str.isdigit, cpf))
            user = next((u for u in usuarios if u['cpf'] == cpf_nums), None)
            if not user:
                print("Usuário não encontrado.")
                continue
            conta = selecionar_conta(contas, cpf_nums)
            if not conta:
                continue

            if opc == 'd':
                valor = float(input("Valor do depósito: R$ "))
                conta['saldo'], conta['extrato'] = deposito(
                    conta['saldo'], valor, conta['extrato']
                )

            elif opc == 's':
                valor = float(input("Valor do saque: R$ "))
                conta['saldo'], conta['extrato'], conta['numero_saques'] = saque(
                    saldo=conta['saldo'], valor=valor,
                    extrato=conta['extrato'], numero_saques=conta['numero_saques'],
                    limite_saques=3, limite=500.0
                )

            elif opc == 'e':
                exibir_extrato(conta['saldo'], extrato=conta['extrato'])

        elif opc == 'q':
            print("Encerrando sistema. Obrigado!")
            break

        else:
            print("Opção inválida. Tente novamente.")

if __name__ == '__main__':
    main()
