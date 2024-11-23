import paramiko

ssh_client =paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(hostname="124.43.130.145",username="super",password="T60@t$MerAcs", port=20002)

ftp_client=ssh_client.open_sftp()
ftp_client.get('/home/super/pytesttextfile.txt','D:\BIN 2022\pytesttextfile.txt')
ftp_client.close()