from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

class DocumentChunker:
    """
    Handles chunking of extracted document texts.
    Uses RecursiveCharacterTextSplitter to create logically bounded overlapping text blocks.
    """
    
    def __init__(self, chunk_size: int = 800, chunk_overlap: int = 100):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )

    def split_documents(self, documents: List[Document]) -> List[Document]:
        """
        Splits a list of LangChain Document objects into smaller chunks.
        Keeps all metadata from the original document intact.
        """
        if not documents:
            return []
        
        chunks = self.splitter.split_documents(documents)
        
        # Add index metadata to each chunk to help with ordering and reference
        for idx, chunk in enumerate(chunks):
            chunk.metadata["chunk_index"] = idx
            
        return chunks
