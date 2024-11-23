
from ldap3 import Server, Connection, ALL, SUBTREE
from ldap3.core.exceptions import LDAPException, LDAPBindError


def global_ldap_authentication(user_name, user_pwd):
    """
      Function: global_ldap_authentication
       Purpose: Make a connection to encrypted LDAP server.
       :params: ** Mandatory Positional Parameters
                1. user_name - LDAP user Name
                2. user_pwd - LDAP User Password
       :return: None
    """

    # fetch the username and password
    ldap_user_name = user_name.strip()+'@intranet.slt.com.lk'
    ldap_user_pwd = user_pwd.strip()

    # ldap server hostname and port
    ldsp_server = f"ldap://intranet.slt.com.lk:389"


    server = Server(ldsp_server, get_info=ALL)

    connection = Connection(server,
                            user=ldap_user_name,
                            password=ldap_user_pwd)
    if connection.bind():
        print(f" *** Successful bind to ldap server")
        l_success_msg = 'Success'
       
        connection.search('DC=intranet,DC=slt,DC=com,DC=lk',
                      "(&(objectClass=person)(sAMAccountName=" + user_name + "))",
                      SUBTREE,
                      attributes=['*'])
        #print(connection.response)              
        #for entry in connection.response:
            #print(entry)

        entry = connection.entries
            print(json.loads(entry[0].entry_to_json()))             
       
              
    else:
        print(f" *** Cannot bind to ldap server: {connection.last_error} ")
        l_success_msg = f' ** Failed Authentication: {connection.last_error}'

    return l_success_msg
    
    
aa = global_ldap_authentication('012583', 'AADp$19870120')
print(aa)    