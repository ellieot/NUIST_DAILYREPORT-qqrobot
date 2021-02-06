from flask import Flask, request
import requests, json, time, re
app = Flask(__name__)
url = "http://119.28.45.248:33649/"

def get_botsession():
    # auth
    payload = {"authKey":"YourKey"}
    ret = requests.post(url+"auth", json=payload)
    sess = ret.json()['session']
    # verify
    payload = {"sessionKey": sess, "qq":976113357}
    ret = requests.post(url+"verify", json=payload)
    if not ret.json()['code'] == 0:
        return False
    return sess
    
def sendwords(qq, word):
    payload = {
    "sessionKey": get_botsession(),
    "target": qq,
    "messageChain": [
        { "type": "Plain", "text":  word}
    ]
    }
    requests.post(url+"sendFriendMessage", json=payload)

def NewFriendRequestEvent(value):
    payload = {
        "sessionKey": get_botsession(),
        "eventId": value['eventId'],
        "fromId": value['fromId'],
        "groupId": 0,
        "operate": 0,
        "message": value['message']
    }
    requests.post(url+"resp/newFriendRequestEvent", json=payload)
    time.sleep(2)
    sendwords(value['fromId'], "\
你好,我是机器人martix,主人是2497732985\n\
我现在的使命是帮你填写健康日报\n\
只需要将学生号和信息门户密码发给我就好了\n\
发送的格式如下:\n用户名\n密码\n\n例如:\n\
201813070002\n\
1234567\n\
\n\
(如果待会你发了账户密码,我没回的话,那你就再发一遍)")

def FriendMessage(value):
    str = value['messageChain'][1]['text']
    try:
        username = re.search("^\d+\\n", str).group()[0:-1]
        password = re.search("\\n.+$", str).group()[1:]
    except:
        return sendwords(value['sender']['id'], "我现在傻乎乎的啥也看不懂,有啥事找我主人")
    
    sendwords(value['sender']['id'], "好耶, 成功接收了! \n你的学号是:"+username+"\n密码是"+password+"\n祝你新年快乐!!")
    with open("config.txt", "a") as f:
        f.write("\n"+username+" "+password)


@app.route("/post", methods=['POST'])
def post():
    value = json.loads(request.get_data(as_text=True))
    event = value['type']
    if event == "NewFriendRequestEvent":
        NewFriendRequestEvent(value)
    elif event == "FriendMessage":
        FriendMessage(value)
    
    return "1"

if __name__ == "__main__":
    app.run()
