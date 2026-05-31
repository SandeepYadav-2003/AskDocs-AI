import re
from typing import List, Dict, Any, Union, BinaryIO
from pypdf import PdfReader
from langchain_core.documents import Document

class PDFLoader:
    """
    Handles PDF loading, text extraction, and basic cleaning.
    Outputs LangChain Document objects with metadata for RAG pipelines.
    """
    
    @staticmethod
    def clean_text(text: str) -> str:
        """
        Cleans extracted PDF text by removing excessive whitespaces and duplicate newlines.
        """
        if not text:
            return ""
        # Replace multiple spaces with a single space
        text = re.sub(r'[ \t]+', ' ', text)
        # Replace 3 or more consecutive newlines with exactly 2 newlines (preserves paragraphs)
        text = re.sub(r'\n{3,}', '\n\n', text)
        return text.strip()

    def load_pdf(self, file_source: Union[str, BinaryIO], filename: str) -> List[Document]:
        """
        Extracts text page-by-page from a PDF file path or file-like object (e.g., BytesIO).
        Returns a list of LangChain Document objects.
        Automatically falls back to Gemini Multimodal OCR if standard extraction yields 0 text.
        """
        documents = []
        pypdf_error = None
        
        try:
            # 1. Try standard PyPDF extraction
            reader = PdfReader(file_source)
            total_pages = len(reader.pages)
            
            for page_idx, page in enumerate(reader.pages):
                page_num = page_idx + 1
                raw_text = page.extract_text() or ""
                cleaned_text = self.clean_text(raw_text)
                
                # Only include pages with actual content
                if cleaned_text:
                    metadata = {
                        "source": filename,
                        "page": page_num,
                        "total_pages": total_pages
                    }
                    documents.append(
                        Document(page_content=cleaned_text, metadata=metadata)
                    )
        except Exception as e:
            pypdf_error = e

        # 2. Trigger Gemini Multimodal OCR Fallback if PyPDF failed or extracted 0 characters
        if not documents:
            import os
            api_key = os.getenv("GEMINI_API_KEY")
            
            if api_key and isinstance(file_source, str) and os.path.exists(file_source):
                try:
                    from google import genai
                    
                    client = genai.Client(api_key=api_key)
                    uploaded_file = client.files.upload(file=file_source)
                    try:
                        # Extract all text page-by-page using gemini-2.5-flash
                        response = client.models.generate_content(
                            model="gemini-2.5-flash",
                            contents=[
                                uploaded_file,
                                "You are an advanced OCR engine. Extract all text page-by-page from this PDF. For each page, start with a line like '--- Page X ---' where X is the page number, followed by the complete verbatim text extracted from that page."
                            ]
                        )
                        extracted_text = response.text
                        
                        # Parse page blocks from response text
                        pages = {}
                        current_page = None
                        
                        # Split on page header delimiters
                        parts = re.split(r'(--- Page \d+ ---)', extracted_text)
                        for part in parts:
                            part_strip = part.strip()
                            match = re.match(r'--- Page (\d+) ---', part_strip)
                            if match:
                                current_page = int(match.group(1))
                            elif current_page is not None and part_strip:
                                pages[current_page] = part_strip
                                
                        # If parsing failed, treat whole response as page 1
                        if not pages:
                            pages[1] = extracted_text
                            
                        # Build Document objects
                        total_pages = len(pages)
                        for page_num, page_text in sorted(pages.items()):
                            cleaned_text = self.clean_text(page_text)
                            if cleaned_text:
                                metadata = {
                                    "source": filename,
                                    "page": page_num,
                                    "total_pages": total_pages,
                                    "ocr_processed": True
                                }
                                documents.append(
                                    Document(page_content=cleaned_text, metadata=metadata)
                                )
                    finally:
                        try:
                            client.files.delete(name=uploaded_file.name)
                        except Exception:
                            pass
                except Exception as ocr_err:
                    if pypdf_error:
                        raise RuntimeError(f"Error reading PDF '{filename}': {str(pypdf_error)} (OCR Fallback also failed: {str(ocr_err)})")
            else:
                if pypdf_error:
                    raise RuntimeError(f"Error reading PDF '{filename}': {str(pypdf_error)}")
                    
        return documents

    def load_multiple_pdfs(self, pdf_files: List[Dict[str, Any]]) -> List[Document]:
        """
        Loads multiple PDF files. Expects a list of dictionaries with:
        - "file": path or file-like object
        - "name": filename
        """
        all_documents = []
        for doc_info in pdf_files:
            docs = self.load_pdf(doc_info["file"], doc_info["name"])
            all_documents.extend(docs)
        return all_documents
