import sys
from celeryQueue import *

if __name__ == '__main__':

    if sys.argv[1] == 'INITIATE':
        result = initiate_task.apply_async(queue='initiate', args=["1000"])
        print(result)
        print(result.get(timeout=1))


    if sys.argv[1] == 'START':
        result = start_task.apply_async(queue='start',)
        print(result)

    if sys.argv[1] == 'PROCESS':
        result = process_task.apply_async(queue='process')
        print(result)

    if sys.argv[1] == 'CLOSE':
        result = close_task.apply_async(queue='close')
        print(result)
