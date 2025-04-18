import smbclient
from config import settings  
from .ConnectionManager import ConnectionManager
import os

class SMBClient(ConnectionManager):

    def __init__(self, folder : str = ""):
        """
        Open an SMB connection and initialize a client.
        """
        
        self.username = settings.SMB_USERNAME
        self.password = settings.SMB_PASSWORD
        self.server = settings.SMB_SERVER
        self.share = settings.SMB_SHARE
        self.path = fr"\\{self.server}\{self.share}\{folder}"
     
        smbclient.ClientConfig(username=self.username, password=self.password)

    def get_client(self):
        """
        Returns the SMB client.

        :return: SMB client instance.
        """
        return smbclient

    def list_files(self):
        """
        Recursively list all files in the SMB share and its subdirectories.

        :return: List of file paths.
        """
        all_files = []

        def walk(directory):
            try:
                entries = smbclient.listdir(directory)
                for entry in entries:
                    full_path = os.path.join(directory, entry)
                    try:
                        if smbclient.stat(full_path).st_mode & 0o170000 == 0o040000:  
                            walk(full_path)
                        else:
                            all_files.append(full_path)
                    except Exception as stat_err:
                        print(f"Error al obtener información de {full_path}: {stat_err}")
            except Exception as list_err:
                print(f"Error al listar {directory}: {list_err}")

        walk(self.path)
        return all_files

    def close_connection(self):
        """
        Close the SMB connection.
        """
 
        print("SMB connection closed.")

    def get_file(self, filepath: str):
        """
        Get a file from the SMB share.

        :param file_name: Name of the file to retrieve.
        :return: File content.
        """
        try:
            with smbclient.open_file(fr"{filepath}", mode='rb') as file:
                return file.read()
        except Exception as e:
            print(f"Error: {e}")
            return None
