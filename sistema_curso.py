'''Programa de CRUD de um sistema de cursos online'''

import mysql.connector
import pandas as pd #biblioteca para tratamento de dados

def conectar(): #Função para conectar no BD
    conexao = mysql.connector.connect(user='root',              
                                    password='MY@sql12345678',       
                                    host='localhost',        
                                    database='curso')
    return conexao
def chose_user(texto): #Função para escolha de interação: Aluno ou Professor
    print ('\n')
    print (texto)
    print ('1- Aluno')
    print ('2- Professor')
    escolha_usuario = int(input('Opção: '))

    return escolha_usuario
def read(conexao, escolha_usuario): #Função para visualização de dados do BD
    cursor = conexao.cursor()

    #Verifica o tipo de usuario (1- Aluno | 2- Professor) e guarda o codigo SQL em uma variavel para visualização dos dados
    if escolha_usuario == 1:
        sql = '''SELECT 
        a.id_aluno, a.nome_aluno, a.sobrenome_aluno, a.telefone, a.nascimento, a.email, a.genero, b.nome_curso
        FROM
        tb_curso b
            JOIN
        ta_curso_aluno c on c.tb_curso_id_curso = b.id_curso
            JOIN
        tb_aluno a on a.id_aluno = c.td_aluno_id_aluno
            
        order by a.nome_aluno;'''
    else:
        sql = '''SELECT 
        a.id_prof, a.nome_prof, a.sobrenome_prof, a.telefone_prof, a.salario, a.nascimento, a.email, a.genero, b.nome_curso
        FROM
        tb_curso b
            JOIN
        ta_professor_curso c on c.tb_curso_id_curso = b.id_curso
            JOIN
        tb_professor a on a.id_prof = c.tb_professor_id_prof
            
        order by a.nome_prof;'''

    #Executa o codigo SQL e coloca os dados na variavel "registros"
    cursor.execute(sql)
    registros = cursor.fetchall()

    #Visualização organizada dos dados dentro da variavel "registro" (uso do Pandas)
    if escolha_usuario == 1:
        colunas = ['Id','Nome','Sobrenome', 'Telefone', 'Data de Nascimento', 'E-mail', 'Genero', 'Curso']
    else:
        colunas = ['Id','Nome','Sobrenome', 'Telefone', 'Salario' ,'Data de Nascimento', 'E-mail', 'Genero', 'Curso']
    dados = pd.DataFrame(registros, columns=colunas)
    for a in range(len(dados)): #Loop para organizar a coluna de cursos
        try:
            if dados['Id'][a+1] == dados['Id'][a]:
                dados['Curso'][a+1] =  dados['Curso'][a] + ', ' + dados['Curso'][a+1]
                dados['Curso'][a] = 'Nan'          
        except:
            continue
    dados.query('Curso != "Nan"', inplace=True)
    dados['Genero'].fillna('Não Fornecido', inplace=True)

    print (dados) #Mostra os dados

    cursor.close() #fecha o cursor
