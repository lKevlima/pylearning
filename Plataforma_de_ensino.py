# importando json e criptografia
import json
from cryptography.fernet import Fernet


# Função para salvar os dados no arquivo JSON
def salvar_dados(dados, chave_secreta):
    salvar_dados = {"usuarios": dados, "chave_secreta": chave_secreta.decode()}
    with open("usuarios.json", "w") as arquivo:
        json.dump(salvar_dados, arquivo, indent=4)


# Função para carregar os dados do arquivo JSON
def carregar_dados():
    try:
        with open("usuarios.json", "r") as arquivo:
            dados = json.load(arquivo)
            if "usuarios" in dados and "chave_secreta" in dados:
                chave_secreta = dados["chave_secreta"].encode()
                return dados["usuarios"], chave_secreta
            else:
                raise ValueError("Estrutura do arquivo inválida")
    except (FileNotFoundError, json.JSONDecodeError, ValueError):
        chave_secreta = Fernet.generate_key()
        return [], chave_secreta

# Função para validar a senha


def validar_senha(senha):
    return len(senha) >= 6 and any(char.isupper() for char in senha) and any(char.isdigit() for char in senha)

# Função para validar email


def validar_email(email):
    return "@" in email and ".com" in email

# Função para calcular média de idade dos usuários


def calcular_media_idades(usuarios):
    if not usuarios:
        print("Nenhum usuário cadastrado para calcular a média.")
        return
    soma_idades = sum(usuario["Idade"] for usuario in usuarios)
    media_idades = soma_idades / len(usuarios)
    print(f"\nTotal de usuários cadastrados: {len(usuarios)}")
    print(f"Soma das idades: {soma_idades}")
    print(f"Média das idades: {media_idades:.2f}")


# Função para calcular a média das notas de desempenho e listar logins
def calcular_media_notas(usuarios):
    if not usuarios:
        print("Nenhum usuário cadastrado para calcular a média de notas.")
        return

    print("\nLista de usuários cadastrados (logins):")
    for usuario in usuarios:
        print(f"- {usuario['Email']}")

    total_notas = 0
    qtd_notas = 0
    usuarios_com_notas = 0

    for usuario in usuarios:
        if usuario["Desempenho"]:  # Verifica se há notas registradas
            total_notas += sum(usuario["Desempenho"])
            qtd_notas += len(usuario["Desempenho"])
            usuarios_com_notas += 1

    if qtd_notas > 0:
        # A soma das notas dividido pelo total de notas
        media_notas = total_notas / qtd_notas
        print(f"\nTotal de usuários com notas: {usuarios_com_notas}")
        print(f"Total de notas registradas: {qtd_notas}")
        print(f"Soma de todas as notas: {total_notas:.2f}")
        print(f"Média geral das notas: {media_notas:.2f}")
    else:
        print("\nNenhuma nota de desempenho registrada.")


# Função para consultar e alterar os dados do usuário
def consultar_alterar_usuario(usuarios, chave_secreta):
    email = input("Digite o e-mail do usuário: ").strip()
    for usuario in usuarios:
        if usuario["Email"] == email:
            print(f"Nome: {usuario['Nome']}")
            print(f"Idade: {usuario['Idade']}")
            print(f"E-mail: {usuario['Email']}")
            print(f"Tipo de usuário: {usuario['Tipo']}")
            print(f"Nível de conhecimento: {usuario['Nivel De Conhecimento']}")
            print(f"Desempenho: {usuario['Desempenho']}")
            acao = input("Deseja alterar os dados? (s/n): ").strip().lower()
            if acao == "s":
                usuario["Nome"] = input(
                    f"Nome atual: {usuario['Nome']}. Digite o seu novo nome: ").strip()
                usuario["Email"] = input(
                    f"E-mail atual: {usuario['Email']}. Digite o seu novo e-mail: ").strip()
                usuario["Idade"] = int(
                    input(f"Idade atual: {usuario['Idade']}. Digite uma nova idade: "))
                usuario["Nivel De Conhecimento"] = input(
                    f"Nível atual: {usuario['Nivel De Conhecimento']}. Digite o seu novo nível: ").strip()
                salvar_dados(usuarios, chave_secreta)
                print("Dados atualizados com sucesso.")
            return
    print("Usuário não encontrado.")


