import nmap

def scan_nmap(ip, output_file):
    nm = nmap.PortScanner()
    print(f"Starting Nmap scan for {ip}...")
    scan_result = nm.scan(ip, arguments=f'-A -p- -sC -sV -v -oN {output_file}')
    print(f"Nmap scan for {ip} completed.")
    return scan_result
