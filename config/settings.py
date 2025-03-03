import os

LOGRHYTHM_API = {
    "base_url_log": os.getenv("LOGRHYTHM_API_URL"),
    "token_log": os.getenv("LOGRHYTHM_API_TOKEN")
}

REMEDY_API = {
    "base_url_rem": "https://remedy.silent4business.com/api",
    "username_rem": "",
    "password_rem": ""
}

PRTG_API = {
    "base_url_prtg": os.getenv("PRTG_API_URL"),
    "token_prtg": os.getenv("PRTG_API_TOKEN") 
}

DEFENDER_API = {
    "base_url_def": "https://api.security.microsoft.com",
    "tenant_id_def": "",
    "client_id_def": "",
    "client_secret_def": ""
}

#KAXAN
BASE_URL = os.getenv("KAXAN_API_URL")
HEADERS = {
    "Content-Type": "application/json"
}
