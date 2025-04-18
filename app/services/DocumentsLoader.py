from typing import List, Dict, Optional
from app.database.FileServer import SMBClient
from app.services.Docling import DocumentProcessor
from app.services.Embeddings import Embeddings
from tqdm import tqdm  
from app.database.Postgres import PostgreSQLManager
from app.models.ProcessedDocument import ProcessedDocument
from prefect import get_run_logger

class DocumentsLoader:

    def __init__(self, folder: str):
        
        self.folder = folder
        self.processor = DocumentProcessor()
        self.embedder = Embeddings()
        self.client = SMBClient(self.folder)
        self.db = PostgreSQLManager()
        
    def _process_document(self, file: str) -> Optional[Dict]:
        
        try:
            org = ""
            folder = "SLA"
            parts = file.replace("\\", "/").split("/")
            if "BD" in parts:
                bd_index = parts.index("BD")
                org = parts[bd_index + 2] if len(parts) > bd_index + 2 else None
                folder = "BD"
            elif "MT" in parts:
                mt_index = parts.index("MT")
                org = parts[mt_index + 1] if len(parts) > mt_index + 1 else None
                folder = "MT"

            raw_content = self.client.get_file(file)
            processed_content = self.processor.getMarkdown(raw_content)
            processed_paragraphs = self.processMarkdown(processed_content)
            embeddings = self.embedder.generateEmbeddings(processed_paragraphs)

            return {
                "payload" : {"folder" : folder, "subfolder" : org, "filename": file.split("/")[-1]},
                "embeddings": embeddings, 
            }

        except Exception as e:
            get_run_logger().info(f"Error processing {file}: {e}")
            return None
                                        
    def load(self) -> List[Dict]:
        
        files = self.client.list_files()
        results = []

        for filepath in files:

            if filepath.endswith((".pdf", ".docx")):

                try:
                    
                    if not self.isSaved(filepath):
                        result = self._process_document(filepath)
                        results.append(result)

                except Exception as e:
                    get_run_logger().info(f"Error processing {filepath}: {e}")
                    continue
                
        return results

    def isSaved(self, file_path : str) -> bool:
        """
        Check if the file is already saved in the database.
        """
        return False
        try:
            with PostgreSQLManager() as session:
                result = session.execute(
                    "SELECT COUNT(*) FROM documents WHERE checksum = :checksum",
                    {"checksum": file_path}
                ).scalar()
            return result > 0
        except Exception as e:
            print(f"Error checking file existence: {e}")
            return False
    
    def processMarkdown(self, markdown: str) -> list[str]:
       
        def joinParagraphs(parrafos: list[str], max_palabras: int = 500) -> list[str]:
            resultado = []
            i = 0
            while i < len(parrafos):
                actual = parrafos[i]
                if i + 1 < len(parrafos):
                    siguiente = parrafos[i + 1]
                    combinado = f"{actual} {siguiente}"
                    if len(combinado.split()) <= max_palabras:
                        resultado.append(combinado)
                        i += 2  
                        continue
                
                resultado.append(actual)
                i += 1
            return resultado

        lineas = markdown.splitlines()
        lineas_filtradas = [linea for linea in lineas if '<!-- image -->' not in linea]
        
        contenido_filtrado = "\n".join(lineas_filtradas)
        parrafos = [p.strip() for p in contenido_filtrado.split('\n\n') if p.strip()]
        
        parrafos_unidos = joinParagraphs(parrafos)
        return parrafos_unidos
