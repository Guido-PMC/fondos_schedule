import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import cronitor
import os
import requests
from prettytable import PrettyTable

cronitor.api_key = '5e67b190fd224e6ca399c5e1b7286199'
cronitor.Monitor.put(
    key='AutomatismoFondos',
    type='job'
)
monitor = cronitor.Monitor('AutomatismoFondos')

if "DOCKER" in os.environ['ENVIRONMENT']:
    credenciales = 'app/pilarminingco-c11e8da70b2f.json'
if "TEST" in os.environ['ENVIRONMENT']:
    credenciales = 'pilarminingco-c11e8da70b2f.json'
if "PROD" in os.environ['ENVIRONMENT']:
    credenciales = '/home/PMC/AutomatismosPMC/pilarminingco-c11e8da70b2f.json'
telegram_id = "-658880136"

def getCellByRow(sheet, worksheet, row):
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(credenciales, scope)
    client = gspread.authorize(creds)
    work_sheet = client.open(sheet)
    sheet_instance = work_sheet.worksheet(worksheet)
    val = sheet_instance.acell(row).value
    return (val)


def telegram_message(message):
    headers_telegram = {"Content-Type": "application/x-www-form-urlencoded"}
    endpoint_telegram = "https://api.telegram.org/bot1956376371:AAFgQ8zc6HLwRReXnzdfN7csz_-iEl8E1oY/sendMessage"
    mensaje_telegram = {"chat_id": telegram_id, "text": "Problemas en RIG"}
    #mensaje_telegram = {"chat_id": "-747786820", "text": "Problemas en RIG"}
    mensaje_telegram["text"] = message
    response = requests.post(endpoint_telegram, headers=headers_telegram, data=mensaje_telegram).json()
    return response

def getDolarBlue(operacion):
    response = requests.get("https://api.bluelytics.com.ar/v2/latest").json()
    if "buy" in operacion:
        return response["blue"]["value_buy"]
    if "sell" in operacion:
        return response["blue"]["value_sell"]
    if "avg" in operacion:
        return response["blue"]["value_avg"]



monitor.ping(state='run')

fondosUSD = getCellByRow("Pilar Mining CO", "FONDOS $ / U$", "U2")
fondosARS = getCellByRow("Pilar Mining CO", "FONDOS $ / U$", "T2")
dolarVenta = getDolarBlue("sell")
dolarCompra = getDolarBlue("buy")
string = PrettyTable(["Fondos","USD", "ARS"])
string.add_row(["","10.000","1.000.000"])
string.border = False
string.left_padding_width(1)
telegram_message(string)
print(string)
#telegram_message("Fondos en USD                         Fondos en ARS ")
#telegram_message("VALORES                 "+str(fondosUSD) + "                                        "+str(fondosARS)+"     .")
#telegram_message("USD          -        Punta Compra       " " -               Punta Venta       ")
#telegram_message("VALORES                 "+str(dolarCompra) + "                                        "+str(dolarVenta)+"     .")



monitor.ping(state='complete')
