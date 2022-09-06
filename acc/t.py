import math
import base64
from re import A
import time


def t1():
    n = 3
    i = 1
    s1 = str(i)
    print(s1)
    # s1 = 'aa'
    s = s1.zfill(n)
    print(s)


def t2():
    math.pi = 222
    print(math.pi)


msg = '''message = "Python is fun"
message_bytes = message.encode('ascii')
base64_bytes = base64.b64encode(message_bytes)
base64_message = base64_bytes.decode('ascii')

print(base64_message)message = "Python is fun"
message_bytes = message.encode('ascii')
base64_bytes = base64.b64encode(message_bytes)
base64_message = base64_bytes.decode('ascii')

print(base64_message)message = "Python is fun"
message_bytes = message.encode('ascii')
base64_bytes = base64.b64encode(message_bytes)
base64_message = base64_bytes.decode('ascii')

print(base64_message)message = "Python is fun"
message_bytes = message.encode('ascii')
base64_bytes = base64.b64encode(message_bytes)
base64_message = base64_bytes.decode('ascii')

print(base64_message)'''

msg = "Python is fun"


def b64_encode(message: str):
    message_bytes = message.encode('utf-8')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('utf-8')
    return base64_message


def b64_decode(b64_message: str):
    b64_message_bytes = b64_message.encode('utf-8')
    message_bytes = base64.b64decode(b64_message_bytes)
    message = message_bytes.decode('utf-8')
    return message

# https://stackabuse.com/encoding-and-decoding-base64-strings-in-python/


def encode_decode_test():
    m1 = b64_encode(msg)
    print(m1)

    m2 = b64_decode(m1)
    print(m2)


def hmac_test():
    # https://www.adamsmith.haus/python/examples/1953/hmac-construct-a-new-hmac-hash-using-the-sha1-algorithm
    import hmac
    import hashlib

    h = hmac.new("key".encode('utf-8'), msg="abc".encode('utf-8'),
                 digestmod=hashlib.sha1)
    print(h.hexdigest())


# encode_decode_test()
# hmac_test()

# t1()

def t3():
    print()
    named_tuple = time.localtime() # get struct_time
    print(named_tuple)
    time_string = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)
    print(time_string)
    print()


# t3()

def t4():
    print()
    seconds = time.time()
    seconds = 1662399771.5360272
    seconds = 1662399771
    print("Seconds since epoch =", seconds)
    local_time = time.ctime(seconds)
    print("Local time:", local_time)
    print()
    
    
def t5():
    print()
    seconds = time.time()
    print('seconds',seconds)
    named_tuple = time.localtime(seconds)
    print(named_tuple)
    time_string = time.strftime("%d.%m.%Y, %H:%M:%S", named_tuple)
    print(time_string)
    s2 = seconds + 60 * 60
    nt2 = time.localtime(s2)
    ts2 = time.strftime("%d.%m.%Y, %H:%M:%S", nt2)
    print(ts2)
    print()
    

t5()    
