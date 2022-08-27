import math
import base64

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

def b64_encode(message):
    message_bytes = message.encode('utf-8')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('utf-8')
    return base64_message


def b64_decode(b64_message):
    b64_message_bytes = b64_message.encode('utf-8')
    message_bytes = base64.b64decode(b64_message_bytes)
    message = message_bytes.decode('utf-8')
    return message


def encode_decode_test():
    m1 = b64_encode(msg)
    print(m1)

    m2 = b64_decode(m1)
    print(m2)

encode_decode_test()