# Função para inserir os dados de desempenho do usuário
def inserir_desempenho(usuarios, chave_secreta):
    email_admin = input("Digite seu e-mail para autenticação: ").strip()
    usuario_admin = next(
        (user for user in usuarios if user["Email"] == email_admin), None)
    if not usuario_admin or usuario_admin["Tipo"] != "Administrador":
        print("Acesso negado! Apenas administradores podem alterar o desempenho.")
        return
    email = input(
        "Digite o e-mail do usuário para inserir um desempenho: ").strip()
    for usuario in usuarios:
        if usuario["Email"] == email:
            desempenho = usuario["Desempenho"]  # Mantém as notas existentes
            while True:
                try:
                    nota = float(
                        input("Digite a pontuação de desempenho (digite -1 para terminar): "))
                    if nota == -1:
                        break
                    desempenho.append(nota)
                except ValueError:
                    print("Entrada inválida. Por favor, insira um número.")
            usuario["Desempenho"] = desempenho
            salvar_dados(usuarios, chave_secreta)
            print("Desempenho registrado com sucesso.")
            return
    print("Usuário não encontrado.")


# Função para autenticação de login
def login(usuarios_cadastrados, fernet):
    email = input("Digite seu e-mail: ").strip()
    senha = input("Digite sua senha: ").strip()
    for usuario in usuarios_cadastrados:
        if usuario["Email"] == email:
            senha_criptografada = usuario["Senha"]
            senha_descriptografada = fernet.decrypt(
                senha_criptografada.encode()).decode()
            if senha == senha_descriptografada:
                print("Login bem-sucedido!")
                print(f"Nome: {usuario['Nome']}")
                print(f"Idade: {usuario['Idade']}")
                print(f"Tipo de usuário: {usuario['Tipo']}")
                print(f"E-mail: {usuario['Email']}")
                print(
                    f"Nível De Conhecimento: {usuario['Nivel De Conhecimento']}")
                print(f"Desempenho: {usuario['Desempenho']}")
                return usuario
            else:
                print("Senha incorreta!")
                return None
    print("Email não cadastrado.")
    return None


# Função para cadastrar o usuário
def cadastrar_usuario(usuarios_cadastrados, fernet, chave_secreta):
    nome = input("Digite seu nome: ")
    idade = int(input("Digite sua idade: "))
    nivel_conhecimento = input(
        "Digite seu nível de conhecimento (iniciante, intermediário ou avançado): ").strip()
    while True:
        email = input("Digite seu e-mail: ").strip()
        if not validar_email(email):
            print("Erro: O e-mail deve conter '@' e '.com'.")
        elif any(user["Email"] == email for user in usuarios_cadastrados):
            print("Erro: E-mail já cadastrado.")
        else:
            break
    while True:
        # Definição de senha do usuário
        senha = input(
            "Digite uma senha (mínimo 6 caracteres, 1 maiúscula e 1 número): ")
        if validar_senha(senha):
            # Senha sendo criptografada
            senha_criptografada = fernet.encrypt(senha.encode()).decode()
            break
        else:
            print("Erro: Senha fraca. Deve ter 6 caracteres, 1 maiúscula e 1 número.")
# Definição de tipo de usuário
    tipo_usuario = input(
        "Digite o tipo de usuário (Administrador ou Comum): ").strip().capitalize()
    if tipo_usuario not in ["Administrador", "Comum"]:
        tipo_usuario = "Comum"
    usuario = {
        "Nome": nome,
        "Email": email,
        "Idade": idade,
        "Nivel De Conhecimento": nivel_conhecimento,
        "Senha": senha_criptografada,
        "Tipo": tipo_usuario,
        "Desempenho": []
    }
    usuarios_cadastrados.append(usuario)
    salvar_dados(usuarios_cadastrados, chave_secreta)
    print(f"Cadastro realizado com sucesso! Bem-vindo, {nome}!")

