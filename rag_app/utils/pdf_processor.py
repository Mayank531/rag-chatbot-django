import fitz
import pdfplumber
import os
from PIL import Image
import io
import base64
from typing import List, Tuple, Dict

class PDFProcessor:
    def __init__(self, pdf_path: str, output_dir: str):
        self.pdf_path = pdf_path
        self.output_dir = output_dir
        self.text_chunks = []
        self.images = []
        os.makedirs(output_dir, exist_ok=True)

    def extract(self) -> Tuple[List[Tuple[str, Dict]], List[Tuple[str, Dict]]]:
        doc = fitz.open(self.pdf_path)

        # Extract text and images
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text = page.get_text()
            self._chunk_text(text, page_num, "text")

            # Extract images
            image_list = page.get_images()
            for img_index, img in enumerate(image_list):
                xref = img[0]
                pix = fitz.Pixmap(doc, xref)
                if pix.n - pix.alpha < 4:
                    img_path = os.path.join(self.output_dir, f"page_{page_num}_img_{img_index}.png")
                    pix.save(img_path)
                    self.images.append((img_path, {"page": page_num, "type": "image"}))
                pix = None

        # Extract tables
        with pdfplumber.open(self.pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages):
                tables = page.extract_tables()
                for table in tables:
                    if table:
                        table_text = self._table_to_text(table)
                        self._chunk_text(table_text, page_num, "table")

        doc.close()
        return self.text_chunks, self.images

    def _chunk_text(self, text: str, page_num: int, chunk_type: str):
        chunk_size = 500
        overlap = 50
        for i in range(0, len(text), chunk_size - overlap):
            chunk = text[i:i + chunk_size]
            if len(chunk.strip()) > 50:
                self.text_chunks.append((chunk, {"page": page_num + 1, "type": chunk_type}))

    def _table_to_text(self, table):
        return "\n".join([" | ".join([cell or "" for cell in row]) for row in table])