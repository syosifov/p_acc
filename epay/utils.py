import base64
from decimal import Decimal
import time
import hmac
import hashlib

from .models import EpayRequest, Merchant
from .serializers import EpayRequestSerializer


def b64_encode(message: str, cp: str = 'utf-8'):
    message_bytes = message.encode(cp)
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode(cp)
    return base64_message


def b64_decode(b64_message: str, cp: str = 'utf-8'):
    b64_message_bytes = b64_message.encode(cp)
    message_bytes = base64.b64decode(b64_message_bytes)
    message = message_bytes.decode(cp)
    return message


def hash_sha1(key: str, message: str, cp: str = 'utf-8'):
    # https://www.adamsmith.haus/python/examples/1953/hmac-construct-a-new-hmac-hash-using-the-sha1-algorithm
    
    h = hmac.new(key.encode(cp), msg=message.encode(cp), digestmod=hashlib.sha1)
    return h.hexdigest()

    

def prepare_payment(min: str, 
                    amount: Decimal, 
                    descr: str, 
                    invoice_numb: str,
                    exp_in_sec: int,
                    exp_at: str = '',
                    encoding: str = 'utf-8'):
    
    if not invoice_numb.isdigit():
        raise Exception("Invoice number must contain only digits")
    merchant = Merchant.objects.get(min=min)
    secret = merchant.secret
    seconds = time.time()
    s2 = seconds + exp_in_sec
    st = time.localtime(s2)
    exp_time = time.strftime("%d.%m.%Y %H:%M:%S", st)

    if not exp_at == '':
        exp_time = exp_at
    
    
    s = f'''MIN={min}
INVOICE={invoice_numb}
AMOUNT={amount}
EXP_TIME={exp_time}
DESCR={descr}
ENCODING={encoding}
'''
    print()
    print(s,"\n\n")
    encoded = b64_encode(s)
    check_sum = hash_sha1(secret, encoded)

    epayRequest = EpayRequest(min,
                              invoice_numb,
                              str(amount),
                              exp_time,
                              descr,
                              encoded,
                              check_sum)
    serializer = EpayRequestSerializer(epayRequest)
    
    print("\nserializer.data\n",serializer.data,"\n\n")
    
    return serializer.data
