import urllib

SECRET_KEY = 'p9Bv<3Eid9%$i01'
# SQLALCHEMY_DATABASE_URI = 'jdbc:sqlserver://(localdb)\MSSQLLocalDB;databaseName=dreamteam_db;integratedSecurity=true;'
# SQLALCHEMY_DATABASE_URI = 'mssql+pyodbc://DRIVER={SQL Server Native Client 11.0};SERVER=(localdb)\MSSQLLocalDB;DATABASE=ElectronicBookBuilding;Trusted_Connection=yes'
# SQLALCHEMY_DATABASE_URI = 'mssql://(localdb)\MSSQLLocalDB/ElectronicBookBuilding?trusted_connection=yes'

params = urllib.parse.quote_plus('DRIVER={SQL Server Native Client 11.0};SERVER=(localdb)\MSSQLLocalDB;DATABASE=dreamteam_db;Trusted_Connection=yes;')
SQLALCHEMY_DATABASE_URI = "mssql+pyodbc:///?odbc_connect=%s" % params