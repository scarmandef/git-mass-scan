import requests
import argparse
from bs4 import BeautifulSoup

VERMELHO = "\033[1;31m"
VERDE = "\033[92m"
BRANCO = "\033[0;0m"
AMARELO = "\033[1;93m"
CLARO = "\033[93m"

parser = argparse.ArgumentParser(usage='gitscan.py -h for help -t hosts.txt -f git or env -o results.txt', description='mass scan for .GIT and .ENV repository exposure')
parser.add_argument('-t', help= VERDE + 'Load the file with the targets. '
                             + CLARO +  'Example: hosts.txt || /home/user/Desktop/hosts.txt' + BRANCO, required=True)
parser.add_argument('-f', help= VERDE + 'Choose git or env function' + BRANCO, required=True)
parser.add_argument('-o', help= VERDE + 'Place the file to be saved.'
                              + CLARO + '\n' + ' Example: Resultados.txt || /home/user/Desktop/Resultados.txt' + BRANCO, required=True)

args = parser.parse_args()
hosts = str(args.t)
funcao = str(args.f)
output = str(args.o)

try:
    files = open(hosts, 'r', encoding="utf8")
except FileNotFoundError as e:
    print('\n',hosts,'not found, please rate the file name or directory.')
    exit()

resultado = open(output, 'w', encoding="utf8")

content_git = 'ref: refs/heads/master'
content_env = 'APP_NAME=Laravel'

header = {'User-Agent':
            'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0'
          }

def env(file):
    for site in files:
        site = site.rstrip()
        try:
            env = requests.get(site + '/.env', headers=header)
            status_env = BeautifulSoup(env.text, 'html.parser')
            response_env = status_env.text[:16]
            if content_env in response_env:
                resultado.writelines(site + ' - ENV' + '\n')
                print(site, VERDE + '[+] Env found ! [+]' + BRANCO)
            else:
                print(site, VERMELHO + '[-] Env not found ! [-]' + BRANCO)
        except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError) as e:
            print(site, AMARELO + '[-] Invalid url or site down [-]' + BRANCO)

def git(file):
    for site in files:
        site = site.rstrip()
        try:
            git = requests.get(site + '/.git/HEAD', headers=header)
            response_git = git.text
            if content_git in response_git:
                resultado.writelines(site + ' - GIT ' + '\n')
                print(site, VERDE + '[+] Git found ! [+]' + BRANCO)
            else:
                print(site, VERMELHO + '[-] Git not found ! [-]' + BRANCO)
        except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError) as e:
            print(site, AMARELO + '[-] Invalid url or site down [-]' + BRANCO)

if funcao == 'git':
     git(hosts)
elif funcao == 'env':
     env(hosts)
else:
    print(VERMELHO + '[-] Invalid function [-]' + BRANCO)

resultado.close()
files.close()
