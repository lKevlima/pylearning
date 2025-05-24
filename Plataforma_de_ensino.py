# Biblioteca padrão para cálculos estatísticos (média, moda, mediana)
import statistics
# Biblietocas json e Fernet para criptografia
import json
from cryptography.fernet import Fernet

# Função para salvar os dados no arquivo JSON


def salvar_chave(chave_secreta, caminho="chave.key"):
    with open(caminho, 'wb') as chave_arquivo:
        chave_arquivo.write(chave_secreta)


def carregar_chave(caminho="chave.key"):
    try:
        with open(caminho, "rb") as chave_arquivo:
            return chave_arquivo.read()
    except FileNotFoundError:
        # Gera uma nova chave se não existir
        nova_chave = Fernet.generate_key()
        salvar_chave(nova_chave, caminho)
        return nova_chave


def salvar_dados(dados):
    salvar_dados = {
        "usuarios": dados,
    }
    # Abro o arquivo no modo de escrita ("w")
    with open("usuarios.json", "w", encoding="utf-8") as arquivo:
        # Salvo os dados no JSON com indentação para melhor leitura
        json.dump(salvar_dados, arquivo, indent=4, ensure_ascii=False)


def carregar_dados():
    try:
        with open("usuarios.json", "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
            if "usuarios" in dados:
                return dados["usuarios"]
            else:
                return []  # Retorna lista vazia se a chave não existir
    except FileNotFoundError:
        # Cria o arquivo se não existir
        salvar_dados([])  # Cria com lista vazia
        return []


# Função para validar a senha
def validar_senha(senha):
    return len(senha) >= 6 and any(char.isupper() for char in senha) and any(char.isdigit() for char in senha)


# Função para validar email
def validar_email(email):
    return "@" in email and ".com" in email


# Função para calcular média de idade dos usuários


def calcular_estatisticas_idades(usuarios):
    if not usuarios:  # Verifica se a lista de usuários está vazia
        print("")  # Imprime uma linha em branco para formatação visual
        print("Nenhum usuário cadastrado para calcular.")  # Mensagem de aviso
        return  # Encerra a função, pois não há dados para processar

    print("========== Estatísticas das idades ==========")
    print("\nLista de usuários cadastrados:")
    for usuario in usuarios:  # Percorre cada dicionário de usuário na lista
        print(f"- {usuario['Email']}")  # Imprime o e-mail de cada usuário

    # Cria uma lista com as idades de todos os usuários
    idades = [usuario["Idade"] for usuario in usuarios]

    # Soma todas as idades (para fins de exibição)
    soma_idades = sum(idades)

    # Calcula a média das idades
    media_idades = statistics.mean(idades)

    # Calcula a mediana (valor central quando a lista está ordenada)
    mediana_idades = statistics.median(idades)

    # Calcula a moda (idade que mais aparece na lista)
    try:
        moda_idades = statistics.mode(idades)
    except statistics.StatisticsError:
        # Caso não haja moda
        moda_idades = "Não existe moda (todos os valores são únicos)"

    # Exibe os resultados no terminal formatado
    print(f"\nTotal de usuários cadastrados: {len(usuarios)}")
    print(f"Soma das idades: {soma_idades}")
    print(f"Média das idades: {media_idades:.2f}")
    print(f"Mediana das idades: {mediana_idades}")
    print(f"Moda das idades: {moda_idades}")
    print("=============================================")


# Função para calcular a média das notas de desempenho e listar logins


def calcular_estatisticas_notas(usuarios):
    if not usuarios:
        print("Nenhum usuário cadastrado para calcular.")
        return

    print("========== Estatísticas das Notas ==========")
    print("\nLista de usuários cadastrados:")
    for usuario in usuarios:
        print(f"- {usuario['Email']}")

    todas_notas = []
    usuarios_com_notas = 0

    for usuario in usuarios:
        if usuario["Desempenho"]:  # Verifica se há notas
            todas_notas.extend(usuario["Desempenho"])  # Junta todas as notas
            usuarios_com_notas += 1

    if todas_notas:
        media = sum(todas_notas) / len(todas_notas)
        mediana = statistics.median(todas_notas)

        try:
            moda = statistics.mode(todas_notas)
        except statistics.StatisticsError:
            moda = "Sem moda (valores igualmente frequentes)"

        print(f"\nTotal de usuários com notas: {usuarios_com_notas}")
        print(f"Total de notas registradas: {len(todas_notas)}")
        print(f"Soma de todas as notas: {sum(todas_notas):.2f}")
        print(f"Média das notas: {media:.2f}")
        print(f"Mediana das notas: {mediana}")
        print(f"Moda das notas: {moda}")
        print("===========================================")

        # Se quiser gerar gráfico, os dados estão prontos em todas_notas
    else:
        print("\nNenhuma nota de desempenho registrada.")
        print("===========================================")


# Função para consultar e alterar os dados do usuário
# Parâmetros que servem para buscar os usuarios e salvar a senha criptografada
# Função para consultar e alterar os dados de um usuário
# Parâmetro: usuarios_cadastrados → lista contendo os dados de todos os usuários
def consultar_alterar_usuario(usuarios_cadastrados):
    print("============ Consulte ou altere dados ============")

    while True:
        email = input("Digite o e-mail do usuário: ").strip()

        # Percorre a lista de usuários para encontrar o e-mail informado
        for usuario in usuarios_cadastrados:
            if usuario["Email"] == email:
                # Exibe os dados atuais do usuário
                print(f"\nNome: {usuario['Nome']}")
                print(f"Idade: {usuario['Idade']}")
                print(f"E-mail: {usuario['Email']}")
                print(f"Tipo de usuário: {usuario['Tipo']}")
                print(f"Nível de conhecimento: {usuario['Nivel De Conhecimento']}")
                print(f"Desempenho: {usuario['Desempenho']}\n")

                acao = input("Deseja alterar os dados? (s/n): ").strip().lower()

                if acao == "s":
                    # Alteração de nome
                    novo_nome = input(
                        f"Nome atual: {usuario['Nome']}. Digite o novo nome: ").strip()

                    # Alteração de e-mail, com verificação de formato e duplicidade
                    while True:
                        novo_email = input(
                            f"E-mail atual: {usuario['Email']}. Digite o novo e-mail: ").strip()

                        if not validar_email(novo_email):
                            print("Erro: O e-mail deve conter '@' e '.com'.")
                            continue

                        # Verifica se já existe outro usuário com o mesmo e-mail
                        # any() retorna True se alguma condição dentro dela for verdadeira
                        # Verifica se:
                        # 1. Existe algum usuário com e-mail igual ao novo_email
                        # 2. Esse usuário não é o próprio que está sendo editado
                        if any(user["Email"] == novo_email and user != usuario for user in usuarios_cadastrados):
                            print("Erro: E-mail já cadastrado.")
                            continue

                        break  # E-mail válido e não duplicado

                    # Alteração de idade, garante que o valor seja um número inteiro
                    while True:
                        try:
                            nova_idade = int(
                                input(f"Idade atual: {usuario['Idade']}. Digite a nova idade: "))
                            break
                        except ValueError:
                            print("Erro: Idade inválida. Digite um número inteiro.")

                    # Alteração do nível de conhecimento, com validação
                    niveis = {
                        "1": "Iniciante",
                        "2": "Intermediário",
                        "3": "Avançado"
                    }

                    while True:
                        escolha_nivel = input(
                            f"Nível atual: {usuario['Nivel De Conhecimento']}. "
                            "Digite o novo nível ((1) - Iniciante, (2) - Intermediário ou (3) - Avançado): "
                        ).strip()

                        if escolha_nivel in niveis:
                            novo_nivel = niveis[escolha_nivel]
                            break
                        else:
                            print("Erro: Escolha inválida. Selecione (1), (2) ou (3).")

                    # Atualiza os dados do usuário
                    usuario["Nome"] = novo_nome
                    usuario["Email"] = novo_email
                    usuario["Idade"] = nova_idade
                    usuario["Nivel De Conhecimento"] = novo_nivel

                    # Salva todos os dados atualizados no arquivo
                    salvar_dados(usuarios_cadastrados)

                    print("Dados atualizados com sucesso.")
                return  # Encerra a função após concluir a alteração ou não querer alterar

        # Se o e-mail não for encontrado, informa e permite tentar novamente
        print("Usuário não encontrado. Tente novamente.")



# Função para inserir os dados de desempenho do usuário
# Mudança ! Fazer essa função aparecer no menu apenas para os usuários administradores, assim não precisa do e-mail de verificação
def inserir_desempenho(usuarios):
    print("============ Inserir desempenho ============")
    # Solicita o e-mail de quem está tentando acessar a função
    email_admin = input("Digite seu e-mail para autenticação: ").strip()
    # Busca o usuário correspondente ao e-mail informado
    usuario_admin = next(  # O next() retorna o primeiro usuário que atende essa condição.
        (user for user in usuarios if user["Email"] == email_admin), None)

    # Verifica se o usuário existe e se é um administrador
    # O not inverte o valor booleano
    if not usuario_admin or usuario_admin["Tipo"] != "Administrador":
        print("Acesso negado! Apenas administradores podem alterar o desempenho.")
        return  # Interrompe a função se não for administrador

    # Solicita o e-mail do usuário que terá o desempenho registrado
    email = input(
        "Digite o e-mail do usuário para inserir um desempenho: ").strip()

    # Percorre a lista de usuários
    for usuario in usuarios:
        # Se encontrar o e-mail correspondente
        if usuario["Email"] == email:
            # Recupera as notas já existentes
            desempenho = usuario["Desempenho"]

            # Loop para inserir múltiplas notas
            while True:
                try:
                    nota = float(
                        input("Digite a pontuação de desempenho (digite -1 para terminar): "))
                    if nota == -1:
                        break  # Encerra o loop se o usuário digitar -1
                    desempenho.append(nota)  # Adiciona a nota à lista
                except ValueError:  # Se a entrada não for um número, aparece a mensagem de erro
                    print("Entrada inválida. Por favor, insira um número.")

            # Atualiza o campo "Desempenho" do usuário
            usuario["Desempenho"] = desempenho

            # Salva os dados atualizados no arquivo
            # Aprendizado ! Entender melhor sobre os pârametros, pq as diferenças de nomemclaturas pra mesma função?
            salvar_dados(usuarios)

            print("============ Desempenho registrado com sucesso! ============")
            return  # Encerra a função após salvar

    # Se o e-mail do usuário não for encontrado
    # Correção ! Digitar o e-mail novamente e não encerrar a função
    print("Usuário não encontrado.")


# Função para questionários de Programação em Python
def escolher_disciplina(usuario, usuarios_cadastrados):
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
                usuario, usuarios_cadastrados)
        elif escolha == "2":
            print("Você escolheu Entrada e saída.")
            questionario_entrada_saida(
                usuario, usuarios_cadastrados)
        elif escolha == "3":
            print("Você escolheu Funções.")
            questionario_funcoes(usuario, usuarios_cadastrados)
        elif escolha == "4":
            print("Você escolheu Lógica em Python.")
            questionario_logica(usuario, usuarios_cadastrados)
        elif escolha == "0":
            print("Saindo da escolha de disciplinas.")
            break
        else:
            print("Opção inválida! Tente novamente.")