def insert(conexao, escolha_usuario): #Função para inserir dados no BD

    #Armazena os cursos existentes na variavel "registros"
    sql1 = '''select id_curso ,nome_curso from tb_curso '''
    cursor = conexao.cursor() #abre o cursor
    cursor.execute(sql1)
    registros = cursor.fetchall()

    #codigos SQL para inserção dos dados
        ##Inserção nas tabelas basicas
    sql2_aluno = '''insert into tb_aluno (id_aluno, nome_aluno, sobrenome_aluno, telefone, nascimento, email, genero)
     value (%s,%s,%s,%s,%s,%s,%s)'''
    sql3_professor = '''insert into tb_professor (id_prof, nome_prof, sobrenome_prof, telefone_prof, salario, email, genero, nascimento)
     value (%s,%s,%s,%s,%s,%s,%s,%s)'''

        ##Inserção nas tabelas associativas
    sql4_ass_aluno = '''insert into ta_curso_aluno value (%s,%s)'''
    sql5_ass_professor = '''insert into ta_professor_curso value (%s,%s)'''

    #verifica o tipo de usuario (1- Aluno | 2- Professor) e faz a inserção dos dados
    if escolha_usuario == 1:

        #recebimento dos dados
        nome = str(input('Insira o nome do aluno: '))
        sobrenome = str(input('Insira o sobrenome: '))
        telefone = str(input('Insira o telefone: '))
        dia = int(input('Insira o dia do nascimento: '))
        mes = int(input('Insira o mes do nascimento: '))
        ano = int(input('Insira o ano do nascimento: '))
        nascimento = f'{ano}-{mes}-{dia}'
        email = str(input('Insira o email: '))
        genero = str(input('Insira o genero (M- masculino | F- Feminino): '))
        genero = genero.upper() #Coloca em letra maiuscula o genero inserido

        print ('\n')
        for a in registros: #mostra os cursos existentes para o usuario poder escolher
            print (f'{a[0]}- {a[1]}')                 
        print('\n')
        curso = int(input('Insira o curso: '))
        
        #Inserir o Aluno
        count = 1
        while True:
            try: #Tenta executar o seguinte codigo, porem caso der erro (na criação do id) ele vai somar mais 1 ao Id
                id_user = count #criação do id
                dados = (id_user, nome, sobrenome, telefone, nascimento, email, genero)
                cursor.execute(sql2_aluno, dados)
                conexao.commit()
                print (f'Aluno "{nome}" inserido com sucesso!')         
                break
            except:
                count += 1
        
        #Insere o ID do aluno e o ID do curso na tabale associativa, ligando os dois
        dados = (id_user, curso)
        cursor.execute(sql4_ass_aluno, dados)  
        conexao.commit()
       
    else:

        #recebimento dos dados
        nome = str(input('Insira o nome do Professor: '))
        sobrenome = str(input('Insira o sobrenome: '))
        telefone = str(input('Insira o telefone: '))
        email = str(input('Insira o e-mail: '))
        genero = str(input('Insira o genero (M- masculino | F- Feminino): '))
        genero = genero.upper() #Coloca em letra maiuscula o genero inserido
        salario = int(input('Insira o salario: '))
        dia = int(input('Insira o dia do nascimento: '))
        mes = int(input('Insira o mes do nascimento: '))
        ano = int(input('Insira o ano do nascimento: '))
        nascimento = f'{ano}-{mes}-{dia}'

        print ('\n')
        for a in registros: #mostra os cursos existentes para o usuario poder escolher
            print (f'{a[0]}- {a[1]}')                 
        print('\n')
        curso = int(input('Insira o curso: '))

        #Inserir o Professor
        count = 1
        while True:
            try: #Tenta executar o seguinte codigo, porem caso der erro (na criação do id) ele vai somar mais 1 ao Id
                id_user = count #criação do id
                dados = (id_user, nome, sobrenome, telefone, salario, email, genero, nascimento)
                cursor.execute(sql3_professor, dados)
                conexao.commit()
                print (f'Professor "{nome}" inserido com sucesso!')
                break
            except:
                count+=1
        
        #Insere o ID do professor e o ID do curso na tabale associativa, ligando os dois
        dados = (id_user, curso)
        cursor.execute(sql5_ass_professor, dados)
        conexao.commit()
    
    cursor.close() #fecha o cursor
