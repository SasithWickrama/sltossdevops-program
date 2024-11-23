import sys
from send_sms_queue import *

if __name__ == '__main__':

    if sys.argv[1] == 'INITIATE_SMS_COLLECT':
        result_a = collect_sms_a.apply_async(queue='SMS_A', args=["PY_SMS_A"])
        result_b = collect_sms_b.apply_async(queue='SMS_B', args=["PY_SMS_B"])
        result_c = collect_sms_c.apply_async(queue='SMS_C', args=["PY_SMS_C"])
        print(result_a)
        print(result_b)
        print(result_c)


