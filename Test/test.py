try:
        with open('test.txt', 'r') as f:
            last_rec = f.readlines()[-1]
        f.close()
        print("last_rec "+last_rec)
        temp = last_rec.split("\t")
        print("temp "+temp[0]+"tt")
        rownum = int(temp[0]) 
        print(rownum +1)
        rownum = rownum +1
        print(type(rownum))
        print("rownum "+rownum)
except Exception as e: 
        print(e)
        rownum = 0



