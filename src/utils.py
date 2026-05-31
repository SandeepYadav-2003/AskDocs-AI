import os
import shutil
from typing import List, Dict, Any
from langchain_core.documents import Document
from langchain_google_genai import ChatGoogleGenerativeAI

class RAGUtilities:
    """
    Utility helpers for file management, chat exports, and LLM suggestions.
    """
    
    def __init__(self, upload_dir: str = "data/uploaded_docs"):
        self.upload_dir = upload_dir
        os.makedirs(self.upload_dir, exist_ok=True)

    def save_uploaded_file(self, uploaded_file) -> str:
        """
        Saves a Streamlit uploaded file to the local data/uploaded_docs directory.
        Returns the absolute path to the saved file.
        """
        try:
            file_path = os.path.join(self.upload_dir, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            return file_path
        except Exception as e:
            raise RuntimeError(f"Failed to save uploaded file '{uploaded_file.name}': {str(e)}")

    def clear_uploads(self) -> bool:
        """
        Clears all saved files in the uploaded_docs directory.
        """
        try:
            if os.path.exists(self.upload_dir):
                shutil.rmtree(self.upload_dir)
            os.makedirs(self.upload_dir, exist_ok=True)
            return True
        except Exception as e:
            raise RuntimeError(f"Failed to clear upload directory: {str(e)}")

    @staticmethod
    def export_chat_to_markdown(chat_history: List[Dict[str, str]]) -> str:
        """
        Formats the chat history into a professional Markdown transcript for downloading.
        """
        if not chat_history:
            return ""
            
        md_lines = [
            "# AskDocs AI - Chat Session Transcript",
            "Generated on: 2026-05-31 (Local Time)",
            "\n---\n"
        ]
        
        for msg in chat_history:
            role = "👤 **User**" if msg["role"] == "user" else "🤖 **AskDocs AI**"
            content = msg["content"]
            md_lines.append(f"### {role}")
            md_lines.append(f"{content}\n")
            
        return "\n".join(md_lines)

    @staticmethod
    def generate_question_suggestions(api_key: str, documents: List[Document]) -> List[str]:
        """
        Queries Gemini to suggest 3-4 intelligent questions based on the uploaded document contents.
        """
        if not api_key or not documents:
            return [
                "What are the main topics discussed in this document?",
                "Can you summarize the core findings of this file?",
                "What are the key conclusions or recommendations?"
            ]
            
        # Compile a small text sample from the first few pages
        sample_text = ""
        for doc in documents[:5]:
            sample_text += doc.page_content[:1000] + "\n"
            
        prompt = f"""You are AskDocs AI. Read the text sample below and generate exactly 3 distinct, highly specific, and analytical questions that a professional would ask about this document. 
Return ONLY the questions as a bulleted list. Do not include introductory or concluding remarks.

=== TEXT SAMPLE ===
{sample_text}

=== 3 SPECIFIC QUESTIONS ===
"""
        try:
            llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash",
                google_api_key=api_key,
                temperature=0.7,
                max_tokens=256
            )
            response = llm.invoke(prompt)
            lines = response.content.strip().split("\n")
            
            questions = []
            for line in lines:
                # Clean up bullet points (-, *, 1., 2., etc.)
                clean_line = line.strip()
                clean_line = re.sub(r'^[\s\-\*\d\.\)]+', '', clean_line).strip()
                if clean_line and clean_line.endswith("?"):
                    questions.append(clean_line)
                    
            # Fallback if parsing failed
            if len(questions) < 2:
                raise ValueError("Incomplete question parsing")
                
            return questions[:4]
            
        except Exception:
            return [
                "What are the primary topics covered in the document?",
                "Can you provide a summary of the key findings?",
                "What are the main recommendations or conclusions?"
            ]
