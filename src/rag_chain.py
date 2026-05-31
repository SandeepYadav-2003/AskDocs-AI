from typing import List, Dict, Any
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate
from google import genai

class RAGChainManager:
    """
    Manages the RAG generation pipeline.
    Combines the user query and retrieved document context into a strict prompt
    and generates answers using Google Gemini's API.
    Supports a Hybrid Mode: acts as standard ChatGPT for general queries/greetings,
    and grounds itself strictly in document context with citations when documents are uploaded.
    """
    
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("Google Gemini API Key must be provided.")
            
        self.api_key = api_key
        self.temperature = 0.5  # Slightly higher for standard conversational flexibility
        self.max_tokens = 1024
        
        # Start with the verified active modern model
        self.active_model = "gemini-2.5-flash"
        
        # Initialize modern GenAI client
        self.client = genai.Client(api_key=api_key)
        
        # Design intelligent hybrid system prompt
        self.prompt_template = PromptTemplate(
            input_variables=["context", "question"],
            template="""You are AskDocs AI, a highly intelligent, conversational, and advanced document intelligence assistant.

=== BEHAVIOR RULES ===
1. **Developer Identity:** If anyone asks who developed you, who your creator is, who built you, or who programmed you, you must proudly and explicitly respond with: "Hello! I am AskDocs AI, a document intelligence assistant developed by the talented engineer **Sandeep Yadav**."
2. **Conversational Flexibility (ChatGPT Mode):** If no document context is provided (e.g. context is empty or conversational greeting is received), you can answer greetings (like 'hi', 'hello'), engage in casual conversation, explain general concepts, write code, or answer general knowledge questions using your broad knowledge base.
3. **Context-Grounded Priority (RAG Mode):** If a document context is provided below and the user's question relates to the uploaded documents, prioritize and base your answer strictly on the retrieved context. Cite the source files and page numbers (e.g., "[Source: file.pdf, Page X]") to make your statements verifiable.
4. **Strict Hallucination Prevention:** If the user is asking a query about the uploaded documents, but the exact information needed to answer the question is not present in the retrieved context, you MUST reply exactly: "I could not find this information in the uploaded document." Do not try to make up answers, guess, or use external knowledge to answer document-specific queries when context is provided.

=== RETRIEVED CONTEXT ===
{context}

=== USER QUESTION ===
{question}

=== YOUR PRECISE ANSWER ===
"""
        )

    def _invoke_with_fallback(self, prompt: str) -> str:
        """
        Attempts to generate content using the active model, and falls back to other 
        supported Gemini models if a 404 NOT_FOUND or 429 error occurs using the modern GenAI SDK.
        """
        models_to_try = [
            self.active_model,
            "gemini-2.5-flash",
            "gemini-2.0-flash",
            "gemini-2.5-pro",
            "gemini-2.0-flash-lite"
        ]
        
        # Remove duplicates while preserving list order
        seen = set()
        candidate_models = [m for m in models_to_try if not (m in seen or seen.add(m))]
        
        last_exception = None
        
        for model_name in candidate_models:
            try:
                from google.genai import types
                
                config = types.GenerateContentConfig(
                    temperature=self.temperature,
                    max_output_tokens=self.max_tokens
                )
                
                response = self.client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config=config
                )
                
                # Success! Cache this working model name for subsequent queries
                self.active_model = model_name
                return response.text
            except Exception as e:
                error_msg = str(e).lower()
                
                # Check if this model is unsupported, not found, or has 0 quota
                is_unsupported = any(term in error_msg for term in [
                    "not_found", "not found", "404", "supported", "limit: 0", "limit:0", 
                    "quota exceeded", "resource_exhausted", "429"
                ])
                
                if is_unsupported:
                    last_exception = e
                    continue
                else:
                    # For other errors, raise immediately
                    raise e
                    
        # If all candidates failed, raise the last exception
        raise RuntimeError(
            f"All available Gemini models failed or are unsupported on your API key. "
            f"Please verify your API key is active. Last error: {str(last_exception)}"
        )

    def _format_context(self, retrieved_chunks: List[Document]) -> str:
        """
        Formats retrieved document chunks into a single readable string with metadata boundaries.
        """
        if not retrieved_chunks:
            return "No document chunks retrieved. (Conversational mode active. Answer general questions.)"
            
        formatted_blocks = []
        for idx, doc in enumerate(retrieved_chunks):
            source = doc.metadata.get("source", "Unknown Document")
            page = doc.metadata.get("page", "Unknown Page")
            
            block = f"--- Chunk {idx + 1} | Source: {source} (Page {page}) ---\n"
            block += doc.page_content
            formatted_blocks.append(block)
            
        return "\n\n".join(formatted_blocks)

    def generate_answer(self, question: str, retrieved_chunks: List[Document]) -> str:
        """
        Formats the context, applies the strict prompt, and requests an answer from Gemini.
        """
        context_str = self._format_context(retrieved_chunks)
        prompt_str = self.prompt_template.format(context=context_str, question=question)
        
        try:
            return self._invoke_with_fallback(prompt_str)
        except Exception as e:
            raise RuntimeError(f"Error generating answer from Gemini API: {str(e)}")

    def generate_summary(self, documents: List[Document]) -> str:
        """
        Generates a concise, high-level summary of the uploaded document(s).
        """
        if not documents:
            return "No documents available to summarize."
            
        # Combine first few pages of text (up to ~3000 words) for summarization
        sampled_text = ""
        total_chars = 0
        for doc in documents:
            if total_chars + len(doc.page_content) > 12000:
                # Add partial content and break to stay within reasonable summary token limits
                sampled_text += doc.page_content[:12000 - total_chars]
                break
            sampled_text += f"\n--- {doc.metadata.get('source')} (Page {doc.metadata.get('page')}) ---\n"
            sampled_text += doc.page_content
            total_chars += len(doc.page_content)
            
        summary_prompt = f"""You are AskDocs AI. Provide a high-quality, professional document summary of the following content.
Structure your response exactly using these sections:

Summary:
[A concise overview of the document's main focus and purpose.]

Key Points:
1. [Key Point 1]
2. [Key Point 2]
3. [Key Point 3]
4. [Key Point 4]

Important Terms:
1. **[Term 1]**: [Definition/Explanation]
2. **[Term 2]**: [Definition/Explanation]
3. **[Term 3]**: [Definition/Explanation]

=== DOCUMENT CONTENT ===
{sampled_text}

=== SUMMARY ===
"""
        try:
            return self._invoke_with_fallback(summary_prompt)
        except Exception as e:
            raise RuntimeError(f"Error generating summary: {str(e)}")
