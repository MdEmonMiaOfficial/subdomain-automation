# enhanced_subdomain_enum.py
import os
import subprocess
from datetime import datetime

# ========== CONFIG ==========
domain = input("Enter the domain (e.g. example.com): ")
wordlist_path = input("Enter path to your wordlist (e.g. wordlist.txt): ")

output_dir = f"./output/{domain}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
os.makedirs(output_dir, exist_ok=True)

# ========== TOOLS ==========
tools = {
    "assetfinder": f"assetfinder --subs-only {domain}",
    "subfinder": f"subfinder -d {domain} -silent",
    "amass": f"amass enum -passive -d {domain}",
    "gau": f"gau {domain}",
    "sublist3r": f"sublist3r -d {domain} -o {output_dir}/sublist3r.txt",
    "findomain": f"findomain -t {domain} -u {output_dir}/findomain.txt",
    "crtsh": f"curl -s https://crt.sh/?q=%25.{domain}\\&output=json | jq -r '.[].name_value' | sed 's/\\*\\.//g' | sort -u > {output_dir}/crtsh.txt",
    "puredns": f"puredns bruteforce {wordlist_path} {domain} -r resolvers.txt -w {output_dir}/puredns.txt"
}

def run_command(name, cmd, outfile):
    print(f"[+] Running {name}...")
    with open(outfile, 'w') as f:
        subprocess.run(cmd, shell=True, stdout=f, stderr=subprocess.DEVNULL)
    print(f"[+] {name} results saved to {outfile}")

# ========== EXECUTE ==========
run_command("Assetfinder", tools["assetfinder"], f"{output_dir}/assetfinder.txt")
run_command("Subfinder", tools["subfinder"], f"{output_dir}/subfinder.txt")
run_command("Amass", tools["amass"], f"{output_dir}/amass.txt")
run_command("gau", tools["gau"], f"{output_dir}/gau.txt")
run_command("Sublist3r", tools["sublist3r"], f"{output_dir}/sublist3r.txt")
run_command("Findomain", tools["findomain"], f"{output_dir}/findomain.txt")
os.system(tools["crtsh"])
os.system(tools["puredns"])

# Merge
final_output = f"{output_dir}/final.txt"
os.system(f"cat {output_dir}/*.txt | sort -u > {final_output}")

# Live check
live_output = f"{output_dir}/live.txt"
os.system(f"cat {final_output} | httpx -silent > {live_output}")

# Screenshots
screenshot_dir = f"{output_dir}/screenshots"
os.makedirs(screenshot_dir, exist_ok=True)
os.system(f"cat {live_output} | aquatone -out {screenshot_dir} -chrome-path /usr/bin/google-chrome")

# Report
subprocess.run(f"python3 generate_report.py '{output_dir}'", shell=True)

print(f"[✔] Recon complete! All data in: {output_dir}")
