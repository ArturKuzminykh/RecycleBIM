import requests

def prepare_token():
    with open("credentials.txt") as file:
        d = {}
        token = file.readline().rstrip().split("=")
        chat_id = file.readline().rstrip().split("=")
        d[token[0]] = token[1]
        d[chat_id[0]] = chat_id[1]
        return d
       # return {elem.split("=")[0] : elem.split("=")[1] for elem in file.readline().rstrip().split(";")}

cred = prepare_token()

def send_msg(text):
   token = cred["RECYCLE_BIM_TELEGRAM_API_TOKEN"]
   chat_id = cred["RECYCLE_BIM_TELEGRAM_CHAT_ID"]
   url_req = "https://api.telegram.org/bot" + token + "/sendMessage" + "?chat_id=" + chat_id + "&text=" + text 
   results = requests.get(url_req)
   #print(results.json())