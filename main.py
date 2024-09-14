import os

from ftp import connexion_ftp, brute_force_ftp
from ssh import connexion_ssh, brute_force_ssh
from nmap_scan import scan_nmap
from zone_transfer_DNS import execute_dns_zone_transfer
from fuzzing import run_fuzzing  # Importer la nouvelle fonction

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
        scan_result = scan_nmap(ip, output_file)
        print(f"Résultat du scan pour {ip} écrit dans {output_file}")

        # Exécuter le transfert de zone DNS
        execute_dns_zone_transfer(domain_name, base_dir, ip)

        # Demander le chemin du fichier contenant les noms à fuzzer
        namelist_path = input("Entrez le chemin du fichier contenant les noms à fuzzer : ")

        # Exécuter le fuzzing des vhosts
        if not run_fuzzing(ip, domain_name, namelist_path, base_dir):
            print(f"Passer l'IP {ip} car elle ne peut pas être associée au nom de domaine.")

if __name__ == "__main__":
    main()