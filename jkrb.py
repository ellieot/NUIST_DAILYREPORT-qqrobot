# -*- coding: utf-8 -*-
import base64
import json
import random
import requests
import time
import traceback
from bs4 import BeautifulSoup
from Crypto.Cipher import AES
class AESCrypto:
    def __init__(self, key, iv):
        self.key = key.encode("utf-8")
        self.iv = iv.encode("utf-8")
        self.length = AES.block_size
        self.aes = AES.new(self.key, AES.MODE_CBC, self.iv)
    def pad(self, text):
        count = len(text.encode("utf-8"))
        add = self.length - (count % self.length)
        entext = text + (chr(add) * add)
        return entext
    def unpad(self, data):
        return data[0 : -ord(data[-1])]
    def encrypt(self, encrData):
        res = self.aes.encrypt(self.pad(encrData).encode("utf-8"))
        msg = base64.b64encode(res).decode("utf-8")
        return msg
    def decrypt(self, decrData):
        res = base64.decodebytes(decrData.encode("utf-8"))
        msg = self.aes.decrypt(res).decode("utf-8")
        return self.unpad(msg)


def fill_jkrb(stuid, stupwd):
    try:
        sess = requests.session()
        login_url = "https://authserver.nuist.edu.cn/authserver/login"
        soup = BeautifulSoup(sess.get(login_url).text, "html.parser")
        login_data = {
            "username": stuid,
            "password": AESCrypto(soup.find("input", id="pwdEncryptSalt").get("value"), "0" * 16).encrypt(("0" * 64) + stupwd),
            "captcha": "",
            "_eventId": "submit",
            "cllt": "userNameLogin",
            "lt": "",
            "execution": soup.find("input", id="execution").get("value")
        }
        sess.post(login_url, data=login_data)
        jkrb1_url = "http://e-office2.nuist.edu.cn/infoplus/form/XNYQSB/start"
        jkrb1_res = sess.get(jkrb1_url)
        soup = BeautifulSoup(jkrb1_res.text, "html.parser")
        jkrb2_url = "http://e-office2.nuist.edu.cn/infoplus/interface/start"
        csrfToken = soup.find("meta", {"itemscope": "csrfToken"}).get("content")
        jkrb2_data = {
            "idc": soup.find("input", id="idc").get("value"),
            "release": soup.find("input", id="release").get("value"),
            "csrfToken": csrfToken,
            "formData": '{"_VAR_URL":"http://e-office2.nuist.edu.cn/infoplus/form/XNYQSB/start","_VAR_URL_Attr":"{}"}'
        }
        jkrb2_res = sess.post(jkrb2_url, data=jkrb2_data)
        jkrb3_url = jkrb2_res.json()["entities"][0]
        stepId = jkrb3_url.split("form/")[1].split("/")[0]
        jkrb4_url = "http://e-office2.nuist.edu.cn/infoplus/interface/render"
        jkrb4_data = {
            "stepId": stepId,
            "instanceId": "",
            "admin": "false",
            "rand": str(random.random() * 1000.0),
            "width": "955",
            "lang": "zh",
            "csrfToken": csrfToken
        }
        jkrb4_res = sess.post(jkrb4_url, data=jkrb4_data, headers={"Referer": "http://e-office2.nuist.edu.cn/infoplus/form/{}/render".format(stepId)})
        jkrb4_json = jkrb4_res.json()["entities"][0]["data"]
        jkrb5_url = "http://e-office2.nuist.edu.cn/infoplus/interface/doAction"
        jkrb5_data_formData = {
            "_VAR_EXECUTE_INDEP_ORGANIZE_Name": jkrb4_json["_VAR_EXECUTE_INDEP_ORGANIZE_Name"],
            "_VAR_ACTION_INDEP_ORGANIZES_Codes": jkrb4_json["_VAR_ACTION_INDEP_ORGANIZES_Codes"],
            "_VAR_ACTION_REALNAME": jkrb4_json["_VAR_ACTION_REALNAME"],
            # "_VAR_ACTION_ORGANIZE": jkrb4_json["_VAR_ACTION_ORGANIZE"],
            "_VAR_EXECUTE_ORGANIZE": jkrb4_json["_VAR_EXECUTE_ORGANIZE"],
            "_VAR_ACTION_INDEP_ORGANIZE": jkrb4_json["_VAR_ACTION_INDEP_ORGANIZE"],
            "_VAR_ACTION_INDEP_ORGANIZE_Name": jkrb4_json["_VAR_ACTION_INDEP_ORGANIZE_Name"],    
            # "_VAR_ACTION_ORGANIZE_Name": jkrb4_json["_VAR_ACTION_ORGANIZE_Name"],
            "_VAR_EXECUTE_ORGANIZES_Names": jkrb4_json["_VAR_EXECUTE_ORGANIZES_Names"],
            "_VAR_OWNER_ORGANIZES_Codes": jkrb4_json["_VAR_OWNER_ORGANIZES_Codes"],
            "_VAR_ADDR": jkrb4_json["_VAR_ADDR"],
            "_VAR_OWNER_ORGANIZES_Names": jkrb4_json["_VAR_OWNER_ORGANIZES_Names"],
            "_VAR_URL": jkrb4_json["_VAR_URL"],
            "_VAR_EXECUTE_ORGANIZE_Name": jkrb4_json["_VAR_EXECUTE_ORGANIZE_Name"],
            "_VAR_RELEASE": jkrb4_json["_VAR_RELEASE"],
            "_VAR_NOW_MONTH": jkrb4_json["_VAR_NOW_MONTH"],
            "_VAR_ACTION_USERCODES": jkrb4_json["_VAR_ACTION_USERCODES"],
            "_VAR_ACTION_EMAIL": jkrb4_json["_VAR_ACTION_EMAIL"],
            "_VAR_ACTION_ACCOUNT": jkrb4_json["_VAR_ACTION_ACCOUNT"],
            "_VAR_ACTION_INDEP_ORGANIZES_Names": jkrb4_json["_VAR_ACTION_INDEP_ORGANIZES_Names"],
            "_VAR_OWNER_ACCOUNT": jkrb4_json["_VAR_OWNER_ACCOUNT"],
            "_VAR_ACTION_ORGANIZES_Names": jkrb4_json["_VAR_ACTION_ORGANIZES_Names"],
            "_VAR_STEP_CODE": jkrb4_json["_VAR_STEP_CODE"],
            "_VAR_OWNER_USERCODES": jkrb4_json["_VAR_OWNER_USERCODES"],
            "_VAR_EXECUTE_ORGANIZES_Codes": jkrb4_json["_VAR_EXECUTE_ORGANIZES_Codes"],
            "_VAR_NOW_DAY": jkrb4_json["_VAR_NOW_DAY"],
            "_VAR_OWNER_EMAIL": jkrb4_json["_VAR_OWNER_EMAIL"],
            "_VAR_OWNER_REALNAME": jkrb4_json["_VAR_OWNER_REALNAME"],
            "_VAR_NOW": jkrb4_json["_VAR_NOW"],
            "_VAR_URL_Attr": jkrb4_json["_VAR_URL_Attr"],
            "_VAR_ENTRY_NUMBER": jkrb4_json["_VAR_ENTRY_NUMBER"],
            "_VAR_EXECUTE_INDEP_ORGANIZES_Names": jkrb4_json["_VAR_EXECUTE_INDEP_ORGANIZES_Names"],
            "_VAR_STEP_NUMBER": jkrb4_json["_VAR_STEP_NUMBER"],
            "_VAR_POSITIONS": jkrb4_json["_VAR_POSITIONS"],
            "_VAR_EXECUTE_INDEP_ORGANIZES_Codes": jkrb4_json["_VAR_EXECUTE_INDEP_ORGANIZES_Codes"],
            "_VAR_EXECUTE_POSITIONS": jkrb4_json["_VAR_EXECUTE_POSITIONS"],
            "_VAR_ACTION_ORGANIZES_Codes": jkrb4_json["_VAR_ACTION_ORGANIZES_Codes"],
            "_VAR_EXECUTE_INDEP_ORGANIZE": jkrb4_json["_VAR_EXECUTE_INDEP_ORGANIZE"],
            "_VAR_NOW_YEAR": jkrb4_json["_VAR_NOW_YEAR"],
            "groupMQJCRList": [0],
            "fieldFLid": jkrb4_json["fieldFLid"],
            "fieldSQSJ": jkrb4_json["fieldSQSJ"],
            "fieldJBXXxm": jkrb4_json["fieldJBXXxm"],
            "fieldJBXXxm_Name": jkrb4_json["fieldJBXXxm_Name"],
            "fieldJBXXgh": jkrb4_json["fieldJBXXgh"],
            "fieldJBXXxb": jkrb4_json["fieldJBXXxb"],
            "fieldJBXXxb_Name": jkrb4_json["fieldJBXXxb_Name"], # 性别
            "fieldJBXXlxfs": jkrb4_json["fieldJBXXlxfs"], # 电话
            "fieldJBXXdw": jkrb4_json["fieldJBXXdw"],
            "fieldJBXXdw_Name": jkrb4_json["fieldJBXXdw_Name"],
            "fieldJBXXnj": jkrb4_json["fieldJBXXnj"], # 班级
            "fieldJBXXsfzh": jkrb4_json["fieldJBXXsfzh"], # 身份证
            "fieldJBXXJG": jkrb4_json["fieldJBXXJG"],
            "fieldJBXXcsny": "",
            "fieldJBXXfdyxm": jkrb4_json["fieldJBXXfdyxm"],
            "fieldJBXXfdyxm_Name": jkrb4_json["fieldJBXXfdyxm_Name"],
            "fieldJBXXfdygh": jkrb4_json["fieldJBXXfdygh"],
            "fieldJBXXjgs": jkrb4_json["fieldJBXXjgs"],
            "fieldJBXXjgs_Name": jkrb4_json["fieldJBXXjgs_Name"], # 省
            "fieldJBXXjgshi": jkrb4_json["fieldJBXXjgshi"],
            "fieldJBXXjgshi_Name": jkrb4_json["fieldJBXXjgshi_Name"], # 市
            "fieldJBXXjgshi_Attr": '{"_parent":"{' + jkrb4_json["fieldJBXXjgs"] + '}"}',
            "fieldJBXXjgq": jkrb4_json["fieldJBXXjgq"],
            "fieldJBXXjgq_Name": jkrb4_json["fieldJBXXjgq_Name"], # 区
            "fieldJBXXjgq_Attr": '{"_parent":"{' + jkrb4_json["fieldJBXXjgshi"] + '}"}',
            "fieldJBXXjgsjtdz": jkrb4_json["fieldJBXXjgsjtdz"],
            "fieldJBXXjjlxr": jkrb4_json["fieldJBXXjjlxr"], # 电话
            "fieldJBXXjjlxrdh": jkrb4_json["fieldJBXXjjlxrdh"],# 电话
            "fieldSTQKsfstbs": jkrb4_json["fieldSTQKsfstbs"],
            "fieldSTQKks": jkrb4_json["fieldSTQKks"],
            "fieldSTQKgm": jkrb4_json["fieldSTQKgm"],
            "fieldSTQKfs": jkrb4_json["fieldSTQKfs"],
            "fieldSTQKfl": jkrb4_json["fieldSTQKfl"],
            "fieldSTQKhxkn": jkrb4_json["fieldSTQKhxkn"],
            "fieldSTQKfx": jkrb4_json["fieldSTQKfx"],
            "fieldSTQKqt": jkrb4_json["fieldSTQKqt"],
            "fieldSTQKqtms": jkrb4_json["fieldSTQKqtms"],
            "fieldSTQKfrtw": str(random.randint(366, 370) / 10),
            "fieldSTQKqtqksm": jkrb4_json["fieldSTQKqtqksm"],
            "fieldSTQKdqstzk": jkrb4_json["fieldSTQKdqstzk"],
            "fieldSTQKglsjrq": "",
            "fieldSTQKglsjsf": "",
            "fieldSTQKfrsjrq": "",
            "fieldSTQKfrsjsf": "",
            "fieldCXXXcxzt": jkrb4_json["fieldCXXXcxzt"],
            "fieldCXXXjtzz": jkrb4_json["fieldCXXXjtzz"],
            "fieldCXXXjtzz_Name": jkrb4_json["fieldCXXXjtzz_Name"], # 省级
            "fieldCXXXjtzzs": jkrb4_json["fieldCXXXjtzzs"],
            "fieldCXXXjtzzs_Name": jkrb4_json["fieldCXXXjtzzs_Name"], # 市级
            "fieldCXXXjtzzs_Attr": '{"_parent":"{' + jkrb4_json["fieldCXXXjtzz"] + '}"}',
            "fieldCXXXjtzzq": jkrb4_json["fieldCXXXjtzzq"],
            "fieldCXXXjtzzq_Name": jkrb4_json["fieldCXXXjtzzq_Name"], # 区
            "fieldCXXXjtzzq_Attr": '{"_parent":"{' + jkrb4_json["fieldCXXXjtzzs"] + '}"}',
            "fieldCXXXjtjtzz": jkrb4_json["fieldCXXXjtjtzz"], # 详细家庭住址
            "fieldCXXXfxxq": jkrb4_json["fieldCXXXfxxq"], 
            "fieldCXXXfxxq_Name": jkrb4_json["fieldCXXXfxxq_Name"], 
            "fieldCXXXssh": jkrb4_json["fieldCXXXssh"],
            "fieldCXXXdqszd": jkrb4_json["fieldCXXXdqszd"],
            "fieldCXXXcqwdq": jkrb4_json["fieldCXXXcqwdq"],
            "fieldCXXXfxcfsj": "",
            "fieldCXXXjtfsfj": jkrb4_json["fieldCXXXjtfsfj"],
            "fieldCXXXjtfshc": jkrb4_json["fieldCXXXjtfshc"],
            "fieldCXXXjtfsdb": jkrb4_json["fieldCXXXjtfsdb"],
            "fieldCXXXjtfspc": jkrb4_json["fieldCXXXjtfspc"],
            "fieldCXXXjtfslc": jkrb4_json["fieldCXXXjtfslc"],
            "fieldCXXXjtfsqt": jkrb4_json["fieldCXXXjtfsqt"],
            "fieldCXXXjtfsqtms": jkrb4_json["fieldCXXXjtfsqtms"],
            "fieldCXXXjtgjbc": jkrb4_json["fieldCXXXjtgjbc"],
            "fieldYQJLjrsfczbl": jkrb4_json["fieldYQJLjrsfczbl"],
            "fieldYQJLjrsfczbldqzt": jkrb4_json["fieldYQJLjrsfczbldqzt"],
            "fieldYQJLsfjcqtbl": jkrb4_json["fieldYQJLsfjcqtbl"],
            "fieldCXXXsftjwh": jkrb4_json["fieldCXXXsftjwh"],
            "fieldCXXXsftjhb": jkrb4_json["fieldCXXXsftjhb"],
            "fieldCXXXsftjhbs": jkrb4_json["fieldCXXXsftjhbs"],
            "fieldCXXXsftjhbs_Name": jkrb4_json["fieldCXXXsftjhbs_Name"],
            "fieldCXXXsftjhbs_Attr": '{"_parent":"420000"}',
            "fieldCXXXsftjhbq": jkrb4_json["fieldCXXXsftjhbq"],
            "fieldCXXXsftjhbq_Name": jkrb4_json["fieldCXXXsftjhbq_Name"],
            "fieldCXXXsftjhbq_Attr": '{"_parent":""}',
            "fieldCXXXsftjhbjtdz": jkrb4_json["fieldCXXXsftjhbjtdz"],
            "fieldYC": jkrb4_json["fieldYC"],
            "fieldMQJCRxh": [1],
            "fieldMQJCRxm": [""],
            "fieldMQJCRlxfs": [""],
            "fieldMQJCRcjdd": [""],
            "fieldCNS": True,
            "_VAR_ENTRY_NAME": u"\u5b66\u751f\u5065\u5eb7\u72b6\u51b5\u7533\u62a5",
            "_VAR_ENTRY_TAGS": u"\u5b66\u5de5\u90e8"
        }
        jkrb5_data = {
            "actionId": "1",
            "formData": json.dumps(jkrb5_data_formData),
            "remark": "",
            "rand": str(random.random() * 1000.0),
            "nextUsers": "{}",
            "stepId": str(stepId),
            "timestamp": str(int(time.time())),
            "boundFields": "fieldCXXXjtgjbc,fieldMQJCRxh,fieldCXXXsftjhb,fieldSTQKqt,fieldSTQKglsjrq,fieldYQJLjrsfczbldqzt,fieldCXXXjtfsqtms,fieldCXXXjtfsfj,fieldJBXXjjlxrdh,fieldJBXXxm,fieldJBXXjgsjtdz,fieldSTQKfrtw,fieldMQJCRxm,fieldCXXXsftjhbq,fieldSTQKqtms,fieldCXXXjtfslc,fieldJBXXlxfs,fieldJBXXxb,fieldCXXXjtfspc,fieldYQJLsfjcqtbl,fieldCXXXssh,fieldJBXXgh,fieldCNS,fieldYC,fieldSTQKfl,fieldCXXXsftjwh,fieldCXXXfxxq,fieldSTQKdqstzk,fieldSTQKhxkn,fieldSTQKqtqksm,fieldFLid,fieldYQJLjrsfczbl,fieldJBXXjjlxr,fieldCXXXfxcfsj,fieldMQJCRcjdd,fieldSQSJ,fieldSTQKfrsjrq,fieldSTQKks,fieldJBXXcsny,fieldSTQKgm,fieldJBXXnj,fieldCXXXjtzzq,fieldJBXXJG,fieldCXXXdqszd,fieldCXXXjtzzs,fieldSTQKfx,fieldSTQKfs,fieldCXXXjtfsdb,fieldCXXXcxzt,fieldCXXXjtfshc,fieldCXXXjtjtzz,fieldCXXXsftjhbs,fieldJBXXsfzh,fieldSTQKsfstbs,fieldCXXXcqwdq,fieldJBXXfdygh,fieldJBXXjgshi,fieldJBXXfdyxm,fieldCXXXjtzz,fieldJBXXjgq,fieldCXXXjtfsqt,fieldJBXXjgs,fieldSTQKfrsjsf,fieldSTQKglsjsf,fieldJBXXdw,fieldCXXXsftjhbjtdz,fieldMQJCRlxfs",
            "csrfToken": csrfToken,
            "lang": "zh"
        }
        jkrb5_res = sess.post(jkrb5_url, jkrb5_data)
        
        ret = dict(time_str=time.asctime(time.localtime(time.time())), form_url=jkrb3_url, submit_json=jkrb5_res.json())
        print(ret)
        return ret
    except:
        print(stuid+" error\n")
        return dict(error_msg=traceback.format_exc().strip().split("\n"))

def handler(event, context):
    res = list()
    with open("config.txt") as f:
        for line in f:
            if line:
                row = line.strip().split()
                res.append(dict(id=row[0], json=fill_jkrb(row[0], row[1])))
    return None

if __name__ == "__main__":
    handler(None, None)