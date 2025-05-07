# Importando as bibliotecas json e Fernet para criptografia
import json
from cryptography.fernet import Fernet

# Função para salvar os dados no arquivo JSON
def salvar_dados(dados, chave_secreta):
    salvar_dados = {
        "usuarios": dados,
        "chave_secreta": chave_secreta.decode()  # Converto a chave de bytes para string (base64) para poder salvar no JSON
    }
    with open("usuarios.json", "w") as arquivo:  # Abro o arquivo no modo de escrita ("w")
        json.dump(salvar_dados, arquivo, indent=4)  # Salvo os dados no JSON com indentação para melhor leitura


# Função para carregar os dados do arquivo JSON
def carregar_dados():
    try:
        # Tenta abrir o arquivo no modo de leitura ("r")
        with open("usuarios.json", "r") as arquivo:
            dados = json.load(arquivo)  # Carrega os dados do JSON como dicionário    
            if "usuarios" in dados and "chave_secreta" in dados: # Verifica se as chaves esperadas estão presentes
                chave_secreta = dados["chave_secreta"].encode()  # Converte a chave de string base64 para bytes
                return dados["usuarios"], chave_secreta  # Retorna os usuários e a chave
            else:
                # Se o formato do JSON estiver incorreto, levanta um erro
                raise ValueError("Estrutura do arquivo inválida")
    # Se o arquivo não existir, estiver corrompido ou com estrutura errada
    except (FileNotFoundError, json.JSONDecodeError, ValueError):
        chave_secreta = Fernet.generate_key()  # Gera nova chave de criptografia (em bytes)
        return [], chave_secreta  # Retorna lista vazia de usuários e a nova chave
# Correção ! As linhas 24, 26, 28, 29 e 30 foram criadas com o intuito de prosseguir caso o Json esteja em branco,
# mas se o caso for outro irá apagar todos os dados sem nenhum tipo de backup

# Função para validar a senha   
def validar_senha(senha):
    return len(senha) >= 6 and any(char.isupper() for char in senha) and any(char.isdigit() for char in senha)


# Função para validar email
def validar_email(email):
    return "@" in email and ".com" in email


# Função para calcular média de idade dos usuários
def calcular_media_idades(usuarios):
    if not usuarios: # Caso não tenha nenhum usuário cadastrado
        print("") # Espaço pra ficar bonito 
        print("Nenhum usuário cadastrado para calcular a média.")
        return # Cancela o processo da função
    print("========== Média das idades ==========")
    print("\nLista de usuários cadastrados:")
    for usuario in usuarios: # Para cada usuário na lista do Json
        print(f"- {usuario['Email']}") #Imprima o Email de cada um

    soma_idades = sum(usuario["Idade"] for usuario in usuarios) # Soma as idades de todos os usuários
    media_idades = soma_idades / len(usuarios) # Utiliza a soma e divide pela quantidade de usuários 
    print(f"\nTotal de usuários cadastrados: {len(usuarios)}") 
    print(f"Soma das idades: {soma_idades}")
    print(f"Média das idades: {media_idades:.2f}")
    print("======================================")  # Espaço pra ficar bonito


# Função para calcular a média das notas de desempenho e listar logins
def calcular_media_notas(usuarios):
    if not usuarios: # Se não houver usuário registrado
        print("Nenhum usuário cadastrado para calcular a média de notas.")
        return # Cancela o processo da função 
    print("========== Média das notas ==========")
    print("\nLista de usuários cadastrados:")
    for usuario in usuarios: # Para cada usuário na lista do Json
        print(f"- {usuario['Email']}") #Imprima o Email de cada um

    total_notas = 0 # Variável local para o total das notas
    qtd_notas = 0 # "" "" "" a quantidade das notas
    usuarios_com_notas = 0 # Quantidade de usuários com notas

    for usuario in usuarios:
        if usuario["Desempenho"]:  # Verifica se há notas registradas
            total_notas += sum(usuario["Desempenho"]) # Soma todas as notas
            qtd_notas += len(usuario["Desempenho"]) # Quantidade de notas na lista do Json
            usuarios_com_notas += 1 # Soma +1 pra cada usuário encontrado na lista

    if qtd_notas > 0: # Se a quantidade das notas for maior que 0
        media_notas = total_notas / qtd_notas # A soma das notas dividido pelo total de notas
        print(f"\nTotal de usuários com notas: {usuarios_com_notas}")
        print(f"Total de notas registradas: {qtd_notas}")
        print(f"Soma de todas as notas: {total_notas:.2f}") # :.2f Significa limitar o float a duas casas decimais
        print(f"Média geral das notas: {media_notas:.2f}")
        print("=====================================") # Pra ficar bonito tb. Confia
    else:
        print("\nNenhuma nota de desempenho registrada.") 
        print("=====================================")