# Função para perguntas de lógica
def questionario_logica(usuario, usuarios_cadastrados):
    print("\n========== Questionário de Lógica de Programação ==========\n")
    print("\nResponda com 'a', 'b' ou 'c'.\n")
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
    salvar_dados(usuarios_cadastrados)

    print("Pontuação registrada com sucesso.")


# Função para perguntas de estrutura
def questionario_estrutura(usuario, usuarios_cadastrados):
    print("\n========== Questionário de Programação em Python ==========\n")
    print("\nResponda com 'a', 'b' ou 'c'.\n")
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
    salvar_dados(usuarios_cadastrados)

    print("Pontuação registrada com sucesso.")


# Função para perguntas de funções
def questionario_funcoes(usuario, usuarios_cadastrados):
    print("\nAgora vamos para o formulário de 'Entrada e saída'. Responda com 'a', 'b' ou 'c'.\n")
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
    salvar_dados(usuarios_cadastrados)

    print("Pontuação registrada com sucesso.")


# Função para perguntas de entrada e saída
def questionario_entrada_saida(usuario, usuarios_cadastrados):
    print("\nAgora vamos para o formulário de 'Entrada e saída'. Responda com 'a', 'b' ou 'c'.\n")
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
    salvar_dados(usuarios_cadastrados)

    print("Pontuação registrada com sucesso.")


