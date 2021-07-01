import requests
import mysql.connector
import json
import sys
import newfile
from decouple import config
mydb = mysql.connector.connect(
  host= config('HOST'),
  user=config('USER'),
  password=config("PASSWORD"),
  database=config("DATABASE")
)
args = []
hasarguments = False


def Validarguments():
    try:
        firstarg = int(sys.argv[1])
        secondarg = int(sys.argv[2])
        args.append(firstarg)
        args.append(secondarg)
    except:
        print("FATAL ERROR: Arguments must be Ints")
        sys.exit()

    if len(sys.argv) != 3 or args[0] > args[1]:
       print("FATAL ERROR: Provide a LOW and a HIGH")
       sys.exit()
    else:
        print("valid arguments")

def getnewtoken():
    data = {
        'grant_type': 'client_credentials'
    }

    response = requests.post('https://us.battle.net/oauth/token', data=data,
                             auth=(config('CLIENT_ID'), config('CLIENT_SECRET')))
    jsonfile = response.json()

    return jsonfile["access_token"]

def requestspell(iterator):
    spellid = iterator
    token = getnewtoken()
    baseurl = ('https://us.api.blizzard.com/data/wow/spell/' + str( spellid) + '?namespace=static-us&locale=en_US&access_token=' + token)
    blob = requests.get(baseurl)
    return blob

def addspellrow(jsonfile):
    id = jsonfile["id"]
    name = jsonfile["name"]
    description = jsonfile["description"]

    sql = "INSERT INTO spells (id, name, description) VALUES (%s, %s, %s)"
    val = (id, name, description)

    mydb.cursor().execute(sql, val)
    mydb.commit()

def addbadrow(error, index):
    id = index

    sql = "INSERT INTO deadindexes (ID, errorcode) VALUES (%s, %s)"
    val = (error , id)

    mydb.cursor().execute(sql, val)
    mydb.commit()

def beinquerys(idrange):
    low = args[0]
    high = args[1]
    for x in range(low,high):
        response = requestspell(x)
        result = response.status_code
        content = response.content
        jsonfile = response.json()

        if result == 200:
            try:
                addspellrow(jsonfile)
                print("ID " + str(x) + ": " + str(content))
            except:
                print("ID: " + str(x) + " Database commit failed")
        else:
            try:
                addbadrow(x, result)
                print("error occoured for id " + str(x) + ": " + "result code:" + str(result))
            except:
                print("error occoured for id " + str(x) + ": " + "result code:" + str(result) + "WARNING, FAILURE LOGGING NOT WORKING")


Validarguments()
beinquerys(args)
