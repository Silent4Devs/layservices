import smbclient
from config import settings  
from .ConnectionManager import ConnectionManager

class SMBClient(ConnectionManager):
    def __init__(self):
        """
        Open an SMB connection and initialize a client.
        """
        # Obtener las configuraciones desde Dynaconf
        self.username = settings.SMB_USERNAME
        self.password = settings.SMB_PASSWORD
        self.server = settings.SMB_SERVER
        self.share = settings.SMB_SHARE
        self.path = fr"\\{self.server}\{self.share}"

        # Configurar el cliente SMB
        smbclient.ClientConfig(username=self.username, password=self.password)

    def get_client(self):
        """
        Returns the SMB client.

        :return: SMB client instance.
        """
        return smbclient

    def list_files(self):
        """
        List files in the SMB share.

        :return: List of files.
        """
        try:
            files = smbclient.listdir(self.path)
            print("Archivos en el directorio:", files)
            return files
        except Exception as e:
            print(f"Error: {e}")
            return []

    def close_connection(self):
        """
        Close the SMB connection.
        """
        # smbclient no tiene un método explícito para cerrar la conexión,
        # pero puedes realizar acciones de limpieza si es necesario.
        print("SMB connection closed.")