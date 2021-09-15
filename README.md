# Mass .Git repository and .Env file Scan by Scarmandef

Scanner to find .env file and .git repository exposure on multiple hosts

Because of the response code from some hosts, it may have some false positives.

# Requeriments

requests and
argparse

     pip3 install -r requirements.txt

# How to use

Be careful with the output filename as it can be deleted if duplicated

    python3 git_scan.py -t hosts.txt -o results.txt -f git or env 
    