# Função para cadastrar o usuário
# A ordem dos parâmetros de uma função devem estar iguais em todo o código.
# Função para cadastrar o usuário
# A ordem dos parâmetros da função deve ser mantida igual em todo o código.
def cadastrar_usuario(usuarios_cadastrados, fernet):
    # Atenção: A ordem estava trocada antes ("fernet, chave_secreta"), o que fazia receber os valores incorretos.

    # Termo de Consentimento LGPD
    print("Este sistema coleta seus dados pessoais (nome, idade, e-mail, desempenho e nível de conhecimento).")
    print("Eles serão utilizados apenas para fins acadêmicos e estatísticos dentro da plataforma.")
    consentimento = input("Você aceita os termos de uso dos seus dados? (s/n): ").strip().lower()

    if consentimento != "s":
        print("Cadastro cancelado. Você não aceitou os termos.")
        return  # Encerra a função caso o usuário não aceite

    # Coleta do nome do usuário
    nome = input("Digite seu nome: ")

    # Coleta da idade
    idade = int(input("Digite sua idade: "))

    # Dicionário para mapear o nível de conhecimento
    niveis = {
        "1": "Iniciante",
        "2": "Intermediário",
        "3": "Avançado"
    }

    # Loop para garantir uma escolha válida para o nível de conhecimento
    while True:
        escolha = input(
            "Digite seu nível de conhecimento ((1) - Iniciante, (2) - Intermediário ou (3) - Avançado): "
        ).strip()

        if escolha not in niveis:
            print("Resposta inválida. Escolha entre (1), (2) ou (3).")
        else:
            nivel_conhecimento = niveis[escolha]
            break

    # Loop para garantir que o e-mail seja válido e não esteja cadastrado
    while True:
        email = input("Digite seu e-mail: ").strip()

        if not validar_email(email):
            # Verifica se o e-mail possui '@' e '.com' para ser considerado válido
            print("Erro: O e-mail deve conter '@' e '.com'.")
        elif any(user["Email"] == email for user in usuarios_cadastrados):
            # any(...) retorna True se algum usuário já possui o e-mail informado
            print("Erro: E-mail já cadastrado.")
        else:
            break  # E-mail válido e único → sai do loop

    # Loop para definir uma senha forte e criptografá-la
    while True:
        senha = input(
            "Digite uma senha (mínimo 6 caracteres, com pelo menos 1 maiúscula e 1 número): "
        )

        if validar_senha(senha):
            # Criptografa a senha:
            # - Primeiro converte a string em bytes com .encode()
            # - Depois criptografa usando Fernet
            # - Por fim, transforma de volta para string com .decode() (JSON não aceita bytes)
            senha_criptografada = fernet.encrypt(senha.encode()).decode()
            break
        else:
            print(
                "Erro: Senha fraca. Deve ter no mínimo 6 caracteres, com pelo menos 1 letra maiúscula e 1 número."
            )

    # Define o tipo de usuário: Administrador ou Comum
    tipo_usuario = input(
        "Digite o tipo de usuário (Administrador ou Comum): "
    ).strip().capitalize()

    # Caso o tipo informado seja inválido, define como 'Comum' por padrão
    if tipo_usuario not in ["Administrador", "Comum"]:
        tipo_usuario = "Comum"

    # Cria o dicionário do usuário com todos os dados coletados
    usuario = {
        "Nome": nome,
        "Email": email,
        "Idade": idade,
        "Nivel De Conhecimento": nivel_conhecimento,
        "Senha": senha_criptografada,  # Senha armazenada de forma segura
        "Tipo": tipo_usuario,
        "Desempenho": []  # Lista vazia para armazenar futuras pontuações
    }

    # Adiciona o usuário recém-cadastrado na lista de usuários
    usuarios_cadastrados.append(usuario)

    # Salva os dados atualizados no arquivo
    salvar_dados(usuarios_cadastrados)

    # Mensagem final confirmando o sucesso do cadastro
    print(f"Cadastro realizado com sucesso! Bem-vindo(a), {nome}!")


