import yaml
def read_db_creds():
    
    with open('db_creds.yaml', 'r') as f:
        credentials_dict = yaml.safe_load(f)
    return credentials_dict

credentials = read_db_creds()

print(credentials)