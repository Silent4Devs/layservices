import smbclient
import os
from dotenv import load_dotenv

class SMBClient:
    def __init__(self, username: str, password: str, server: str, share: str):
        self.username = username
        self.password = password
        self.server = server
        self.share = share
        self.path = fr"\\{self.server}\{self.share}"
        smbclient.ClientConfig(username=self.username, password=self.password)

    def listFiles(self):
        try:
            files = smbclient.listdir(self.path)
            print("Archivos en el directorio:", files)
            return files
        except Exception as e:
            print(f"Error: {e}")
            return []

if __name__ == "__main__":
    load_dotenv()

    username = os.getenv("SMB_USERNAME")
    password = os.getenv("SMB_PASSWORD")
    server = os.getenv("SMB_SERVER")
    share = os.getenv("SMB_SHARE")

    if not all([username, password, server, share]):
        print("Error: No se encontraron todas las variables de entorno necesarias.")
    else:
        smb_client = SMBClient(username, password, server, share)
        smb_client.listFiles()