# Função para autenticação de login
def login(usuarios_cadastrados, fernet):
    # 'fernet' é o objeto usado para descriptografar a senha armazenada

    # Solicita o e-mail e remove espaços extras
    email = input("Digite seu e-mail: ").strip()
    # Solicita a senha e remove espaços extras
    senha = input("Digite sua senha: ").strip()

    # Percorre cada usuário cadastrado na lista
    for usuario in usuarios_cadastrados:
        if usuario["Email"] == email:  # Verifica se o e-mail informado existe
            # Pega a senha criptografada do usuário
            senha_criptografada = usuario["Senha"]
            senha_descriptografada = fernet.decrypt(
                senha_criptografada.encode()).decode()  # Descriptografa a senha

            if senha == senha_descriptografada:  # Verifica se a senha digitada está correta
                print("Entrada bem-sucedida!")
                print(f"Nome: {usuario['Nome']}")
                print(f"Idade: {usuario['Idade']}")
                print(f"Tipo de usuário: {usuario['Tipo']}")
                print(f"E-mail: {usuario['Email']}")
                print(
                    f"Nivel De Conhecimento: {usuario['Nivel De Conhecimento']}")
                print(f"Desempenho: {usuario['Desempenho']}")
                print("=====================================")
                return usuario  # Retorna o dicionário do usuário logado
            else:
                # Senha digitada não bate com a senha armazenada
                print("Senha incorreta!")
                return None

    # Nenhum usuário com o e-mail informado foi encontrado
    print("Email não cadastrado.")
    return None  # Retorna None se o login falhar