# Função para perguntas


def questionario_logica(usuario, usuarios_cadastrados, chave_secreta):
    print("\n========== Questionário de Lógica de Programação ==========\n")
    print("\nResponda com 'a', 'b' ou 'c'.\n")
# Perguntas de Lógica da programação
    perguntas = [
        {"pergunta": "1. O que significa 'def' em Python?",
         "a": "Define uma função", "b": "Declara uma variável", "c": "Cria uma classe"},

        {"pergunta": "2. Qual dessas opções é usada para criar um comentário em Python?",
         "a": "//", "b": "#", "c": "/*"},

        {"pergunta": "3. Qual função é usada para obter a entrada do usuário em Python?",
         "a": "input()", "b": "scan()", "c": "get()"},

        {"pergunta": "4. Em Python, qual o tipo de dado para números inteiros?",
         "a": "int", "b": "float", "c": "str"},

        {"pergunta": "5. Qual é o operador usado para multiplicação em Python?",
         "a": "*", "b": "/", "c": "%"}
    ]

    # Respostas corretas para cada pergunta
    respostas_corretas = ["a", "b", "a", "a", "a"]
    respostas_usuario = []
    pontuacao = 0  # Inicializa a pontuação do usuário

    for i, pergunta in enumerate(perguntas):
        print(pergunta["pergunta"])
        print("a) " + pergunta["a"])
        print("b) " + pergunta["b"])
        print("c) " + pergunta["c"])

        resposta = input("Escolha a opção (a, b ou c): ").lower()
        while resposta not in ["a", "b", "c"]:
            print("Resposta inválida! Por favor, escolha 'a', 'b' ou 'c'.")
            resposta = input("Escolha a opção (a, b ou c): ").lower()

        respostas_usuario.append(resposta)

        # Verifica se a resposta está correta
        if resposta == respostas_corretas[i]:
            pontuacao += 1

    print(
        f"\nSua pontuação no questionário de Lógica de Programação: {pontuacao}/{len(perguntas)}")

    # Adiciona a pontuação ao desempenho do usuário
    usuario["Desempenho"].append(pontuacao)

    # Salva os dados atualizados no JSON
    salvar_dados(usuarios_cadastrados, chave_secreta)

    print("Pontuação registrada com sucesso.")

# Função para Perguntas


def questionario_estrutura(usuario, usuarios_cadastrados, chave_secreta):
    print("\n========== Questionário de Programação em Python ==========\n")
    print("\nResponda com 'a', 'b' ou 'c'.\n")
# Perguntas de Programação em Python
    perguntas = [
        {"pergunta": "1. O que é uma estrutura de controle?", "a": "Uma forma de organizar o código",
         "b": "Uma variável", "c": "Uma função"},
        {"pergunta": "2. Qual é a principal estrutura de controle condicional em Python?", "a": "while", "b": "for",
         "c": "print"},
        {"pergunta": "3. O que faz o comando 'else'?", "a": "Define uma variável",
         "b": "Executa um bloco de código quando a condição não é atendida", "c": "Repete uma ação já feita"},
        {"pergunta": "4. O que significa o comando 'elif'?", "a": "Executa código se uma condição for falsa",
         "b": "Executa um código caso a condição anterior falhe", "c": "Verifica se o número é par"},
        {"pergunta": "5. O comando 'break' serve para?", "a": "Parar o loop", "b": "Criar uma nova variável",
         "c": "Executar um comando repetidamente"}
    ]

    # Respostas corretas para cada pergunta
    respostas_corretas = ["a", "b", "b", "b", "a"]
    respostas_usuario = []
    pontuacao = 0  # Inicializa a pontuação do usuário

    for i, pergunta in enumerate(perguntas):
        print(pergunta["pergunta"])
        print("a) " + pergunta["a"])
        print("b) " + pergunta["b"])
        print("c) " + pergunta["c"])

        resposta = input("Escolha a opção (a, b ou c): ").lower()
        while resposta not in ["a", "b", "c"]:
            print("Resposta inválida! Por favor, escolha 'a', 'b' ou 'c'.")
            resposta = input("Escolha a opção (a, b ou c): ").lower()

        respostas_usuario.append(resposta)

        # Verifica se a resposta está correta
        if resposta == respostas_corretas[i]:
            pontuacao += 1

    print(
        f"\nSua pontuação no questionário de Estrutura de Controle: {pontuacao}/{len(perguntas)}")

    # Adiciona a pontuação ao desempenho do usuário
    usuario["Desempenho"].append(pontuacao)

    # Salva os dados atualizados no JSON
    salvar_dados(usuarios_cadastrados, chave_secreta)

    print("Pontuação registrada com sucesso.")

