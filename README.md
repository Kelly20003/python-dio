# Sistema Bancário em Python (Versão 2.0 - Orientado a Objetos)

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)

Este projeto é uma versão refatorada e aprimorada de um sistema bancário, agora implementado com os princípios da **Programação Orientada a Objetos (POO)** em Python. O sistema simula as operações básicas de um banco, como criação de clientes, contas, depósitos, saques e visualização de extratos, com uma estrutura de código mais robusta, modular e escalável.

## 🚀 Funcionalidades Principais

O sistema oferece um menu interativo no console com as seguintes operações:

* **[d] Depositar:** Adiciona um valor ao saldo de uma conta existente.
* **[s] Sacar:** Retira um valor do saldo de uma conta, respeitando limites e número de saques diários.
* **[e] Extrato:** Exibe o histórico de transações (depósitos e saques) e o saldo atual da conta.
* **[nu] Novo Usuário:** Cadastra um novo cliente (Pessoa Física) no sistema, validando se o CPF já existe.
* **[nc] Nova Conta:** Cria uma nova conta corrente vinculada a um cliente já cadastrado.
* **[lc] Listar Contas:** Exibe uma lista formatada de todas as contas cadastradas no banco.
* **[q] Sair:** Encerra a execução do programa.

## ✨ Estrutura do Código e Conceitos Aplicados

O projeto foi modelado utilizando conceitos avançados de POO para garantir um código limpo e de fácil manutenção:

* **Abstração e Herança:**
    * `Cliente` é uma classe base que define a estrutura geral de um cliente.
    * `PessoaFisica` herda de `Cliente`, adicionando atributos específicos como nome e CPF.
    * `Conta` é a classe base para contas bancárias.
    * `ContaCorrente` herda de `Conta`, implementando regras de negócio próprias (limite de saque e número de saques).
    * `Transacao` é uma classe abstrata que define a interface para `Saque` e `Deposito`.

* **Encapsulamento:**
    * Atributos como `_saldo`, `_numero`, `_agencia` são protegidos, e seu acesso é feito através de `@property` (getters), garantindo maior controle e segurança.

* **Polimorfismo:**
    * O método `sacar()` da classe `ContaCorrente` sobrescreve o método da classe mãe (`Conta`) para aplicar regras de negócio específicas, demonstrando polimorfismo.

* **Composição:**
    * A classe `Cliente` "tem" uma ou mais `Contas`.
    * A classe `Conta` "tem" um `Historico` de transações.

* **Iteradores:**
    * A classe `ContasIterador` foi implementada para percorrer a lista de contas de forma otimizada e elegante, sendo utilizada na funcionalidade de "Listar Contas".

* **Métodos de Classe (`@classmethod`):**
    * O método `nova_conta()` na classe `Conta` funciona como uma *factory*, centralizando a lógica de criação de novas instâncias.

## 🛠️ Como Executar

Para executar o sistema, você precisa ter o Python 3 instalado em sua máquina.

1.  **Clone o repositório (ou baixe os arquivos):**
    ```bash
    git clone [https://github.com/seu-usuario/seu-repositorio.git](https://github.com/seu-usuario/seu-repositorio.git)
    ```

2.  **Navegue até a pasta do projeto:**
    ```bash
    cd seu-repositorio
    ```

3.  **Execute o script principal:**
    ```bash
    python nome_do_seu_arquivo.py
    ```

    O menu interativo será exibido no terminal, e você poderá começar a usar o sistema.

## 👨‍💻 Autor

Este projeto foi desenvolvido por **Kelly e a equipe da DIO**.

* **LinkedIn:** `www.linkedin.com/in/kelly-antunes77`

