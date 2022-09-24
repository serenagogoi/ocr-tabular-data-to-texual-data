import cx_Oracle
con = cx_Oracle.connect('trainee/trainee@10.203.187.51/epijrt')
print (con.version)
con.close()