import json
import pymysql
import pymysql.cursors


# Read ALL data from database and convert it to a JSON structure
def convertDataToJson(mycursor):
    query = "SELECT * FROM pgcps_environmental_info"
    mycursor.execute(query)
    result = mycursor.fetchall()

    return json.dumps(result)



################
## MAIN PROGRAM
################
mydb = pymysql.connect(host='127.0.0.1',
                      user='root',
                      password='Chickenleg125',
                      db='pgcps_environmental_lit',
                      charset='utf8mb4',
                      cursorclass=pymysql.cursors.DictCursor)
# mydb = pymysql.connect(host='pgcpsdb.cciww86edgy9.us-east-1.rds.amazonaws.com',
#                       user='root',
#                       password='38kvFH6K20stnYiq7l9z',
#                       db='pgcps_environmental_lit',
#                       charset='utf8mb4',
#                       cursorclass=pymysql.cursors.DictCursor)

mycursor = mydb.cursor()
jsonValue = convertDataToJson(mycursor)
print(jsonValue)
mydb.close()