# Função para Perguntas


def questionario_funcoes(usuario, usuarios_cadastrados, chave_secreta):
    print("\nAgora vamos para o formulário de 'Entrada e saída'. Responda com 'a', 'b' ou 'c'.\n")
# Perguntas de Entrada e Saída
    perguntas = [
        {"pergunta": "1. O que é uma função?", "a":  "Uma variável",
            "b":  "Uma sequência de comandos", "c": "Um comando repetido"},
        {"pergunta": "2. Como se define uma função em Python?",
            "a": "function nome_funcao()", "b": "função nome_funcao:", "c": "def nome_funcao():"},
        {"pergunta": "3. O que faz o comando 'return'?", "a": "Retorna um valor de uma função",
            "b": "Repete o código", "c": "Chama a função novamente"},
        {"pergunta": "4. O que acontece quando uma função é chamada?",
            "a": "O código da função é executado", "b": "A função é definida", "c": "Nada acontece"},
        {"pergunta": "5. Como se chama uma função em Python?",
            "a": "chamar.nome_funcao()", "b": "funcao.nome()", "c": "nome_funcao()"}
    ]
    # Respostas corretas
    respostas_corretas = ["b", "c", "a", "a", "c"]
    respostas_usuario = []
    pontuacao = 0  # Inicializa a pontuação do usuário

    for i, pergunta in enumerate(perguntas):
        print(pergunta["pergunta"])
        print("a) " + pergunta["a"])
        print("b) " + pergunta["b"])
        print("c) " + pergunta["c"])

        resposta = input("Escolha a opção (a, b ou c): ").lower()
        while resposta not in ["a", "b", "c"]:
            print("Resposta inválida! Por favor, escolha 'a', 'b' ou 'c'.")
            resposta = input("Escolha a opção (a, b ou c): ").lower()

        respostas_usuario.append(resposta)

        # Verifica se a resposta está correta
        if resposta == respostas_corretas[i]:
            pontuacao += 1

    print(
        f"\nSua pontuação no questionário de Funções: {pontuacao}/{len(perguntas)}")

    # Adiciona a pontuação ao desempenho do usuário
    usuario["Desempenho"].append(pontuacao)

    # Salva os dados atualizados no JSON
    salvar_dados(usuarios_cadastrados, chave_secreta)

    print("Pontuação registrada com sucesso.")

# Função para Perguntas


def questionario_entrada_saida(usuario, usuarios_cadastrados, chave_secreta):
    print("\nAgora vamos para o formulário de 'Entrada e saída'. Responda com 'a', 'b' ou 'c'.\n")
