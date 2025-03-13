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


class DocumentProcessor:
    def __init__(self, input_paths, output_dir="scratch"):
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

if __name__ == "__main__":


    input_paths = [
        Path("/home/jonathan/Downloads/herramientas.docx"),
    ]
  
    processor = DocumentProcessor(input_paths)
    processor.processDocuments()