# Use the MYSQL database through the pymysql plugin,
# the query statement is the same as the ordinary statement
import pymysql

f_entity = open('../subgraph_v1/entity2id.txt', 'r')
f_relation = open('../subgraph_v1/relation2id.txt', 'r')
f_train = open('../subgraph_v1/train2id.txt', 'r')

# read all content
# data = f.read()
# print(data)   #end=''do not print space，print(data, end='')
# #process data
# all_entity = f_entity.readlines()
all_relation = f_relation.readlines()
# all_train = f_train.readlines()
# print('{0}\n{1}\n{2}'.format(all_entity, all_relation, all_train))

new_entity, new_relation, new_train = [], [], []

def clear_dataset(dataset, new):
    for i in dataset:
        first = i.strip('\n')  # delete \n
        second = first.split()  # delete space
        new.append(second)  # add into list

# clear_dataset(all_entity, new_entity)
clear_dataset(all_relation, new_relation)

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

# connected database
conn = pymysql.Connect(
    host='localhost',
    port=3306,
    user='root',
    passwd='',
    db='kit301',
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

#insert relation data
# for n in new_relation:
#     if len(n) != 1:
#         new_0 = n[0]
#         new_1 = int(n[1])
#         #new_2 = int(n[2])
#         sql = 'INSERT INTO relation2id(Relation_Name, Relation_ID) values (%s, %s)'
#         res = cursor.execute(sql, (new_0, new_1))
#         print(res)




# insert entity data
# for n in new_entity:
#     if len(n) != 1:
#         new_0 = n[0]
#         new_1 = int(n[1])
#         #new_2 = int(n[2])
#         sql = 'INSERT INTO entity2id(Entity_Name, Entity_ID) values (%s, %s)'
#         #print(type(int(n[0])), type(int(n[1])), type(int(n[2])))
#         #res = cursor.execute(sql, ((int(n[0])), (int(n[1])), (int(n[2]))))
#         res = cursor.execute(sql, (new_0, new_1))
#         print(res)


# insert train data
# for n in new_train:
#     if len(n) != 1:
#         head = int(n[0])
#         tail = int(n[1])
#         relation = int(n[2])
#         sql = 'INSERT INTO train(Data_1, Data_2, Data_3) values (%s, %s, %s)'
#         res = cursor.execute(sql, (head, tail, relation))


# a = 1
# b = 2
# c = 3
# sql = 'INSERT INTO train(Data_1, Data_2, Data_3) VALUES (%d, %d, %d)' % (a, b, c)
# cursor.execute(sql)

# # sql
# sql = 'SELECT * FROM users'
#
# # execete sql query
# cursor.execute(sql)
#
# # print how many results are returned
# print(cursor.rowcount)
#
# # read all results
# all_users = cursor.fetchall()
#
# # print result
# for row in all_users:
#     print(' user id is: {}\n'
#           ' first name: {}\n'
#           ' last name:{}\n'
#           ' account name: {}\n'
#           ' email: {}\n'
#           ' password: {}\n'
#           ' phone: {}\n'
#           ' address: {}\n'
#           ' ABN: {}\n'
#           ' account rate: {}\n'.format(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9])
#           )

#print('result is \t', all_users)

# for row in all_users:
#     print('result is', row)

sql = f'SELECT * FROM entity2id'
cursor.execute(sql)
entities = cursor.fetchall()

for row in entities:
    print(' Entity_Name is: {}'
          ' Entity_ID is: {}'.format(row[0], row[1])
          )

# print('entities list: \n', entities, '\n')
# entity = entities
# conn.commit()  # important

conn.commit()   # important
cursor.close()
conn.close()