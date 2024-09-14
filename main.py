import os

from ftp import connexion_ftp, brute_force_ftp
from ssh import connexion_ssh, brute_force_ssh
from nmap_scan import scan_nmap
from zone_transfer_DNS import execute_dns_zone_transfer 


def main():
    # Demander le nom de la société
    company_name = input("Entrez le nom de la société : ")
    base_dir = f"result_{company_name}"

    domain_name = input("Entrez le nom de domaine : ")

    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    # Créer les sous-dossiers "scan_nmap", "ftp", et "ssh" dans le dossier parent
    scan_nmap_dir = os.path.join(base_dir, "scan_nmap")

    if not os.path.exists(scan_nmap_dir):
        os.makedirs(scan_nmap_dir)

    # Demander le chemin du fichier contenant les IPs à scanner
    fichier_ips = input("Entrez le chemin du fichier contenant les IPs à scanner : ")

    # Lire les IPs à partir d'un fichier
    with open(fichier_ips, 'r') as f:
        ips = f.read().splitlines()

    # Scanner chaque IP
    for ip in ips:
        print(f"Scanning {ip}...")
        output_file = os.path.join(scan_nmap_dir, f"{ip}-nmap.txt")
        # stock le resultat du scan nmap dans la variable scan_result
        scan_result = scan_nmap(ip, output_file)
        print(f"Résultat du scan pour {ip} écrit dans {output_file}")

        # Exécuter le transfert de zone DNS
        execute_dns_zone_transfer(domain_name, base_dir, ip)

if __name__ == "__main__":
    main()