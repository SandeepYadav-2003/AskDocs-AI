import os
import sys

# Import from local package source
from langchain_core.documents import Document
from src.vector_store import VectorStoreManager

def main():
    print("=== AskDocs AI RAG Verification System ===")
    
    # 1. Initialize Vector Database Manager
    print("\n1. Initializing local ChromaDB and loading HuggingFaceEmbeddings...")
    try:
        # Save db inside verify_db directory
        vstore = VectorStoreManager(persist_directory="verify_db")
        print("[OK] Embeddings model and ChromaDB initialized successfully!")
    except Exception as e:
        print(f"[ERROR] Initialization failed: {str(e)}")
        sys.exit(1)
        
    # 2. Reset database for clean verification
    print("\n2. Wiping existing verify database...")
    vstore.clear_database()
    print("[OK] Database cleared!")
    
    # 3. Create mock documents to index
    print("\n3. Generating mock document chunks...")
    sample_docs = [
        Document(
            page_content="Database Management System (DBMS) is software used to manage databases. It allows users to store, retrieve, update, and delete data efficiently. Main components are database engine, schema, and query processor.",
            metadata={"source": "DBMS_Notes.pdf", "page": 1}
        ),
        Document(
            page_content="Normalization in DBMS is a systematic approach to decomposing tables to eliminate data redundancy (duplication) and undesirable characteristics like insertion, update, and deletion anomalies. Normal forms include 1NF, 2NF, 3NF, and BCNF.",
            metadata={"source": "DBMS_Notes.pdf", "page": 3}
        ),
        Document(
            page_content="Retrieval-Augmented Generation (RAG) is a technique that enhances large language model responses by retrieving relevant information from an external knowledge source before generating the answer. This prevents hallucinations and secures contextual grounding.",
            metadata={"source": "RAG_Research.pdf", "page": 1}
        )
    ]
    print(f"[OK] Generated {len(sample_docs)} test document chunks.")
    
    # 4. Write documents to vector store
    print("\n4. Indexing chunks into local ChromaDB...")
    try:
        success = vstore.add_documents(sample_docs)
        if success:
            print("[OK] Chunks successfully vectorized and stored!")
        else:
            print("[ERROR] Failed to add documents.")
            sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Indexing failed with error: {str(e)}")
        sys.exit(1)
        
    # 5. Test Similarity Search
    print("\n5. Running similarity search query...")
    query = "What is database normalization?"
    print(f"Query: '{query}'")
    
    try:
        results = vstore.similarity_search(query, k=2)
        print(f"[OK] Search completed! Retrieved {len(results)} chunks.")
        
        for idx, doc in enumerate(results):
            source = doc.metadata.get("source")
            page = doc.metadata.get("page")
            print(f"\n--- Result {idx + 1} | Source: {source} (Page {page}) ---")
            print(doc.page_content)
            
        # Quick validation
        if results and "Normalization" in results[0].page_content:
            print("\n[SUCCESS] Local offline embeddings and ChromaDB match expectations!")
        else:
            print("\n[WARNING] Search returned results, but the top result was not the normalization chunk.")
            
    except Exception as e:
        print(f"[ERROR] Similarity search failed: {str(e)}")
        sys.exit(1)
        
    # Clean up test database
    print("\n6. Wiping verification database folder...")
    try:
        import shutil
        if os.path.exists("verify_db"):
            shutil.rmtree("verify_db")
        print("[OK] Cleaned up database folder.")
    except Exception as e:
        print(f"[WARNING] Could not clean up verify_db: {str(e)}")
        
    print("\n=== Verification Finished ===")

if __name__ == "__main__":
    main()
