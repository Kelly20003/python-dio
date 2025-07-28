import textwrap
from abc import ABC, abstractmethod
from datetime import datetime

class ContasIterador:
    """Iterador para percorrer as contas de um cliente."""
    def __init__(self, contas):
        self.contas = contas
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        try:
            conta = self.contas[self._index]
            return f"""\
            Agência:\t{conta.agencia}
            Número:\t\t{conta.numero}
            Titular:\t{conta.cliente.nome}
            Saldo:\t\tR$ {conta.saldo:.2f}
            """
        except IndexError:
            raise StopIteration
        finally:
            self._index += 1

class Cliente:
    """Representa um cliente do banco."""
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        """Realiza uma transação em uma das contas do cliente."""
        if len(conta.historico.transacoes_do_dia()) >= 10:
            print("\n@@@ Você excedeu o número de transações permitidas para hoje! @@@")
            return
            
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        """Adiciona uma conta ao cliente."""
        self.contas.append(conta)

class PessoaFisica(Cliente):
    """Representa um cliente do tipo Pessoa Física."""
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

    def __repr__(self) -> str:
        return f"<PessoaFisica: {self.nome}, CPF: {self.cpf}>"

class Conta:
    """Classe base para todas as contas."""
    def __init__(self, numero, cliente):
        self._saldo = 0.0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        """Cria uma nova conta."""
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        """Saca um valor da conta."""
        if valor > self.saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
            return False
        
        if valor <= 0:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False
        
        self._saldo -= valor
        print("\n=== Saque realizado com sucesso! ===")
        return True

    def depositar(self, valor):
        """Deposita um valor na conta."""
        if valor > 0:
            self._saldo += valor
            print("\n=== Depósito realizado com sucesso! ===")
            return True
        
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
        return False

class ContaCorrente(Conta):
    """Representa uma conta corrente, com limites específicos."""
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        """Sobrescreve o método sacar com regras da conta corrente."""
        saques_realizados = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        if valor > self.limite:
            print(f"\n@@@ Operação falhou! O valor do saque excede o limite de R$ {self.limite:.2f}. @@@")
            return False
        
        if saques_realizados >= self.limite_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
            return False
            
        return super().sacar(valor)

    def __repr__(self):
        return f"<ContaCorrente: Ag {self.agencia}, C/C {self.numero}, Saldo R$ {self.saldo:.2f}>"

class Historico:
    """Registra o histórico de transações de uma conta."""
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        """Adiciona uma transação ao histórico."""
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )
    
    def transacoes_do_dia(self):
        """Filtra e retorna as transações realizadas no dia de hoje."""
        hoje = datetime.utcnow().date()
        transacoes_diarias = []
        for transacao in self.transacoes:
            data_transacao = datetime.strptime(transacao["data"], "%d-%m-%Y %H:%M:%S").date()
            if hoje == data_transacao:
                transacoes_diarias.append(transacao)
        return transacoes_diarias


class Transacao(ABC):
    """Classe base para todas as transações."""
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    """Representa uma transação de saque."""
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        """Registra o saque na conta."""
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    """Representa uma transação de depósito."""
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        """Registra o depósito na conta."""
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)

# --- Funções Auxiliares para o Menu ---

def menu():
    menu_texto = """
    ===================== MENU =====================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nu]\tNovo Usuário
    [nc]\tNova Conta
    [lc]\tListar Contas
    [q]\tSair
    ==> """
    return input(textwrap.dedent(menu_texto)).lower()

def filtrar_cliente(cpf, clientes):
    """Busca um cliente pelo CPF."""
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(cliente):
    """Recupera a conta de um cliente."""
    if not cliente.contas:
        print("\n@@@ Cliente não possui conta! @@@")
        return None
    # FIXME: não permite cliente escolher a conta
    return cliente.contas[0]

def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)
    
    conta = recuperar_conta_cliente(cliente)
    if conta:
        cliente.realizar_transacao(conta, transacao)

def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if conta:
        cliente.realizar_transacao(conta, transacao)

def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes
    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['data']}\t{transacao['tipo']}:\t\tR$ {transacao['valor']:.2f}"
    
    print(extrato)
    print(f"\nSaldo:\t\tR$ {conta.saldo:.2f}")
    print("==========================================")


def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente número): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\n@@@ Já existe cliente com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
    clientes.append(cliente)

    print("\n=== Cliente criado com sucesso! ===")

def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado, fluxo de criação de conta encerrado! @@@")
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.adicionar_conta(conta)

    print("\n=== Conta criada com sucesso! ===")

def listar_contas(contas):
    if not contas:
        print("\n@@@ Nenhuma conta cadastrada. @@@")
        return
        
    print("\n================ LISTA DE CONTAS ================")
    for conta in ContasIterador(contas):
        print(textwrap.dedent(str(conta)))
        print("-" * 45)


def main():
    """Função principal que executa o sistema bancário."""
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            depositar(clientes)
        elif opcao == "s":
            sacar(clientes)
        elif opcao == "e":
            exibir_extrato(clientes)
        elif opcao == "nu":
            criar_cliente(clientes)
        elif opcao == "nc":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)
        elif opcao == "lc":
            listar_contas(contas)
        elif opcao == "q":
            print("\nObrigado por usar o Sistema Bancário S.A. Volte sempre!\n")
            break
        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

if __name__ == "__main__":
    main()