import pyodbc
import configparser

config = configparser.ConfigParser()
config.read("Database/webconfig")
driver = config.get("conn", "driver")
server = config.get("conn", "server")
us = config.get("conn", "us")
pw = config.get("conn", "pwd")
database = config.get("conn", "database1")
string_conn = "driver={0};server={1};database={2};uid={3};pwd={4}".format(driver, server, database, us, pw)


def log(mytext):
    with open("./logdata.txt", "a") as file:
        file.write(mytext + "\n")


def save_venue(venue):
    try:
        cnxn = pyodbc.connect(string_conn)
        cnxn.autocommit = True
        cursor = cnxn.cursor()
        cursor.execute(
            '{CALL [PR_INSUPD_VENUE](@IDV=?,@IDEVENUE=?,@VNAME=?,@VURL=?,@ACCTOILET=?,@CHANGEPLACE=?,@HOIST=?,@WET=?)}',
            (venue["idv"], venue["idevenue"], venue["name"],
             venue["url"], venue["acc"], venue["ch"],
             venue["ho"], venue["we"]))
        the_result = cursor.fetchval()
        cnxn.close()
        return the_result
    except pyodbc.Error as e:
        log(mytext='save_venue' + str(e))
        return 0


def save_user(user):
    try:
        cnxn = pyodbc.connect(string_conn)
        cnxn.autocommit = True
        cursor = cnxn.cursor()
        cursor.execute('{CALL [PR_INSUPD_VUSER](@IDU=?,@NICK=?,@LOCAT=?)}',
                       (user["idu"], user["author"], user["location"]))
        the_result = cursor.fetchval()
        cnxn.close()
        return the_result
    except pyodbc.Error as e:
        log(mytext='save_user' + str(e))
        return 0


def save_review(review):
    try:
        cnxn = pyodbc.connect(string_conn)
        cnxn.autocommit = True
        cursor = cnxn.cursor()
        cursor.execute(
            '{CALL [PR_INSUPD_VREVIEW](@IDREV=?,@IDU=?,@IDV=?,@IDEVREV=?,@RANK=?,@VMONTH=?,@VYEAR=?,@OVERVIEW=?,@TRANSPORT=?,@ACCESS=?,@TOILET=?,@STAFF=?,@ANYTHING=?)}',
            (review["idrev"], review["idu"], review["idv"], review["idevrev"], review["rank"],
             review["month"], review["year"], review["Overview"], review["Transport & Parking"],
             review["Access"], review["Toilets"], review["Staff"], review["Anything else you wish to tell us?"]
             ))
        the_result = cursor.fetchval()
        cnxn.close()
        return the_result
    except pyodbc.Error as e:
        log(mytext='save_review ' + str(e) + " /" + str(review["rank"]) + " /" + str(review["month"]))
        return 0

def save_sum(ids,idv,idt,sum):
    try:
        cnxn = pyodbc.connect(string_conn)
        cnxn.autocommit = True
        cursor = cnxn.cursor()
        cursor.execute(
            '{CALL [PR_INSUPD_SUMMARY](@IDS=?,@IDV=?,@IDT=?,@SUM=?)}',
            (ids,idv,idt,sum))
        the_result = cursor.fetchval()
        cnxn.close()
        return the_result
    except pyodbc.Error as e:
        log(mytext='save_venue' + str(e))
        return 0
    
def if_sum(idv,idt):
    try:
        cnxn = pyodbc.connect(string_conn)
        cnxn.autocommit = True
        cursor = cnxn.cursor()
        cursor.execute(
            '{CALL [PR_IF_SUMMARY](@IDV=?,@IDT=?)}',
            (idv,idt))
        the_result = cursor.fetchval()
        cnxn.close()
        return the_result
    except pyodbc.Error as e:
        log(mytext='if_sum' + str(e))
        return 0