def update(conexao, escolha_usuario): #Função para atualização dos dados no BD

    #Armazena os cursos existentes na variavel "registros_cursos"
    sql1 = '''select id_curso ,nome_curso from tb_curso '''
    cursor = conexao.cursor() #abre o cursor
    cursor.execute(sql1)
    registros_cursos = cursor.fetchall()

    #Variaveis com codigos SQL para a atualização dos dados

        ##Alunos
    sql_nome_aluno = '''                                              
    update tb_aluno
    set nome_aluno = %s
    where id_aluno = %s'''

    sql_sobrenome_aluno = '''                                               
    update tb_aluno
    set sobrenome_aluno = %s
    where id_aluno = %s
    '''
    sql_telefone_aluno = '''                                               
    update tb_aluno
    set telefone = %s
    where id_aluno = %s
    '''
    sql_nascimento_aluno = '''                                               
    update tb_aluno
    set nascimento = %s
    where id_aluno = %s
    '''
    sql_email_aluno = '''                                               
    update tb_aluno
    set email = %s
    where id_aluno = %s
    '''
    sql_genero_aluno = '''                                               
    update tb_aluno
    set genero = %s
    where id_aluno = %s
    '''
    sql_curso_add_aluno = '''                                               
    insert into ta_curso_aluno
    value (%s, %s)
    '''

    sql_getCursos_aluno = '''
    SELECT 
        b.id_curso ,b.nome_curso
        FROM
        tb_curso b
            JOIN
        ta_curso_aluno c on c.tb_curso_id_curso = b.id_curso
            JOIN
        tb_aluno a on a.id_aluno = c.td_aluno_id_aluno
        
        where a.id_aluno = %s
     '''

    sql_curso_delete_aluno = '''

    delete from ta_curso_aluno
    where td_aluno_id_aluno = %s and tb_curso_id_curso = %s
     
     '''

        ##Professor
    sql_nome_professor = '''                                               
    update tb_professor
    set nome_prof = %s
    where id_prof = %s
    '''
    sql_sobrenome_professor = '''                                               
    update tb_professor
    set sobrenome_prof = %s
    where id_prof = %s
    '''
    sql_telefone_professor = '''                                               
    update tb_professor
    set telefone_prof = %s
    where id_prof = %s
    '''
    sql_nascimento_professor = '''                                              
    update tb_professor
    set nascimento = %s
    where id_prof = %s
    '''
    sql_email_professor = '''
    update tb_professor                                               
    set email = %s
    where id_prof = %s
    '''
    sql_genero_professor = '''                                               
    update tb_professor
    set genero = %s
    where id_prof = %s
    '''
    sql_salario_professor = '''
    update tb_professor
    set salario = %s
    where id_prof = %s
    '''

    sql_curso_add_professor = '''                                               
    insert into ta_professor_curso
    value (%s, %s)
    '''

    sql_getCursos_professor = '''
    SELECT 
        b.id_curso ,b.nome_curso
        FROM
        tb_curso b
            JOIN
        ta_professor_curso c on c.tb_curso_id_curso = b.id_curso
            JOIN
        tb_professor a on a.id_prof = c.tb_professor_id_prof
        
        where a.id_prof = %s
     '''

    sql_curso_delete_professor = '''

    delete from ta_professor_curso
    where tb_professor_id_prof = %s and tb_curso_id_curso = %s
     
     '''
    

    while True:

        #Verifica o tipo de usuario abre o Menu de opções de atualização e as realiza        
        if escolha_usuario == 1: 
            print ('Menu de alteração')
            print ('1- Alterar nome')
            print ('2- Alterar sobrenome')
            print ('3- Alterar telefone')
            print ('4- Alterar data de nascimento')
            print ('5- Alterar email')
            print ('6- Alterar genero')
            print ('7- Alterar curso')
            print ('9- Voltar')        
            alt = int(input('O que voce deseja alterar?: '))


            if alt != 9: #Caso o usuario digite "9" ele volta, caso diferente disse ele segue para a execução do programa              
                
                #Seleciona o ID do aluno que sofrera alteração e armazena o nome dele na variavel "registros"
                read(conexao, escolha_usuario) #Mostra os alunos
                user_id = int(input('Insira o ID do aluno que deseja alterar: '))
                sql_select_aluno = '''select nome_aluno from tb_aluno where id_aluno = %s'''
                dado = (user_id,)
                cursor.execute(sql_select_aluno, dado)
                registros = cursor.fetchall()

                #Opções de alteração
                if alt == 1: ##Nome
                    novo_nome = str(input(f'\nInsira o novo nome para {registros[0][0]}: '))

                    #executa o codigo SQL referente a função
                    dados = (novo_nome, user_id)
                    cursor.execute(sql_nome_aluno, dados)
                    print ('\nNome alterado com sucesso\n\n')

                elif alt == 2:##Sobrenome
                    novo_sobrenome = str(input(f'\nInsira o novo sobrenome para {registros[0][0]}: '))

                    #executa o codigo SQL referente a função
                    dados = (novo_sobrenome, user_id)
                    cursor.execute(sql_sobrenome_aluno, dados)
                    print ('\nSobrenome alterado com sucesso\n\n')

                elif alt == 3:##Telefone
                    novo_telefone = str(input(f'\nInsira o novo telefone para {registros[0][0]}: '))

                    #executa o codigo SQL referente a função
                    dados = (novo_telefone, user_id)
                    cursor.execute(sql_telefone_aluno, dados)
                    print ('\nTelefone alterado com sucesso\n\n')

                elif alt == 4:##Data de nascimento
                    novo_dia = str(input(f'\nInsira o novo dia de nascimento para {registros[0][0]}: '))
                    novo_mes = str(input(f'Insira o novo mes: '))
                    novo_ano = str(input(f'Insira o novo ano: '))
                    novo_nascimento = f'{novo_ano}-{novo_mes}-{novo_dia}'

                    #executa o codigo SQL referente a função
                    dados = (novo_nascimento, user_id)
                    cursor.execute(sql_nascimento_aluno, dados)
                    print ('\nData de nascimento alterada com sucesso\n\n')

                elif alt == 5:##E-mail
                    novo_email = str(input(f'\nInsira o novo email para {registros[0][0]}: '))

                    #executa o codigo SQL referente a função
                    dados = (novo_email, user_id)
                    cursor.execute(sql_email_aluno, dados)
                    print ('\nEmail alterado com sucesso\n\n')

                elif alt == 6:##Genero
                    novo_genero = str(input(f'\nInsira o novo genero para {registros[0][0]}: '))
                    novo_genero = novo_genero.upper()

                    #executa o codigo SQL referente a função
                    dados = (novo_genero, user_id)
                    cursor.execute(sql_genero_aluno, dados)
                    print ('\nGenero alterado com sucesso\n\n')

                elif alt == 7:##Curso

                    #Os cursos o usuario pode escolher entre, adicionar um novo ou excluir um
                    print ('1- Adicionar um novo curso: ')
                    print ('2- Excluir um curso')
                    escolha = int(input('Opção: '))

                    if escolha == 1: #Adicionar curso
                        print ('\n')
                        for a in registros_cursos: #mostra os cursos disponiveis para ele adicionar
                            print (f'{a[0]}- {a[1]}')                 
                        print('\n')
                        novo_curso = int(input(f'\nInsira o novo curso para {registros[0][0]}: '))

                        #executa o codigo SQL referente a função
                        dados = (user_id, novo_curso)
                        cursor.execute(sql_curso_add_aluno, dados)
                        print ('\nCurso alterado com sucesso\n\n')

                    elif escolha == 2: #remover curso
                        dados = (user_id,)
                        cursor.execute(sql_getCursos_aluno, dados)
                        registros = cursor.fetchall()

                        print ('\n')
                        for a in registros: #mostra os cursos disponiveis para ele remover
                            print (f'{a[0]}- {a[1]}')                 
                        print('\n')

                        excuir = int(input('\nInsira qual curso deseja excluir: '))

                        #executa o codigo SQL referente a função
                        dados= (user_id, excuir)
                        cursor.execute(sql_curso_delete_aluno, dados)
                        print ('\nCurso alterado com sucesso\n\n')

                conexao.commit() #envia os executes para o banco de dados           

            else:
                cursor.close() #fecha o cursor
                break
        
        else:
            print ('Menu de alteração')
            print ('1- Alterar nome')
            print ('2- Alterar sobrenome')
            print ('3- Alterar telefone')
            print ('4- Alterar data de nascimento')
            print ('5- Alterar email')
            print ('6- Alterar salario')
            print ('7- Alterar genero')
            print ('8- Alterar curso')
            print ('10- Voltar')  
            alt = int(input('O que voce deseja alterar?: '))
            if alt != 10:
                
                #Seleciona o ID do professor que sofrera alteração e armazena o nome dele na variavel "registros"
                read(conexao, escolha_usuario)#Mostra os professores
                user_id = int(input('Insira o ID do professor que deseja alterar: '))
                sql_select_professor = '''select nome_prof from tb_professor where id_prof = %s'''
                dado = (user_id,)
                cursor.execute(sql_select_professor, dado)
                registros = cursor.fetchall()

                #Opções de alteração
                if alt == 1: ##Nome
                    novo_nome = str(input(f'\nInsira o novo nome para {registros[0][0]}: '))

                    #executa o codigo SQL referente a função
                    dados = (novo_nome, user_id)
                    cursor.execute(sql_nome_professor, dados)
                    print ('\nNome alterado com sucesso\n\n')
                elif alt == 2:##Sobrenome
                    novo_sobrenome = str(input(f'\nInsira o novo sobrenome para {registros[0][0]}: '))

                    #executa o codigo SQL referente a função
                    dados = (novo_sobrenome, user_id)
                    cursor.execute(sql_sobrenome_professor, dados)
                    print ('\nSobrenome alterado com sucesso\n\n')
                elif alt == 3:##Telefone
                    novo_telefone = str(input(f'\nInsira o novo telefone para {registros[0][0]}: '))

                    #executa o codigo SQL referente a função
                    dados = (novo_telefone, user_id)
                    cursor.execute(sql_telefone_professor, dados)
                    print ('\nTelefone alterado com sucesso\n\n')
                elif alt == 4:##Data de nascimento
                    novo_dia = str(input(f'\nInsira o novo dia de nascimento para {registros[0][0]}: '))
                    novo_mes = str(input(f'Insira o novo mes: '))
                    novo_ano = str(input(f'Insira o novo ano: '))
                    novo_nascimento = f'{novo_ano}-{novo_mes}-{novo_dia}'

                    #executa o codigo SQL referente a função
                    dados = (novo_nascimento, user_id)
                    cursor.execute(sql_nascimento_professor, dados)
                    print ('\nData de nascimento alterada com sucesso\n\n')
                elif alt == 5:##E-mail
                    novo_email = str(input(f'\nInsira o novo email para {registros[0][0]}: '))

                    #executa o codigo SQL referente a função
                    dados = (novo_email, user_id)
                    cursor.execute(sql_email_professor, dados)
                    print ('\nEmail alterado com sucesso\n\n')
                elif alt == 6:##Salario
                    novo_salario = int(input(f'\nInsira o novo salario para {registros[0][0]}: '))

                    #executa o codigo SQL referente a função
                    dados = (novo_salario, user_id)
                    cursor.execute(sql_salario_professor, dados)
                    print ('\nSalario alterado com sucesso\n\n')
                elif alt == 7:##Genero
                    novo_genero = str(input(f'\nInsira o novo genero para {registros[0][0]}: '))
                    novo_genero = novo_genero.upper()

                    #executa o codigo SQL referente a função
                    dados = (novo_genero, user_id)
                    cursor.execute(sql_genero_professor, dados)
                    print ('\nGenero alterado com sucesso\n\n')
                elif alt == 8:##Curso

                    #Os cursos o usuario pode escolher entre, adicionar um novo ou excluir um
                    print ('1- Adicionar um novo curso: ')
                    print ('2- Excluir um curso')
                    escolha = int(input('Opção: '))

                    if escolha == 1: #Adicionar curso

                        print ('\n')
                        for a in registros_cursos: #mostra os cursos disponiveis para ele adicionar
                            print (f'{a[0]}- {a[1]}')                 
                        print('\n')

                        novo_curso = int(input(f'\nInsira o novo curso para {registros[0][0]}: '))

                        #executa o codigo SQL referente a função
                        dados = (user_id, novo_curso)
                        cursor.execute(sql_curso_add_professor, dados)
                        print ('\nCurso alterado com sucesso\n\n')
                    elif escolha == 2: #Remover curso

                        dados = (user_id,)
                        cursor.execute(sql_getCursos_professor, dados)
                        registros = cursor.fetchall()

                        print ('\n')
                        for a in registros: #mostra os cursos disponiveis para ele remover
                            print (f'{a[0]}- {a[1]}')                 
                        print('\n')

                        excuir = int(input('\nInsira qual curso deseja excluir: '))

                        #executa o codigo SQL referente a função
                        dados= (user_id, excuir)
                        cursor.execute(sql_curso_delete_professor, dados)
                        print ('\nCurso alterado com sucesso\n\n')

                conexao.commit() #envia os executes para o banco de dados  
                        
            else:
                cursor.close() #fecha o cursor
                break
