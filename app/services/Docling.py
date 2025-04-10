import json
import yaml
from pathlib import Path
from docling.backend.pypdfium2_backend import PyPdfiumDocumentBackend
from docling.datamodel.base_models import InputFormat
from docling.document_converter import (
    DocumentConverter,
    PdfFormatOption,
    WordFormatOption,
)
from docling.pipeline.simple_pipeline import SimplePipeline
from docling.pipeline.standard_pdf_pipeline import StandardPdfPipeline
from io import BytesIO
import tempfile
from pathlib import Path
from typing import List

class DocumentProcessor:
    def __init__(self, input_paths : str = "", output_dir="scratch"):
        self.input_paths = input_paths
        self.output_dir = Path(output_dir)
        self.doc_converter = self.configureDocumentConverter()

    def configureDocumentConverter(self):
        return DocumentConverter(
            allowed_formats=[
                InputFormat.PDF,
                InputFormat.IMAGE,
                InputFormat.DOCX,
                InputFormat.HTML,
                InputFormat.PPTX,
                InputFormat.ASCIIDOC,
                InputFormat.CSV,
                InputFormat.MD,
            ], 
            format_options={
                InputFormat.PDF: PdfFormatOption(
                    pipeline_cls=StandardPdfPipeline, backend=PyPdfiumDocumentBackend
                ),
                InputFormat.DOCX: WordFormatOption(
                    pipeline_cls=SimplePipeline 
                ),
            },
        )

    def processDocuments(self):
        self.output_dir.mkdir(exist_ok=True)
        conv_results = self.doc_converter.convert_all(self.input_paths)

        for res in conv_results:
            self.saveJson(res)
            self.saveYaml(res)
            self.saveMarkdown(res)

    def saveMarkdown(self, res):
        md_output_path = self.output_dir / f"{res.input.file.stem}.md"
        with md_output_path.open("w", encoding="utf-8") as fp:
            fp.write(res.document.export_to_markdown())

    def saveJson(self, res):
        json_output_path = self.output_dir / f"{res.input.file.stem}.json"
        with json_output_path.open("w", encoding="utf-8") as fp:
            json.dump(res.document.export_to_dict(), fp, ensure_ascii=False, indent=4)

    def saveYaml(self, res):
        yaml_output_path = self.output_dir / f"{res.input.file.stem}.yaml"
        with yaml_output_path.open("w", encoding="utf-8") as fp:
            yaml.safe_dump(res.document.export_to_dict(), fp)
        
    def getMarkdown(self, file: BytesIO | bytes) -> str:
        """
        Converts an file (PDF, DOCX, etc.) to Markdown format and returns it as a string.
        
        Args:
            file (BytesIO or bytes): The file to convert.
        
        Returns:
            str: The content converted to Markdown format.
        """
        with tempfile.NamedTemporaryFile(delete=True) as temp_file:
        
            if isinstance(file, BytesIO):
                content = file.getvalue()
            else:
                content = file
            
            temp_file.write(content)
            temp_file.flush()
            
            conv_results = self.doc_converter.convert(temp_file.name)
            
            if not conv_results:
                raise ValueError("Error en la conversión")
            
            return conv_results.document.export_to_markdown()
        
    def getParagraphsFromMarkdown(self, markdown_text: str) -> List[str]:
        """
        Splits a Markdown string into paragraphs.

        Args:
            markdown_text (str): The input Markdown-formatted text.

        Returns:
            List[str]: A list of paragraphs.
        """
        paragraphs = [p.strip() for p in markdown_text.split("\n\n") if p.strip()]
        return paragraphs