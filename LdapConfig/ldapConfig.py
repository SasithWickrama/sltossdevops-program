import paramiko
import time
import hashlib
import os

def connectSsh(self,usr,pwd):
    conn = paramiko.SSHClient()
    conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    conn.connect(
        str(self),
        username=usr,
        password=pwd,
        look_for_keys=False,
        allow_agent=False)
    return conn
ldapip= "10.68.74.32"
cust="CEN2395320"
desc="Suspended 08-06-22"
ldappwd="o$Sld@PAdm!N"
conn = connectSsh("172.25.17.194","Administrator","#45Dev@Ops0194")

#conn = connectSsh("172.25.18.196","clarity","clarity#12345")
#stdin, stdout, stderr = conn.exec_command("ldapsearch -h "+ldapip+" -D \"uid="+ldapid+",cn=config\" -w "+ldappwd+" -b \"ou=people,o=auth\" uid="+cust+"")
#stdin, stdout, stderr = conn.exec_command("/clarity/c12app1/etc/ldaprunit.sh /clarity/c12app1/ldapbin/ldapsearch  -b ou=people,o=auth uid=CEN2395320 ")
# stdout = stdout.readlines()
#
# for line in stdout:
#     print(line)

remote_conn = conn.invoke_shell()
remote_conn.send("ldapmodify -h "+ldapip+" -p 389 -D \"uid=OSSUser,cn=config\" -w "+ldappwd+" \n")

#remote_conn.send("/clarity/c12app1/etc/ldaprunit.sh /clarity/c12app1/ldapbin/ldapmodify \n")
remote_conn.send("""dn: uid="""+cust+""", ou=people, o=auth
changetype: modify
replace: sltInactiveStatus
sltInactiveStatus: Suspended
-
replace: inetUserStatus
inetUserStatus: inactive
-
add: description
description: """+desc+"""

\n""")

# remote_conn.send("""dn: uid=CEN2395320, ou=people, o=auth
# changetype: modify
# replace: sltInactiveStatus
# sltInactiveStatus: Resumed
# -
# replace: inetUserStatus
# inetUserStatus: active
# -
# add: description
# description: Test Resume26
#
# ${LF}${LF}${LF} \n""")


remote_conn.send("\n")
time.sleep(5)
output = remote_conn.recv(30000)
print(output.decode("utf-8"))


