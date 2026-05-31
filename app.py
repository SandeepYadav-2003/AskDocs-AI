import os
import streamlit as st
from dotenv import load_dotenv

# Ensure the local src/ modules are importable
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from src.pdf_loader import PDFLoader
from src.text_splitter import DocumentChunker
from src.vector_store import VectorStoreManager
from src.rag_chain import RAGChainManager
from src.utils import RAGUtilities
from src.styles import get_theme_css, CUSTOM_CSS

# Load environment variables
load_dotenv()

# Load profile picture base64
import base64
def get_base64_image(file_path):
    if os.path.exists(file_path):
        try:
            with open(file_path, "rb") as f:
                return base64.b64encode(f.read()).decode("utf-8")
        except Exception:
            return None
    return None

profile_pic_path = os.path.join(os.path.dirname(__file__), "data", "profile_pic.jpg")
profile_pic_base64 = get_base64_image(profile_pic_path)


# Set Page Config with custom title and icon
st.set_page_config(
    page_title="AskDocs AI - Personal Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session States
if "active_page" not in st.session_state:
    st.session_state.active_page = "home"
if "active_theme" not in st.session_state:
    st.session_state.active_theme = "Amethyst Violet"
if st.session_state.get("active_theme") == "Minimalist Light":
    st.session_state.active_theme = "Amethyst Violet"
if "chunk_size" not in st.session_state:
    st.session_state.chunk_size = 800
if "chunk_overlap" not in st.session_state:
    st.session_state.chunk_overlap = 100
if "llm_temp" not in st.session_state:
    st.session_state.llm_temp = 0.5

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "processed_docs" not in st.session_state:
    st.session_state.processed_docs = []
if "question_suggestions" not in st.session_state:
    st.session_state.question_suggestions = [
        "Summarize active documents",
        "Explain key terms",
        "List main takeaways"
    ]
if "raw_docs" not in st.session_state:
    st.session_state.raw_docs = []
if "last_sources" not in st.session_state:
    st.session_state.last_sources = []
if "last_confidence" not in st.session_state:
    st.session_state.last_confidence = 0
if "pipeline_step" not in st.session_state:
    st.session_state.pipeline_step = 0  # 0: Standby, 5: Ready/Live

# Inject curated theme stylesheet based on active selection
st.markdown(get_theme_css(st.session_state.active_theme), unsafe_allow_html=True)

# Inject dynamic CSS to highlight the active menu button in the sidebar
active_button_css = ""
active_theme = st.session_state.active_theme
active_page = st.session_state.active_page

if active_page == "home":
    button_idx = 1
elif active_page == "settings":
    button_idx = 3
elif active_page == "contact":
    button_idx = 4
else:
    button_idx = 0

if button_idx > 0:
    if active_theme == "Amethyst Violet":
        active_color = "#8b5cf6"
        active_bg = "rgba(121, 40, 202, 0.15)"
    elif active_theme == "Cyberpunk Neon":
        active_color = "#00f2fe"
        active_bg = "rgba(0, 242, 254, 0.08)"
    elif active_theme == "Deep Midnight":
        active_color = "#ffffff"
        active_bg = "rgba(255, 255, 255, 0.05)"
    elif active_theme == "Minimalist Light":
        active_color = "#8b5cf6"
        active_bg = "rgba(139, 92, 246, 0.08)"
    else:
        active_color = "#8b5cf6"
        active_bg = "rgba(121, 40, 202, 0.15)"

    active_button_css = f"""
    <style>
    div[data-testid="stSidebar"] .stButton:nth-of-type({button_idx}) > button {{
        background: {active_bg} !important;
        color: {active_color} !important;
        border-left: 3px solid {active_color} !important;
        border-radius: 0 10px 10px 0 !important;
        font-weight: bold !important;
    }}
    </style>
    """
    st.markdown(active_button_css, unsafe_allow_html=True)

# Instantiate managers
@st.cache_resource
def get_managers():
    loader = PDFLoader()
    chunker = DocumentChunker()
    vstore = VectorStoreManager()
    utils = RAGUtilities()
    return loader, chunker, vstore, utils

pdf_loader, doc_chunker, vector_store, rag_utils = get_managers()

# Automatically fetch API Key from .env
API_KEY = os.getenv("GEMINI_API_KEY", "")

# ================= SIDEBAR (ELEGANT MENU & INGESTION) =================
with st.sidebar:
    # 1. USER PROFILE CARD (Styled exactly like the John Doe card in your screenshot!)
    avatar_html = "<div class='profile-avatar'>SY</div>"
    if profile_pic_base64:
        avatar_html = f"<img src='data:image/jpeg;base64,{profile_pic_base64}' class='profile-avatar' style='object-fit: cover; padding: 0;' />"
        
    st.markdown(
        f"""
        <div class='profile-card'>
            {avatar_html}
            <div class='profile-info'>
                <span class='profile-name'>Sandeep Yadav</span>
                <span class='profile-email'>sandeepyadav19651@gmail.com</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # 2. VERTICAL MENU NAVIGATION LINKS (Active Streamlit Navigation Buttons)
    st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
    
    if st.button("🏡 Dashboard", key="btn_nav_home", use_container_width=True):
        st.session_state.active_page = "home"
        st.rerun()
        
    if st.button("💬 New Chat Session", key="btn_nav_new_chat", use_container_width=True):
        st.session_state.chat_history = []
        st.session_state.last_sources = []
        st.session_state.last_confidence = 0
        st.session_state.active_page = "home"
        st.toast("New chat session started!", icon="💬")
        st.rerun()
        
    if st.button("⚙️ Platform Settings", key="btn_nav_settings", use_container_width=True):
        st.session_state.active_page = "settings"
        st.rerun()
        
    if st.button("📬 About Developer", key="btn_nav_contact", use_container_width=True):
        st.session_state.active_page = "contact"
        st.rerun()
    
    # 3. PDF ACQUISITION CARD
    st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)
    st.markdown("<div class='sidebar-header' style='font-size:0.8rem; text-transform:uppercase;'>📂 Ingestion Engine</div>", unsafe_allow_html=True)
    uploaded_files = st.file_uploader(
        "Upload one or more PDF files",
        type=["pdf"],
        accept_multiple_files=True,
        label_visibility="collapsed"
    )
    
    # Ingestion pipeline processing
    if uploaded_files:
        current_names = [f.name for f in uploaded_files]
        session_names = [f["name"] for f in st.session_state.processed_docs]
        
        if set(current_names) != set(session_names):
            st.session_state.pipeline_step = 1
            
            with st.status("🔄 Ingesting document files...", expanded=True) as status:
                try:
                    # Clear previous DB state
                    vector_store.clear_database()
                    rag_utils.clear_uploads()
                    
                    all_loaded_docs = []
                    processed_meta = []
                    
                    st.session_state.pipeline_step = 2  # Parsing
                    for ufile in uploaded_files:
                        status.write(f"Parsing pages: **{ufile.name}**...")
                        local_path = rag_utils.save_uploaded_file(ufile)
                        docs = pdf_loader.load_pdf(local_path, ufile.name)
                        all_loaded_docs.extend(docs)
                        processed_meta.append({
                            "name": ufile.name,
                            "pages": len(docs),
                            "chars": sum(len(d.page_content) for d in docs)
                        })
                        
                    st.session_state.raw_docs = all_loaded_docs
                    
                    st.session_state.pipeline_step = 3  # Chunking
                    status.write("Calculating logical chunk boundaries...")
                    chunks = doc_chunker.split_documents(all_loaded_docs)
                    
                    st.session_state.pipeline_step = 4  # Vector Mapping
                    status.write(f"Vectorizing {len(chunks)} text chunks...")
                    
                    st.session_state.pipeline_step = 5  # Index Creation
                    status.write("Mapping and writing vectors to ChromaDB persistent local index...")
                    vector_store.add_documents(chunks)
                    
                    # Store metadata
                    st.session_state.processed_docs = processed_meta
                    
                    # Question Suggestions
                    status.write("Mining context to compile analytical suggestions...")
                    st.session_state.question_suggestions = rag_utils.generate_question_suggestions(
                        API_KEY, all_loaded_docs
                    )
                    
                    status.update(label="🚀 Ingestion complete! Context Index active.", state="complete", expanded=False)
                    st.toast(f"Ingested {len(uploaded_files)} PDF nodes into local ChromaDB!", icon="💾")
                except Exception as e:
                    st.session_state.pipeline_step = -1
                    status.update(label="❌ Ingestion failed!", state="error")
                    st.error(f"Ingestion crashed: {str(e)}")
                    
    # 4. PIPELINE CHECKLIST
    st.markdown("<div class='sidebar-header' style='font-size:0.75rem; text-transform:uppercase; margin-top:25px;'>📋 Ingestion Timeline</div>", unsafe_allow_html=True)
    
    step = st.session_state.pipeline_step
    
    st.markdown(
        f"""
        <div class='glass-card' style='padding: 12px; background: rgba(255,255,255,0.01); margin-bottom:15px; border-radius:12px;'>
            <div class='pipeline-item {"active done" if step >= 1 else ""}'>
                <div class='pipeline-circle'>{"✓" if step >= 1 else "1"}</div>
                <span style='font-size:0.75rem;'>File uploaded</span>
            </div>
            <div class='pipeline-item {"active done" if step >= 2 else ""}'>
                <div class='pipeline-circle'>{"✓" if step >= 2 else "2"}</div>
                <span style='font-size:0.75rem;'>Text extracted</span>
            </div>
            <div class='pipeline-item {"active done" if step >= 3 else ""}'>
                <div class='pipeline-circle'>{"✓" if step >= 3 else "3"}</div>
                <span style='font-size:0.75rem;'>Text chunked</span>
            </div>
            <div class='pipeline-item {"active done" if step >= 4 else ""}'>
                <div class='pipeline-circle'>{"✓" if step >= 4 else "4"}</div>
                <span style='font-size:0.75rem;'>Embeddings created</span>
            </div>
            <div class='pipeline-item {"active done" if step >= 5 else ""}'>
                <div class='pipeline-circle'>{"✓" if step >= 5 else "5"}</div>
                <span style='font-size:0.75rem;'>Vector database ready</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Reset Database Button
    if st.session_state.processed_docs:
        if st.button("🗑️ Reset Database", use_container_width=True):
            vector_store.clear_database()
            rag_utils.clear_uploads()
            st.session_state.processed_docs = []
            st.session_state.chat_history = []
            st.session_state.raw_docs = []
            st.session_state.last_sources = []
            st.session_state.last_confidence = 0
            st.session_state.pipeline_step = 0
            st.session_state.question_suggestions = [
                "Summarize active documents",
                "Explain key terms",
                "List main takeaways"
            ]
            st.toast("Local vector database and uploads have been deleted.", icon="🧹")
            st.rerun()

# ================= MAIN AREA (MINIMALIST GRADIEN UI) =================
# Set up dynamic mode variables
is_rag = len(st.session_state.processed_docs) > 0
mode_badge = "⚡ CONTEXT INGESTED" if is_rag else "🟢 GENERAL MODE ACTIVE"
badge_class = "capsule-badge-active" if is_rag else ""

# 3-Column main screen layout (Divided into col_main for Chat, col_right for stats/inspection)
col_main, col_right = st.columns([5, 2])

with col_main:
    # 1. "Hi Friend! Can I help you?" STYLE HEADER (Personalized to Sandeep!)
    st.markdown(
        f"""
        <div style='margin-top: 15px; margin-bottom: 25px;'>
            <div class='main-title'>Hi Sandeep!</div>
            <div class='main-subtitle' style='display:flex; align-items:center; gap:15px;'>
                <span>Can I help you?</span>
                <span class='capsule-badge {badge_class}' style='font-size:0.7rem; padding:4px 10px; border-radius:20px;'>{mode_badge}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # 2. THE TWO FLOATING VIOLET CARDS (FROSTED VIOLET GLASS CARDS)
    c1, c2 = st.columns(2)
    with c1:
        if is_rag:
            active_file = st.session_state.processed_docs[0]["name"]
            if len(st.session_state.processed_docs) > 1:
                active_file += f" (+{len(st.session_state.processed_docs)-1} more)"
            card_desc = f"Analyzing active file context: <strong>{active_file}</strong>."
        else:
            card_desc = "Running in General Assistant Mode. Paste Gemini key and talk casually about any topics."
            
        st.markdown(
            f"""
            <div class='glass-card' style='height: 120px; overflow: hidden; padding: 16px 20px;'>
                <div style='font-family: Outfit, sans-serif; font-weight:600; font-size:0.95rem; color:#ffffff; margin-bottom:6px;'>Active Session</div>
                <div style='font-size:0.78rem; color:rgba(255,255,255,0.5); line-height:1.45;'>{card_desc}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with c2:
        if is_rag and st.session_state.last_confidence > 0:
            conf = st.session_state.last_confidence
            card_2_content = f"""
            <div style='display:flex; justify-content:space-between; align-items:center;'>
                <span style='font-size:0.78rem; color:rgba(255,255,255,0.5);'>Search Match Strength</span>
                <span style='font-family:Outfit, sans-serif; font-weight:700; color:#00f2fe; font-size:0.9rem;'>{conf}%</span>
            </div>
            <div class='cyber-meter' style='margin-top:6px;'>
                <div class='cyber-meter-fill' style='width: {conf}%;'></div>
            </div>
            """
        else:
            card_2_content = "<div style='font-size:0.78rem; color:rgba(255,255,255,0.5); padding-top:4px;'>Vector DB standby. Upload documents to activate real-time match strength telemetry.</div>"
            
        st.markdown(
            f"""
            <div class='glass-card' style='height: 120px; overflow: hidden; padding: 16px 20px;'>
                <div style='font-family: Outfit, sans-serif; font-weight:600; font-size:0.95rem; color:#ffffff; margin-bottom:6px;'>Vector Search Status</div>
                {card_2_content}
            </div>
            """,
            unsafe_allow_html=True
        )
        
    # Mode Notice
    if not is_rag:
        st.markdown(
            """
            <div style='background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 12px; padding: 12px 16px; font-size: 0.8rem; color: rgba(255,255,255,0.6); margin-bottom: 20px; line-height: 1.4;'>
                💡 <strong>Conversational Mode:</strong> I am currently running as a general assistant. Feel free to ask general questions, write code, or just say hello!
            </div>
            """,
            unsafe_allow_html=True
        )
        
    # Chat container (Renders minimal floating bubbles)
    chat_container = st.container()
    
    with chat_container:
        for msg in st.session_state.chat_history:
            bubble_class = "chat-bubble-user" if msg["role"] == "user" else "chat-bubble-ai"
            avatar = "👤 Sandeep Yadav" if msg["role"] == "user" else "🤖 AskDocs AI"
            avatar_color = "#c084fc" if msg["role"] == "user" else "#22d3ee"
            
            st.markdown(
                f"""
                <div class='chat-bubble-container {bubble_class}'>
                    <div style='font-size:0.7rem; color:{avatar_color}; font-weight:700; margin-bottom:5px; font-family:Outfit, sans-serif;'>{avatar}</div>
                    {msg["content"]}
                </div>
                """,
                unsafe_allow_html=True
            )
            
    # Suggested quick-question pill capsules
    selected_question = None
    if not is_rag:
        st.markdown(
            """
            <div style='background: rgba(255, 255, 255, 0.02); border: 1px dashed rgba(255, 255, 255, 0.15); border-radius: 12px; padding: 12px; text-align: center; font-size: 0.8rem; color: rgba(255,255,255,0.45); font-family: Outfit, sans-serif;'>
                Upload a document to unlock AI document actions
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.write("<p style='font-size:0.72rem; color:rgba(255,255,255,0.4); font-weight:600; font-family:Outfit, sans-serif; margin-bottom:8px; letter-spacing:0.5px;'>💡 Suggested Questions:</p>", unsafe_allow_html=True)
        q_cols = st.columns(len(st.session_state.question_suggestions))
        for i, q_text in enumerate(st.session_state.question_suggestions):
            with q_cols[i]:
                if st.button(q_text, key=f"q_suggest_{i}", use_container_width=True):
                    selected_question = q_text
                
    st.markdown("---")
    
    # Chat Input bar
    chat_input_val = st.chat_input("Ask any questions...")
    query = selected_question if selected_question else chat_input_val
    
    if query:
        if not API_KEY:
            st.error("🔒 SYSTEM LOCK: Gemini API Authentication Key not found. Please write it to your .env file.")
        else:
            # 1. Append user message to chat history
            st.session_state.chat_history.append({"role": "user", "content": query})
            
            # 2. Perform RAG pipeline
            with st.spinner("🔍 Reviewing context..."):
                try:
                    retrieved_chunks = []
                    
                    if is_rag:
                        chunks_with_score = vector_store.similarity_search_with_score(query, k=4)
                        
                        if chunks_with_score:
                            retrieved_chunks = [doc for doc, score in chunks_with_score]
                            top_score = chunks_with_score[0][1]
                            confidence = int(max(50, min(99, (1.0 - (top_score / 1.6)) * 100)))
                            st.session_state.last_confidence = confidence
                            st.session_state.last_sources = chunks_with_score
                        else:
                            st.session_state.last_confidence = 0
                            st.session_state.last_sources = []
                    else:
                        st.session_state.last_confidence = 0
                        st.session_state.last_sources = []
                        
                    # Initialize LLM chain
                    chain_manager = RAGChainManager(api_key=API_KEY)
                    
                    # Generate Answer
                    answer = chain_manager.generate_answer(query, retrieved_chunks)
                    
                    # Format and append sources for user if RAG is active
                    if is_rag and retrieved_chunks:
                        if "I could not find this information in the uploaded document" not in answer:
                            sources_list = []
                            seen_sources = set()
                            for chunk in retrieved_chunks:
                                src = chunk.metadata.get("source", "Unknown Document")
                                pg = chunk.metadata.get("page", "Page N/A")
                                src_key = (src, pg)
                                if src_key not in seen_sources:
                                    seen_sources.add(src_key)
                                    sources_list.append(f"{src} — Page {pg}")
                            
                            if sources_list:
                                sources_md = "\n\nSources:\n" + "\n".join([f"{idx + 1}. {s}" for idx, s in enumerate(sources_list)])
                                answer += sources_md
                    
                    # Save assistant message
                    assistant_msg = {
                        "role": "assistant",
                        "content": answer
                    }
                    st.session_state.chat_history.append(assistant_msg)
                    st.rerun()
                except Exception as e:
                    st.error(f"Failed to generate response: {str(e)}")

# ================= RIGHT PANEL (CONTEXT INTELLIGENCE HUD) =================
with col_right:
    st.markdown(
        """
        <div class='glass-card' style='background: rgba(255,255,255,0.02); margin-top: 10px; padding:15px 18px;'>
            <h3 style='margin: 0 0 2px 0; font-size:0.95rem; color:#ffffff; font-family:Outfit, sans-serif; font-weight:700;'>📊 Document Intelligence Panel</h3>
            <p style='font-size:0.7rem; color:rgba(255,255,255,0.4); margin:0;'>Active telemetry metrics</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # 1. METRICS DASHBOARD
    stats = vector_store.get_collection_stats()
    unique_docs = len(st.session_state.processed_docs)
    total_pages = sum(d["pages"] for d in st.session_state.processed_docs)
    
    if unique_docs == 0:
        total_chunks = 0
        db_status = "STANDBY"
        db_color = "rgba(255,255,255,0.2)"
    else:
        total_chunks = stats.get("total_chunks", 0)
        db_status = "ONLINE" if total_chunks > 0 else "STANDBY"
        db_color = "#a78bfa" if total_chunks > 0 else "rgba(255,255,255,0.2)"
    
    st.markdown(
        f"""
        <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 15px;'>
            <div class='glass-card' style='padding: 10px 14px; margin:0; text-align:center;'>
                <div class='card-stat-label'>Docs Mapped</div>
                <div class='card-stat-number'>{unique_docs}</div>
            </div>
            <div class='glass-card' style='padding: 10px 14px; margin:0; text-align:center;'>
                <div class='card-stat-label'>Total Pages</div>
                <div class='card-stat-number'>{total_pages}</div>
            </div>
            <div class='glass-card' style='padding: 10px 14px; margin:0; text-align:center;'>
                <div class='card-stat-label'>Vector Chunks</div>
                <div class='card-stat-number'>{total_chunks}</div>
            </div>
            <div class='glass-card' style='padding: 10px 14px; margin:0; text-align:center;'>
                <div class='card-stat-label'>Index Status</div>
                <div class='card-stat-number' style='font-size:1rem; color:{db_color}; font-weight:700; padding-top:8px;'>{db_status}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # 2. RETRIEVED SOURCES PANEL
    if is_rag and st.session_state.last_sources:
        st.markdown(
            """
            <div class='glass-card' style='padding: 15px;'>
                <h4 style='margin: 0 0 10px 0; font-size: 0.8rem; color:#ffffff; font-family:Outfit, sans-serif; font-weight:600;'>📍 Retrieved Citations</h4>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        for s_idx, (doc, score) in enumerate(st.session_state.last_sources):
            source_name = doc.metadata.get("source", "Unknown PDF")
            page_num = doc.metadata.get("page", "Page N/A")
            ind_conf = int(max(50, min(99, (1.0 - (score / 1.6)) * 100)))
            
            with st.expander(f"📍 Citation {s_idx + 1} | Pg {page_num}"):
                st.markdown(
                    f"""
                    <div class='source-citation-card'>
                        <div style='display:flex; justify-content:space-between; font-size:0.7rem; color:#c084fc; font-family:Outfit, sans-serif; margin-bottom:5px; font-weight:500;'>
                            <span>RELEVANCE: {ind_conf}%</span>
                            <span>FILE: {source_name}</span>
                        </div>
                        <p style='margin:0; font-style:italic; font-size:0.75rem; color:#cbd5e1; line-height:1.4;'>"{doc.page_content}"</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
    # 3. EXTRA CONTROLS
    st.markdown(
        """
        <div class='glass-card' style='padding: 15px;'>
            <h4 style='margin: 0 0 10px 0; font-size: 0.8rem; color:#ffffff; font-family:Outfit, sans-serif; font-weight:600;'>🕹️ Controls</h4>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Document Summarizer Button
    if is_rag:
        if st.button("✨ Generate Document Summary", use_container_width=True):
            with st.spinner("Generating document summary..."):
                try:
                    chain_manager = RAGChainManager(api_key=API_KEY)
                    summary = chain_manager.generate_summary(st.session_state.raw_docs)
                    st.markdown(
                        """
                        <div class='glass-card' style='background: rgba(121, 40, 202, 0.05); border-color: rgba(121, 40, 202, 0.2); margin-top: 10px; padding:12px; margin-bottom:10px;'>
                            <h4 style='margin-top:0; margin-bottom:0; font-size:0.8rem; color:#c084fc; font-family:Outfit, sans-serif; font-weight:600;'>📄 Summary Overview</h4>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    st.markdown(summary)
                except Exception as e:
                    st.error(f"Summary failed: {str(e)}")
                    
    # Transcript Download Button
    if st.session_state.chat_history:
        transcript_md = rag_utils.export_chat_to_markdown(st.session_state.chat_history)
        st.markdown("<div class='secondary-btn'>", unsafe_allow_html=True)
        st.download_button(
            label="📥 Download Transcript",
            data=transcript_md,
            file_name="askdocs_chat_transcript.md",
            mime="text/markdown",
            use_container_width=True
        )
        st.markdown("</div>", unsafe_allow_html=True)
        
    # Chat memory and Session controls
    st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
    c_col1, c_col2 = st.columns(2)
    with c_col1:
        if st.button("🧹 Clear Chat", use_container_width=True):
            st.session_state.chat_history = []
            st.toast("Chat feed cleared!", icon="🧹")
            st.rerun()
    with c_col2:
        if st.button("🔄 New Session", use_container_width=True):
            # Wipe database and reset uploads/timeline
            vector_store.clear_database()
            rag_utils.clear_uploads()
            st.session_state.processed_docs = []
            st.session_state.chat_history = []
            st.session_state.raw_docs = []
            st.session_state.last_sources = []
            st.session_state.last_confidence = 0
            st.session_state.pipeline_step = 0
            st.session_state.question_suggestions = [
                "Summarize active documents",
                "Explain key terms",
                "List main takeaways"
            ]
            st.toast("System reset! Starting fresh session.", icon="🔄")
            st.rerun()

# ================= DYNAMIC PAGE ROUTING =================
if st.session_state.active_page == "settings":
    st.markdown(
        """
        <div style='margin-top: 15px; margin-bottom: 25px;'>
            <div class='main-title'>⚙️ Platform Control Center</div>
            <div class='main-subtitle'>Configure theme, document processing, and answer generation settings</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Sibling anchor for CSS glassmorphism card wrapping
    st.markdown("<div id='settings-deck-anchor'></div>", unsafe_allow_html=True)
    
    with st.container():
        # Theme Selector Engine
        st.markdown("<h3 style='margin-top:0; margin-bottom: 15px; font-family:Outfit, sans-serif; font-size:1.1rem; color:#ffffff;'>🎨 Theme Settings</h3>", unsafe_allow_html=True)
        
        themes = ["Amethyst Violet", "Cyberpunk Neon", "Deep Midnight"]
        
        selected_theme = st.selectbox(
            "Choose visual theme",
            options=themes,
            index=themes.index(st.session_state.active_theme),
            label_visibility="collapsed"
        )
        
        if selected_theme != st.session_state.active_theme:
            st.session_state.active_theme = selected_theme
            st.toast(f"Theme changed to {selected_theme}!", icon="🎨")
            st.rerun()
            
        st.markdown("<hr style='border-color: rgba(255,255,255,0.08); margin: 25px 0;'>", unsafe_allow_html=True)
        
        # RAG Ingestion Boundary Settings
        st.markdown("<h3 style='margin-top:0; margin-bottom: 5px; font-family:Outfit, sans-serif; font-size:1.1rem; color:#ffffff;'>📂 Document Processing Settings</h3>", unsafe_allow_html=True)
        st.markdown("<p style='font-size: 0.78rem; color: rgba(255,255,255,0.5); line-height: 1.4; margin-bottom: 15px;'>Adjust logical chunk sizes and overlapping bounds for parsing context nodes.</p>", unsafe_allow_html=True)
        
        chunk_size_val = st.slider("Logical Chunk Size (characters)", min_value=500, max_value=1500, value=st.session_state.chunk_size, step=100)
        chunk_overlap_val = st.slider("Logical Chunk Overlap (characters)", min_value=50, max_value=300, value=st.session_state.chunk_overlap, step=10)
        
        if chunk_size_val != st.session_state.chunk_size:
            st.session_state.chunk_size = chunk_size_val
        if chunk_overlap_val != st.session_state.chunk_overlap:
            st.session_state.chunk_overlap = chunk_overlap_val
        
        st.markdown("<hr style='border-color: rgba(255,255,255,0.08); margin: 25px 0;'>", unsafe_allow_html=True)
        
        # System Environment Telemetry
        st.markdown("<h3 style='margin-top:0; margin-bottom: 15px; font-family:Outfit, sans-serif; font-size:1.1rem; color:#ffffff;'>🤖 System Environment Telemetry</h3>", unsafe_allow_html=True)
        
        masked_key = "MOCKED / DETECTED IN ENVIRONMENT"
        if API_KEY:
            masked_key = f"{API_KEY[:8]}...{API_KEY[-4:]}" if len(API_KEY) > 12 else "ACTIVE // SECURED"
            
        st.markdown(
            f"""
            <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 15px; font-size: 0.8rem; line-height: 1.5; color: rgba(255,255,255,0.7);'>
                <div>💻 <strong>Engine:</strong> Streamlit / Python 3.11</div>
                <div>🔑 <strong>Gemini Credentials:</strong> <span style='font-family:Share Tech Mono; color:#22d3ee;'>{masked_key}</span></div>
                <div>📁 <strong>Embeddings Model:</strong> sentence-transformers/all-MiniLM-L6-v2</div>
                <div>💾 <strong>Local Vector Store:</strong> ChromaDB / persistent_sqlite3</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    # Elegant footer inside the settings page
    st.markdown(
        """
        <div class='cyber-footer' style='margin-top: 30px;'>
            ASKDOCS AI PLATFORM v2.0 // HANDCRAFTED BY SANDEEP YADAV // ALL SYSTEMS ACTIVE
        </div>
        """,
        unsafe_allow_html=True
    )
    st.stop()

# ================= CONTACT ROUTER =================
if st.session_state.active_page == "contact":
    st.markdown(
        """
        <div style='margin-top: 15px; margin-bottom: 25px;'>
            <div class='main-title'>📬 About Developer</div>
            <div class='main-subtitle'>Building practical AI/ML and document intelligence solutions</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Sibling anchor for CSS glassmorphism card wrapping
    st.markdown("<div id='contact-deck-anchor'></div>", unsafe_allow_html=True)
    
    with st.container():
        # User details card inside settings container
        main_avatar_html = "<div style='width: 80px; height: 80px; border-radius: 50%; background: linear-gradient(135deg, #8b5cf6 0%, #00f2fe 100%); display: flex; align-items: center; justify-content: center; font-family:Outfit, sans-serif; font-weight:700; font-size:2.2rem; color:#ffffff; margin-bottom:15px; box-shadow:0 0 20px rgba(139,92,246,0.4);'>SY</div>"
        if profile_pic_base64:
            main_avatar_html = f"<img src='data:image/jpeg;base64,{profile_pic_base64}' style='width: 80px; height: 80px; border-radius: 50%; object-fit: cover; margin-bottom:15px; box-shadow:0 0 20px rgba(139,92,246,0.4); border: 2px solid #8b5cf6;' />"
            
        st.markdown(
            f"""
            <div style='display:flex; flex-direction:column; align-items:center; text-align:center; padding: 20px 0;'>
                {main_avatar_html}
                <h3 style='margin:0; font-family:Outfit, sans-serif; font-size:1.4rem; color:#ffffff;'>Sandeep Yadav</h3>
                <p style='margin: 5px 0 20px 0; font-size:0.85rem; color:#22d3ee; font-family:Share Tech Mono; letter-spacing:0.5px;'>DATA SCIENCE STUDENT • AI/ML ENTHUSIAST</p>
                <p style='margin:0 0 15px 0; max-width:550px; font-size:0.82rem; color:rgba(255,255,255,0.6); line-height:1.55;'>
                    B.Tech Data Science student at SKIT Jaipur and IIT Madras BS Data Science learner. Passionate about AI/ML, RAG-based applications, Python, Flask, Streamlit, and full-stack project development.
                </p>
            </div>
            
            <div class='glass-card' style='padding: 20px; border-radius: 12px; margin-top: 10px; margin-bottom: 25px; text-align: left; background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.08);'>
                <h4 style='margin-top: 0; margin-bottom: 12px; font-family: Outfit, sans-serif; font-size: 1rem; color: #ffffff;'>📄 Developer & Project Biography</h4>
                <p style='font-size: 0.82rem; color: rgba(255,255,255,0.7); line-height: 1.6; margin-bottom: 12px; font-family: "Plus Jakarta Sans", sans-serif;'>
                    I am a B.Tech Data Science student at SKIT Jaipur and a BS Data Science and Applications learner at IIT Madras. I enjoy building practical AI/ML and full-stack projects, especially applications involving machine learning, document intelligence, RAG systems, and web development.
                </p>
                <p style='font-size: 0.82rem; color: rgba(255,255,255,0.7); line-height: 1.6; margin: 0; font-family: "Plus Jakarta Sans", sans-serif;'>
                    <strong>AskDocs AI</strong> is one of my projects focused on Retrieval-Augmented Generation, where users can upload documents and ask questions based on the uploaded content.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Action Buttons grid
        st.markdown("<hr style='border-color: rgba(255,255,255,0.08); margin: 15px 0;'>", unsafe_allow_html=True)
        st.markdown("<h4 style='margin-top:0; margin-bottom: 20px; font-family:Outfit, sans-serif; font-size:1.1rem; color:#ffffff; text-align:center;'>🔗 Connect Channels</h4>", unsafe_allow_html=True)
        
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            st.markdown(
                """
                <a href='mailto:sandeepyadav19651@gmail.com' style='text-decoration:none;'>
                    <div class='glass-card capsule-chip' style='padding: 15px; text-align:center; border-color:rgba(255,255,255,0.1); cursor:pointer;'>
                        <span style='font-size:1.2rem; margin-right:8px;'>📧</span>
                        <strong style='font-family:Outfit, sans-serif; font-size:0.88rem; color:#ffffff;'>Email Me Directly</strong>
                        <div style='font-size:0.7rem; color:rgba(255,255,255,0.4); margin-top:4px;'>sandeepyadav19651@gmail.com</div>
                    </div>
                </a>
                """,
                unsafe_allow_html=True
            )
        with col_c2:
            st.markdown(
                """
                <a href='https://www.linkedin.com/in/sandeepyadav2003' target='_blank' style='text-decoration:none;'>
                    <div class='glass-card capsule-chip' style='padding: 15px; text-align:center; border-color:rgba(255,255,255,0.1); cursor:pointer;'>
                        <span style='font-size:1.2rem; margin-right:8px;'>💼</span>
                        <strong style='font-family:Outfit, sans-serif; font-size:0.88rem; color:#ffffff;'>LinkedIn Profile</strong>
                        <div style='font-size:0.7rem; color:rgba(255,255,255,0.4); margin-top:4px;'>sandeepyadav2003</div>
                    </div>
                </a>
                """,
                unsafe_allow_html=True
            )
            
        st.markdown("<hr style='border-color: rgba(255,255,255,0.08); margin: 25px 0;'>", unsafe_allow_html=True)
        st.markdown("<h4 style='margin-top:0; margin-bottom: 10px; font-family:Outfit, sans-serif; font-size:1.1rem; color:#ffffff; text-align:center;'>📬 Send a Direct Message</h4>", unsafe_allow_html=True)
        
        # Interactive contact form
        contact_name = st.text_input("Your Name", placeholder="e.g. John Doe")
        contact_subj = st.text_input("Subject", placeholder="e.g. Collaboration Request")
        contact_msg = st.text_area("Your Message", placeholder="Write your message here...")
        
        if st.button("🚀 Compile & Send Message", use_container_width=True):
            if not contact_name or not contact_msg:
                st.error("⚠️ Please fill in both your Name and Message.")
            else:
                import urllib.parse
                import json
                import datetime
                
                # 1. Log the message locally in JSON registry
                log_dir = "data"
                log_file = os.path.join(log_dir, "contact_messages.json")
                os.makedirs(log_dir, exist_ok=True)
                
                messages = []
                if os.path.exists(log_file):
                    try:
                        with open(log_file, "r", encoding="utf-8") as f:
                            messages = json.load(f)
                    except Exception:
                        messages = []
                        
                messages.append({
                    "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "name": contact_name,
                    "subject": contact_subj if contact_subj else "General Inquiry",
                    "message": contact_msg
                })
                
                try:
                    with open(log_file, "w", encoding="utf-8") as f:
                        json.dump(messages, f, indent=4, ensure_ascii=False)
                    st.toast("Saved to local message registry!", icon="💾")
                except Exception as e:
                    st.warning(f"Could not save to local registry: {str(e)}")
                
                # 2. Construct mailto link
                body_content = f"Hi Sandeep,\n\n{contact_msg}\n\nBest regards,\n{contact_name}"
                encoded_subject = urllib.parse.quote(contact_subj if contact_subj else "AskDocs AI Inquiry")
                encoded_body = urllib.parse.quote(body_content)
                mailto_link = f"mailto:sandeepyadav19651@gmail.com?subject={encoded_subject}&body={encoded_body}"
                
                st.markdown(
                    f"""
                    <div style='text-align:center; margin-top: 15px;'>
                        <a href="{mailto_link}" style='text-decoration:none;'>
                            <button class='nav-btn' style='background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%) !important; color:#030008 !important; font-weight:700; padding:12px 25px !important; font-family:Outfit, sans-serif !important; border-radius:10px; border:none; cursor:pointer;'>
                                📤 Open Mail Client to Send
                            </button>
                        </a>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
        st.markdown("<hr style='border-color: rgba(255,255,255,0.08); margin: 25px 0;'>", unsafe_allow_html=True)
        st.markdown("<h4 style='margin-top:0; margin-bottom: 15px; font-family:Outfit, sans-serif; font-size:1.1rem; color:#ffffff; text-align:center;'>📥 Developer Message Inbox (Local Log)</h4>", unsafe_allow_html=True)
        
        # Read and display logged messages
        import json
        log_file = os.path.join("data", "contact_messages.json")
        messages = []
        if os.path.exists(log_file):
            try:
                with open(log_file, "r", encoding="utf-8") as f:
                    messages = json.load(f)
            except Exception:
                messages = []
                
        with st.expander(f"📬 View Logged Messages ({len(messages)} submissions)"):
            if not messages:
                st.info("No messages have been logged in the local system registry yet.")
            else:
                for idx, msg in enumerate(reversed(messages)):
                    st.markdown(
                        f"""
                        <div class='glass-card' style='background: rgba(255, 255, 255, 0.02); padding: 12px; margin-bottom:12px; border-radius:10px; border: 1px solid rgba(255,255,255,0.08);'>
                            <div style='display:flex; justify-content:space-between; font-size:0.72rem; color:#00f2fe; font-family:Outfit, sans-serif; margin-bottom:6px;'>
                                <strong>👤 {msg['name']}</strong>
                                <span>🕒 {msg['timestamp']}</span>
                            </div>
                            <div style='font-size:0.8rem; font-weight:600; color:#ffffff; margin-bottom:4px; font-family:Outfit, sans-serif;'>Subject: {msg['subject']}</div>
                            <p style='margin:0; font-size:0.78rem; color:#cbd5e1; line-height:1.4;'>"{msg['message']}"</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                
                # Option to clear logs
                if st.button("🗑️ Clear Message Registry", use_container_width=True):
                    if os.path.exists(log_file):
                        try:
                            os.remove(log_file)
                            st.toast("Message registry cleared!", icon="🧹")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Failed to clear logs: {str(e)}")
                
    # Elegant footer inside the settings page
    st.markdown(
        """
        <div class='cyber-footer' style='margin-top: 30px;'>
            ASKDOCS AI PLATFORM v2.0 // HANDCRAFTED BY SANDEEP YADAV // ALL SYSTEMS ACTIVE
        </div>
        """,
        unsafe_allow_html=True
    )
    st.stop()

# ================= ELEGANT CYBER FOOTER =================
st.markdown(
    """
    <div class='cyber-footer'>
        ASKDOCS AI PLATFORM v2.0 // HANDCRAFTED BY SANDEEP YADAV // ALL SYSTEMS ACTIVE
    </div>
    """,
    unsafe_allow_html=True
)
