# Use the MYSQL database through the pymysql plugin,
# the query statement is the same as the ordinary statement
import pymysql

f_entity = open('dataset/entity2id.txt', 'r')
f_relation = open('dataset/relation2id.txt', 'r')
f_train = open('dataset/train2id.txt', 'r')

# read all content
# data = f.read()
# print(data)   #end=''do not print space，print(data, end='')
# #process data
# all_entity = f_entity.readlines()
all_relation = f_relation.readlines()
# all_train = f_train.readlines()
# print('{0}\n{1}\n{2}'.format(all_entity, all_relation, all_train))

# new_entity, new_relation, new_train = [], [], []


#def clear_dataset(dataset, new):
#    for i in dataset:
#        first = i.strip('\n')  # delete \n
#        second = first.split()  # delete space
#        new.append(second)  # add into list


# clear_dataset(all_entity, new_entity)
# clear_dataset(all_relation, new_relation)

# testing code
# clear_dataset(all_train, new_train)
# print('{0}\n{1}\n{2}'.format(new_entity, new_relation, new_train))
# print(int(new_train[2][1]))
# print(len(new_train))
# print(new_train)

# close files
# f_entity.close()
# f_relation.close()
# f_train.close()


def upload_data(dbname, new_relation, new_entity, new_train):
    # connected database
    conn = pymysql.Connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='',
        db="kit301",
        charset='utf8'
    )

    # Create an object linked to a database, similar to mysqli
    cursor = conn.cursor()

    # User_ID INT(20) NOT NULL AUTO_INCREMENT,
    # If the data table already exists use the execute() method to delete the table.
    # cursor.execute("DROP TABLE IF EXISTS EMPLOYEE")
    #
    # # Create data table SQL statement
    # sql = """CREATE TABLE EMPLOYEE (
    #          FIRST_NAME  CHAR(20) NOT NULL,
    #          LAST_NAME  CHAR(20),
    #          AGE INT,
    #          SEX CHAR(1),
    #          INCOME FLOAT)
    #          ENGINE=InnoDB DEFAULT CHARSET=utf8;"""
    #
    # cursor.execute(sql)
    sql = f'drop table if exists {dbname}relations;'
    cursor.execute(sql)
    sql = f'CREATE TABLE {dbname}relations (Relation_Name varchar(255), Relation_ID varchar(255));'
    cursor.execute(sql)

    #insert relation data
    for n in new_relation:
        if len(n) != 1:
            name = n[0]
            id = int(n[1])
            sql = f'INSERT INTO {dbname}relations (Relation_Name, Relation_ID) values (%s, %s)'
            res = cursor.execute(sql, (name, id))
    conn.commit()   # important

    sql = f'drop table if exists {dbname}entities;'
    cursor.execute(sql)
    sql = f'CREATE TABLE {dbname}entities (Entity_Name varchar(255), Entity_ID varchar(255));'
    cursor.execute(sql)

    # insert entity data
    for n in new_entity:
        if len(n) != 1:
            new_0 = n[0]
            new_1 = int(n[1])
            sql = f'INSERT INTO {dbname}entities (Entity_Name, Entity_ID) values (%s, %s)'
            #print(type(int(n[0])), type(int(n[1])), type(int(n[2])))
            #res = cursor.execute(sql, ((int(n[0])), (int(n[1])), (int(n[2]))))
            res = cursor.execute(sql, (new_0, new_1))
            print(res)

    sql = f'drop table if exists {dbname}facts;'
    cursor.execute(sql)
    sql = f'CREATE TABLE {dbname}facts (Data_1 varchar(255), Data_2 varchar(255), Data_3 varchar(255));'
    cursor.execute(sql)
    # insert train data
    for n in new_train:
        if len(n) != 1:
            new_0 = int(n[0])
            new_1 = int(n[1])
            new_2 = int(n[2])
            sql = f'INSERT INTO {dbname}facts(Data_1, Data_2, Data_3) values (%s, %s, %s)'
            #print(type(int(n[0])), type(int(n[1])), type(int(n[2])))
            #res = cursor.execute(sql, ((int(n[0])), (int(n[1])), (int(n[2]))))
            res = cursor.execute(sql, (new_0, new_1, new_2))
            print(res)

    conn.commit()   # important
    cursor.close()
    conn.close()
    # a = 1
    # b = 2
    # c = 3
    # sql = 'INSERT INTO train(Data_1, Data_2, Data_3) VALUES (%d, %d, %d)' % (a, b, c)
    # cursor.execute(sql)


def download_data(dbname, relation, entity, fact):
    #relation.clear()
    #entity.clear()
    #fact.clear()

    conn = pymysql.Connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='',
        db=dbname,
        charset='utf8'
    )

    # Create an object linked to a database, similar to mysqli
    cursor = conn.cursor()

    # Entities
    sql = f'SELECT * FROM entities'
    cursor.execute(sql)
    entities = cursor.fetchall()

    for row in entities:
        print(' Entity_Name is: {}\n'
              ' Entity_ID is: {}\n'.format(row[0], row[1])
              )

    print('entities list: \n', entities, '\n')
    #entity = entities
    conn.commit()   # important

    # Relations
    sql = f'SELECT * FROM relations'
    cursor.execute(sql)
    relations = cursor.fetchall()

    for row in relations:
        print(' Relation_Name is: {}\n'
              ' Relation_ID is: {}\n'.format(row[0], row[1])
              )

    print('relations list: \n', relations, '\n')
    #relation = relations
    conn.commit()   # important

    # Facts
    sql = f'SELECT * FROM facts'
    cursor.execute(sql)
    facts = cursor.fetchall()

    for row in facts:
        print(' Fact_Name is: {}\n'
              ' Fact_ID is: {}\n'.format(row[0], row[1])
              )

    print('facts list: \n', facts, '\n')
    #fact = facts
    conn.commit()   # important

    cursor.close()
    conn.close()