# Função para consultar e alterar os dados do usuário
def consultar_alterar_usuario(usuarios, chave_secreta): # Parâmetros que servem para buscar os usuarios e salvar a senha criptografada
    print("============ Consulte ou altere dados ============")
    email = input("Digite o e-mail do usuário: ").strip() 

    for usuario in usuarios:
        if usuario["Email"] == email: # Se o E-mail digitado for igual a qualquer um que esteja registrado
            print(f"\nNome: {usuario['Nome']}") 
            print(f"Idade: {usuario['Idade']}")
            print(f"E-mail: {usuario['Email']}")
            print(f"Tipo de usuário: {usuario['Tipo']}")
            print(f"Nível de conhecimento: {usuario['Nivel De Conhecimento']}")
            print(f"Desempenho: {usuario['Desempenho']}\n")
            # A função strip() é usada para remover espaços em branco extras. lower() transforma todos os caracteres da string em minúsculas.
            acao = input("Deseja alterar os dados? (s/n): ").strip().lower() 
            if acao == "s":
                novo_nome = input(f"Nome atual: {usuario['Nome']}. Digite o novo nome: ").strip() # Salvar o novo nome na váriavel
                while True:
                    novo_email = input(f"E-mail atual: {usuario['Email']}. Digite o novo e-mail: ").strip() # Salvar o novo e-mail na váriavel
                    if not validar_email(novo_email):
                        print("Erro: O e-mail deve conter '@' e '.com'.")
                        continue # Se o e-mail estiver correto, segue o baile
                    elif any(user["Email"] == novo_email and user != usuario for user in usuarios): 
                    # any(...) retorna True se alguma condição dentro da expressão for verdadeira.
                    # "user" representa cada dicionário (usuário) da lista "usuarios". É uma variável temporária usada apenas nessa verificação.
                    # user["Email"] == novo_email → Verifica se o e-mail do usuário atual é igual ao novo e-mail digitado.
                    # user != usuario → Garante que o usuário sendo comparado não é o mesmo que está sendo editado.
                    # Ou seja: se existir outro usuário com o mesmo e-mail, impede a duplicação.
                    # "!=" significa "diferente de".
                        print("Erro: E-mail já cadastrado.")
                        continue # Se o e-mail não existir ou for igual ao usuário atual, segue o baile
                    break # Encerra o código

                try: # Tente inserir uma nova idade 
                    nova_idade = int(input(f"Idade atual: {usuario['Idade']}. Digite a nova idade: "))
                except ValueError: # Erro ao digitar algo que não seja um número inteiro
                    print("Erro: Idade inválida. Digite um número inteiro.")
                    return # Correção ! Deveria tentar digitar a idade novamente, e não encerrar a função

                novo_nivel = input(f"Nível atual: {usuario['Nivel De Conhecimento']}. Digite o novo nível: ").strip() # Correção ! É possível digitar um nível inválido

                # Atualizando os dados
                usuario["Nome"] = novo_nome
                usuario["Email"] = novo_email
                usuario["Idade"] = nova_idade
                usuario["Nivel De Conhecimento"] = novo_nivel

                salvar_dados(usuarios, chave_secreta)
                print("Dados atualizados com sucesso.")
            return
    
    print("Usuário não encontrado.") # Correção ! Digitar o e-mail novamente e não encerrar a função



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
        print("\n========== Bem-vindo! ==========")
        print("1 - Login")
        print("2 - Cadastro")
        acao = input("Escolha uma opção: ").strip()

        if acao == "1":
            usuario = login(usuarios_cadastrados, fernet)
            if usuario:
                menu(usuario, usuarios_cadastrados, chave_secreta)
        elif acao == "2":
            cadastrar_usuario(usuarios_cadastrados, chave_secreta, fernet)


def menu(usuario, usuarios_cadastrados, chave_secreta):
    while True:
        print("1 - Questionários")
        print("3 - Consultar/Alterar Dados")
        print("4 - Inserir Desempenho")
        print("5 - Calcular Média de Idades")
        print("6 - Calcular Média de Notas")
        print("0 - Sair")
        acao = input("Escolha uma opção: ").strip()

        if acao == "1":
            escolher_disciplina(usuario, usuarios_cadastrados, chave_secreta)
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
