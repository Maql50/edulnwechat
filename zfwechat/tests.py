import MySQLdb


db = MySQLdb.connect(user='root', password='123321', db='test')
cursor = db.cursor()
cursor.execute("select * from table")
result = cursor.fetchall()
cursor.close()
db.close()