import os
import subprocess

def execute_dns_zone_transfer(domain_name, base_dir, ip):
    # Créer le répertoire scan_zonedns s'il n'existe pas
    scan_zonedns_dir = os.path.join(base_dir, "scan_zonedns")
    if not os.path.exists(scan_zonedns_dir):
        os.makedirs(scan_zonedns_dir)

    # Définir le fichier de sortie
    output_file = os.path.join(scan_zonedns_dir, f"{ip}-zonedns.txt")

    # Exécuter la commande dig axfr
    command = ["dig", "axfr", domain_name, f"@{ip}"]
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        with open(output_file, 'w') as f:
            f.write(result.stdout)
        print(f"Résultat du transfert de zone DNS pour {domain_name} écrit dans {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution de la commande dig: {e}")
        print(f"Commande : {' '.join(command)}")
        print(f"Code de sortie : {e.returncode}")
        print(f"Message d'erreur : {e.stderr}")