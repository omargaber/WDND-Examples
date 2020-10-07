import psycopg2

# ENTER YOUR DB YOU CREATTED LOCALLY BELOW
# ESTABLISH CONNECTION TO THAT DATABASE
conn = psycopg2.connect('dbname={DB_NAME_HERE}}')

cursor = conn.cursor()

# CREATING TABLES
cursor.execute('create table clients (id SERIAL PRIMARY KEY, first_name VARCHAR NOT NULL);')
cursor.execute('create table contacts (id SERIAL PRIMARY KEY, contact_number INTEGER, client_id INTEGER, CONSTRAINT fk_client FOREIGN KEY(client_id) REFERENCES clients(id));')


# ADDING TO DB

list_of_names = ['Omar', 'Ahmad', 'Mohammad', 'Salma', 'Dina', 'Ibrahim', 'Shakal', "Mo Salah"]

# ADDING TO CLIENTS
for i in list_of_names:
    cursor.execute("INSERT INTO clients (first_name) values ('{}')".format(i))

# ADDING TO TABLE WITH FOREIGN KEY
for i in list_of_names:
    cursor.execute("select * from clients where first_name='{}'".format(i))
    client_id = cursor.fetchone()
    print(client_id[0])
    cursor.execute("INSERT INTO contact (contact_number, client_id) values (1234, '{}')".format(client_id[0]))

# FETCHING (TRY IT OUT)

cursor.execute('''
select * from clients;
''')

print('all', cursor.fetchmany(5))
print('many', cursor.fetchall())
print('one', cursor.fetchone())

# ___________________________________________________________________________________________

conn.commit()
cursor.close()
conn.close()