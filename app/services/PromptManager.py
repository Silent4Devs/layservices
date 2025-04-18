import os

class PromptManager:
    def __init__(self):
        # Route to the the prompts folder
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 
        self.templates_dir = os.path.join(project_root, 'prompts') 

    def get_prompt_file(self, file_name: str) -> str:
        """
        Return the prompt template by reading from a file inside the prompts folder.
        """
        try:
            file_path = os.path.join(self.templates_dir, file_name)

            if not os.path.exists(file_path):
                raise FileNotFoundError(f"El archivo {file_path} no se encontró.")

            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        
        except Exception as e:
            return f"Error al obtener el template: {str(e)}"