def delete(conexao, escolha_usuario): #Função para deletar dados no BD
    cursor = conexao.cursor() #Abre o cursor

    #Variaveis com codigos SQL para a remoção dos dados

        ##tabelas basicas
    sql_aluno = '''delete
    from tb_aluno
    where id_aluno = %s'''

    sql_professor = '''delete
    from tb_professor
    where id_prof = %s'''

        ##tabelas associativas
    sql_ass_aluno = '''delete
    from ta_curso_aluno
    where td_aluno_id_aluno = %s
    '''
    sql_ass_professor = '''delete
    from ta_professor_curso
    where tb_professor_id_prof = %s
    '''

    read(conexao, escolha_usuario) #mostra os dados com base na escolha de tipo de usuario (1- Aluno | 2- Professor)
    
    #Verifica o tipo de usuario (1- Aluno | 2- Professor) para excluir os dados
    if escolha_usuario == 1:      
        user_id = int(input('Insira o ID do aluno que deseja deletar: '))

        #executa o codigo SQL para excluir
        dados = (user_id,)
        cursor.execute(sql_ass_aluno, dados)
        cursor.execute(sql_aluno, dados)
        
    else:
        user_id = int(input('Insira o ID do professor que deseja deletar: '))

        #executa o codigo SQL para excluir
        dados = (user_id,)
        cursor.execute(sql_ass_professor, dados)
        cursor.execute(sql_professor, dados)
        
    
    conexao.commit()
    print ('\nUsuario deletado com sucesso')
    cursor.close() #fecha o cursor


if __name__ == '__main__':
    conn = conectar() #Inicia a conexão com o banco de dados
    print ('Bem vindo a nossa plataforma de gerenciamento de cursos online\n')

    while True:
        print ('MENU\n')
        print ('1- Visualizar usuarios')
        print ('2- Adicionar novo usuario')
        print ('3- Atualizar usuario')
        print ('4- Deletar usuario')
        print ('5- Sair')
        opcao_menu = int(input('Opção: '))


        if opcao_menu == 1:
            escolha_usuario = chose_user('Qual usuario deseja visualizar?')
            read(conn, escolha_usuario)
        elif opcao_menu == 2:
            escolha_usuario = chose_user('Qual tipo de usuario deseja adicionar?')
            insert(conn, escolha_usuario)
        elif opcao_menu == 3:
            escolha_usuario = chose_user('Qual tipo de usuario deseja atualizar?')
            update(conn, escolha_usuario)
        elif opcao_menu == 4:
            escolha_usuario = chose_user('Qual tipo de usuario deseja deletar?')
            delete(conn, escolha_usuario)
        elif opcao_menu == 5:
            conn.close() #Fecha a conexão ao sair do programa
            break
        else:
            print ('Opção incorreta')
