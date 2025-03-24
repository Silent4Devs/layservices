from remedy_py.RemedyAPIClient import RemedyClient
from config.settings import REMEDY_API

class RemedyAPI:
    def __init__(self):
        """Inicializa la conexión con Remedy usando remedy-py"""
        self.client = RemedyClient(
            server=REMEDY_API["base_url_rem"],
            username=REMEDY_API["username_rem"],
            password=REMEDY_API["password_rem"]
        )

    def create_ticket(self, title, description):
        """Crea un nuevo ticket en Remedy"""
        ticket_data = {
            "Title": title,
            "Description": description
        }
        response = self.client.create_entry("HPD:IncidentInterface_Create", ticket_data)
        return response  # Devuelve el ID del ticket o error

    def get_ticket(self, ticket_id):
        """Obtiene los detalles de un ticket"""
        response = self.client.get_entry("HPD:Help Desk", ticket_id)
        return response
