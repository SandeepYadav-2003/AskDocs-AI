import os
import shutil
from typing import List
from langchain_core.documents import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

class VectorStoreManager:
    """
    Manages vector database operations using local ChromaDB and HuggingFace Embeddings.
    Allows zero-cost offline vectorization and semantic similarity queries.
    """
    
    def __init__(self, persist_directory: str = "vector_db"):
        self.persist_directory = persist_directory
        # Use a high-quality, lightweight local sentence transformer model
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={"device": "cpu"}
        )
        self.vector_store = None
        self._init_vector_store()

    def _init_vector_store(self):
        """
        Initializes or loads the persistent ChromaDB collection.
        """
        os.makedirs(self.persist_directory, exist_ok=True)
        self.vector_store = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings,
            collection_name="askdocs_collection"
        )

    def add_documents(self, documents: List[Document]) -> bool:
        """
        Adds a list of chunked Document objects to the local ChromaDB vector store.
        """
        if not documents:
            return False
        
        try:
            self.vector_store.add_documents(documents)
            self.vector_store.persist()  # Ensure persistent write to disk
            return True
        except Exception as e:
            raise RuntimeError(f"Failed to write documents to vector store: {str(e)}")

    def similarity_search(self, query: str, k: int = 4) -> List[Document]:
        """
        Performs a semantic similarity search in ChromaDB.
        Returns the top 'k' matching Document chunks.
        """
        if not self.vector_store:
            return []
        
        try:
            return self.vector_store.similarity_search(query, k=k)
        except Exception as e:
            raise RuntimeError(f"Error during similarity search: {str(e)}")

    def similarity_search_with_score(self, query: str, k: int = 4) -> List[tuple]:
        """
        Performs a semantic similarity search in ChromaDB and returns (Document, score) tuples.
        """
        if not self.vector_store:
            return []
        
        try:
            return self.vector_store.similarity_search_with_score(query, k=k)
        except Exception as e:
            raise RuntimeError(f"Error during similarity search with score: {str(e)}")

    def clear_database(self) -> bool:
        """
        Resets and wipes the local ChromaDB database.
        Useful when the user wants to start over with new documents.
        """
        try:
            # Delete collection contents via Chroma API (safely clears vectors and tables)
            if self.vector_store:
                try:
                    self.vector_store.delete_collection()
                except Exception:
                    pass
                
            # Re-initialize collection to have a clean, ready-to-use vector database
            self._init_vector_store()
            return True
        except Exception as e:
            raise RuntimeError(f"Failed to clear database: {str(e)}")
            
    def get_collection_stats(self) -> dict:
        """
        Returns basic stats about the stored vectors.
        """
        if not self.vector_store:
            return {"total_chunks": 0, "unique_sources": []}
            
        try:
            # Access underlying client to get count
            collection = self.vector_store._collection
            count = collection.count()
            
            # Fetch all metadata to identify unique sources
            results = collection.get(include=["metadatas"])
            sources = set()
            if results and "metadatas" in results:
                for metadata in results["metadatas"]:
                    if metadata and "source" in metadata:
                        sources.add(metadata["source"])
                        
            return {
                "total_chunks": count,
                "unique_sources": list(sources)
            }
        except Exception:
            return {"total_chunks": 0, "unique_sources": []}