def excluir_conta(usuario, usuarios_cadastrados):
    confirmacao = input("Tem certeza que deseja excluir sua conta? Seus dados serão apagados permanentemente. (s/n): ").strip().lower()
    if confirmacao == "s":
        usuarios_cadastrados.remove(usuario)
        salvar_dados(usuarios_cadastrados)
        print("Sua conta foi excluída com sucesso.")
        return True  # Indica que a conta foi excluída
    else:
        print("Exclusão cancelada.")
        return False  # Conta não foi excluída
     

# Função principal para controlar o sistema
def main():
    # Carrega os dados dos usuários e a chave secreta do arquivo JSON
    usuarios_cadastrados = carregar_dados()
    chave_secreta = carregar_chave()

    # Cria uma instância do Fernet com a chave secreta para criptografia e descriptografia
    fernet = Fernet(chave_secreta)

    # Loop principal do programa (menu inicial)
    while True:
        print("\n========== Bem-vindo! ==========")
        print("1 - Entrar")
        print("2 - Cadastro")

        # Pede ao usuário para escolher entre fazer login ou se cadastrar
        acao = input("Escolha uma opção: ").strip()

        # Se o usuário escolher "1", inicia o processo de login
        if acao == "1":
            # Tenta fazer o login com os usuários cadastrados e a ferramenta de descriptografia
            usuario = login(usuarios_cadastrados, fernet)
            # Se o login for bem-sucedido (usuário válido), abre o menu do sistema
            if usuario:
                menu(usuario, usuarios_cadastrados)

        # Se o usuário escolher "2", inicia o processo de cadastro de novo usuário
        elif acao == "2":
            cadastrar_usuario(usuarios_cadastrados, fernet)

# Função que exibe o menu principal após o login e executa ações conforme a escolha do usuário
def menu(usuario, usuarios_cadastrados):
    while True:
        # Exibe as opções disponíveis no menu
        print("1 - Questionários")
        print("2 - Consultar/Alterar Dados")
        print("3 - Inserir Desempenho")
        print("4 - Calcular as Estátisticas das Idades")
        print("5 - Calcular as Estátisticas das Notas")
        print("6 - Excluir Minha Conta")
        print("0 - Sair")

        # Recebe a escolha do usuário
        acao = input("Escolha uma opção: ").strip()

        # Opção 1: Acessa a parte de questionários, passando os dados necessários
        if acao == "1":
            escolher_disciplina(usuario, usuarios_cadastrados)

        # Opção 3: Permite consultar ou alterar dados de usuários
        elif acao == "2":
            consultar_alterar_usuario(usuarios_cadastrados)

        # Opção 4: Permite inserir dados de desempenho dos usuários
        elif acao == "3":
            inserir_desempenho(usuarios_cadastrados)

        # Opção 5: Calcula e exibe a média das idades cadastradas
        elif acao == "4":
            calcular_estatisticas_idades(usuarios_cadastrados)

        # Opção 6: Calcula e exibe a média das notas dos usuários
        elif acao == "5":
            calcular_estatisticas_notas(usuarios_cadastrados)
        
        elif acao == "6":
             if excluir_conta(usuario, usuarios_cadastrados):
                break  # Sai do menu após excluir a conta

        # Opção 0: Encerra o menu e retorna ao menu principal (ou finaliza o programa)
        elif acao == "0":
            print("Saindo...")
            break

        # Qualquer outra opção: mensagem de erro
        else:
            print("Opção inválida.")


# Verifica se este arquivo está sendo executado diretamente
# Se sim, chama a função principal que inicia o sistema
if __name__ == "__main__":
    main()


# Mudanças ! Incluir anonimato. Guardar com mais segurança a chave_secreta. Implementar mais algum tipo de interação educativa com o úsuario.
# No readme.me incluir passo a passo para utilizar o programa, inclusive a instalação das bibliotecas (criptography and dotenv)
