class ConnectionError(Exception):
    pass

class DBConnectionError(ConnectionError):
    pass

class TestError(Exception):
    pass

class WrongSQLFormat(Exception):
    pass



def executeSQL(sqlStr,dbname):
    if(sqlStr =='test'):
        connectToDB(dbname);
        print("2 : Executin SQL Qurey");
    else:
        raise WrongSQLFormat("Wrong SQL Format, please check");

def connectToDB(dbName):
    if(dbName=="db"):
        print("1 : connected with db")
    else:
        raise ConnectionError("Not Able to connect with DB");

try:
    executeSQL("test1","db1");
except WrongSQLFormat as err:
    print("handled wrong sql format err : ", err)
except ConnectionError as err:
    print("handled connection err : ", err)
except Exception as err:
    print("Error handled : ",err)