# Perguntas de Entrada e Saída
    perguntas = [
        {"pergunta": "1. O que é a função 'input'?", "a": "Lê dados da entrada do usuário",
         "b": "Exibe informações na tela", "c": "Cria uma variável"},
        {"pergunta": "2. O que faz a função 'print'?", "a": "Exibe dados na tela", "b": "Lê dados da entrada",
         "c": "Calcula uma operação"},
        {"pergunta": "3. Como se lê um número inteiro usando 'input'?", "a": "input()", "b": "int(input())",
         "c": "float(input())"},
        {"pergunta": "4. Qual comando é usado para ler uma linha inteira de texto?", "a": "input()", "b": "print()",
         "c": "read()"},
        {"pergunta": "5. Como converter um valor para string?",
            "a": "str()", "b": "float()", "c": "int()"}
    ]
    # Respostas corretas
    respostas_corretas = ["a", "a", "b", "a", "a"]
    respostas_usuario = []
    pontuacao = 0  # Inicializa a pontuação do usuário

    for i, pergunta in enumerate(perguntas):
        print(pergunta["pergunta"])
        print("a) " + pergunta["a"])
        print("b) " + pergunta["b"])
        print("c) " + pergunta["c"])

        resposta = input("Escolha a opção (a, b ou c): ").lower()
        while resposta not in ["a", "b", "c"]:
            print("Resposta inválida! Por favor, escolha 'a', 'b' ou 'c'.")
            resposta = input("Escolha a opção (a, b ou c): ").lower()

        respostas_usuario.append(resposta)

        # Verifica se a resposta está correta
        if resposta == respostas_corretas[i]:
            pontuacao += 1

    print(
        f"\nSua pontuação no questionário de entrada e saída: {pontuacao}/{len(perguntas)}")

    # Adiciona a pontuação ao desempenho do usuário
    usuario["Desempenho"].append(pontuacao)

    # Salva os dados atualizados no JSON
    salvar_dados(usuarios_cadastrados, chave_secreta)

    print("Pontuação registrada com sucesso.")


# Função para questionário de Programação em Python

def escolher_disciplina(usuario, usuarios_cadastrados, chave_secreta):
    while True:
        print("\nEscolha uma disciplina:")
        print("1 - Estrutura de controle")
        print("2 - Entrada e saída")
        print("3 - Funções")
        print("4 - Lógica em Python")
        print("0 - Sair")

        escolha = input("Digite o número da disciplina escolhida: ").strip()

        if escolha == "1":
            print("Você escolheu Estrutura de controle.")
            questionario_estrutura(
                usuario, usuarios_cadastrados, chave_secreta)
        elif escolha == "2":
            print("Você escolheu Entrada e saída.")
            questionario_entrada_saida(
                usuario, usuarios_cadastrados, chave_secreta)
        elif escolha == "3":
            print("Você escolheu Funções.")
            questionario_funcoes(usuario, usuarios_cadastrados, chave_secreta)
        elif escolha == "4":
            print("Você escolheu Lógica em Python.")
            questionario_logica(usuario, usuarios_cadastrados, chave_secreta)
        elif escolha == "0":
            print("Saindo da escolha de disciplinas.")
            break
        else:
            print("Opção inválida! Tente novamente.")

# Função principal para controlar o sistema


def main():
    usuarios_cadastrados, chave_secreta = carregar_dados()
    fernet = Fernet(chave_secreta)
    while True:
        print("\n========== Menu ==========")
        print("1 - Login")
        print("2 - Cadastro")
        print("3 - Consultar/Alterar Dados")
        print("4 - Inserir Desempenho")
        print("5 - Calcular Média de Idades")
        print("6 - Calcular Média de Notas")
        print("0 - Sair")
        acao = input("Escolha uma opção: ").strip()

        if acao == "1":
            usuario = login(usuarios_cadastrados, fernet)
            if usuario:
                escolher_disciplina(
                    usuario, usuarios_cadastrados, chave_secreta)
        elif acao == "2":
            cadastrar_usuario(usuarios_cadastrados, fernet, chave_secreta)
        elif acao == "3":
            consultar_alterar_usuario(usuarios_cadastrados, chave_secreta)
        elif acao == "4":
            inserir_desempenho(usuarios_cadastrados, chave_secreta)
        elif acao == "5":
            calcular_media_idades(usuarios_cadastrados)
        elif acao == "6":
            calcular_media_notas(usuarios_cadastrados)
        elif acao == "0":
            print("Saindo...")
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()
