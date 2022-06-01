from core import MySqlDatabase, Database, Table


@MySqlDatabase("application", host="localhost", user="root", password="omar1234")
class Users(Table):
    id = Table.integerField(primary=True, null=False)
    name = Table.stringField()
    username = Table.stringField()
    password = Table.stringField()


u = Users()
find = u.where("username").equals("other").first()
if find:
    pass






