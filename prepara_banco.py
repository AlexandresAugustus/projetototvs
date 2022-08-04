import mysql.connector
from flask_bcrypt import generate_password_hash
from mysql.connector import errorcode                 ## importando as bibliotecas do Mysql ; Flask

print("Conectando...")
try:
      conn = mysql.connector.connect(
            host='127.0.0.1',
            user='root',                                               ## fazendo conexão com servidor do Mysql
            password='admin'
      )
except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('Existe algo errado no nome de usuário ou senha')
      else:
            print(err)

cursor = conn.cursor()

cursor.execute("DROP DATABASE IF EXISTS `segredo`;")

cursor.execute("CREATE DATABASE `segredo`;")

cursor.execute("USE `segredo`;")

# criando tabelas
TABLES = {}
TABLES['Segredo'] = ('''
      CREATE TABLE `segredo` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `nome` varchar(50) NOT NULL,      
      PRIMARY KEY (`id`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

TABLES['Usuarios'] = ('''
      CREATE TABLE `usuarios` (
      `nome` varchar(20) NOT NULL,
      `nickname` varchar(8) NOT NULL,                               
      `senha` varchar(100) NOT NULL,
      PRIMARY KEY (`nickname`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

for tabela_nome in TABLES:
      tabela_sql = TABLES[tabela_nome]
      try:
            print('Criando tabela {}:'.format(tabela_nome), end=' ')
            cursor.execute(tabela_sql)
      except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                  print('Já existe')
            else:
                  print(err.msg)
      else:
            print('OK')


# inserindo usuarios
usuario_sql = 'INSERT INTO usuarios (nome, nickname, senha) VALUES (%s, %s, %s)'
usuarios = [
      ("Alexandre Augusto", "ASA", generate_password_hash("1234").decode('utf-8')),
      ("Flavia Marcela", "preta", generate_password_hash("1234").decode('utf-8')),
      ("Aquilles Perseu", "cat", generate_password_hash("1234").decode('utf-8'))
]
cursor.executemany(usuario_sql, usuarios)

cursor.execute('select * from segredo.usuarios')
print(' -------------  Usuários:  -------------')
for user in cursor.fetchall():
    print(user[1])

# inserindo segredo
segredo_sql = 'INSERT INTO segredo (nome ) VALUES (%s)'
segredo = [

]
cursor.executemany(segredo_sql, segredo)

cursor.execute('select * from segredo.segredo')
print(' -------------  Segredo:  -------------')
for segredo in cursor.fetchall():
    print(segredo[1])

# commitando se não nada tem efeito
conn.commit()

cursor.close()
conn.close()