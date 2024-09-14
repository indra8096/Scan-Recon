import os
import subprocess
import json

def get_content_length(ip, host):
    command = ["curl", "-s", "-I", f"http://{ip}", "-H", f"HOST: {host}"]
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        for line in result.stdout.splitlines():
            if "Content-Length:" in line:
                return int(line.split(":")[1].strip())
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution de la commande curl: {e}")
        print(f"Commande : {' '.join(command)}")
        print(f"Code de sortie : {e.returncode}")
        print(f"Message d'erreur : {e.stderr}")
    return None

def fuzz_vhosts(ip, domain, namelist_path, content_length, output_file):
    command = [
        "ffuf", "-w", f"{namelist_path}:FUZZ", "-u", f"http://{ip}/",
        "-H", f"Host:FUZZ.{domain}", "-fs", str(content_length), "-o", output_file, "-of", "json"
    ]
    try:
        subprocess.run(command, check=True)
        print(f"Résultats du fuzzing stockés dans {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution de la commande ffuf: {e}")
        print(f"Commande : {' '.join(command)}")
        print(f"Code de sortie : {e.returncode}")
        print(f"Message d'erreur : {e.stderr}")

def write_fuzzing_results_to_text(output_file, text_output_file):
    try:
        with open(output_file, 'r') as f:
            data = json.load(f)
            with open(text_output_file, 'w') as txt_file:
                txt_file.write(f"Résultats du fuzzing pour {output_file}:\n")
                for result in data['results']:
                    txt_file.write(f"Host: {result['host']}, Status: {result['status']}, Length: {result['length']}, Words: {result['words']}, Lines: {result['lines']}, Content-Type: {result['content-type']}\n")
        print(f"Résultats du fuzzing écrits dans {text_output_file}")
    except Exception as e:
        print(f"Erreur lors de la lecture ou de l'écriture du fichier de résultats: {e}")

def run_fuzzing(ip, domain, namelist_path, base_dir):
    # Obtenir la taille de la réponse pour un hôte non valide
    invalid_host = f"defnotvalid.{domain}"
    content_length = get_content_length(ip, invalid_host)
    if content_length is None:
        print(f"Impossible d'obtenir la taille de la réponse pour l'hôte non valide pour l'IP {ip}.")
        return False

    print(f"Taille de la réponse pour l'hôte non valide : {content_length}")

    # Définir les fichiers de sortie
    fuzzing_dir = os.path.join(base_dir, "fuzzing")
    if not os.path.exists(fuzzing_dir):
        os.makedirs(fuzzing_dir)
    output_file = os.path.join(fuzzing_dir, f"{domain}-fuzz.json")
    text_output_file = os.path.join(fuzzing_dir, f"{domain}-fuzz.txt")

    # Fuzzer les vhosts
    fuzz_vhosts(ip, domain, namelist_path, content_length, output_file)
    
    # Écrire les résultats du fuzzing dans un fichier texte
    write_fuzzing_results_to_text(output_file, text_output_file)
    return True