import textwrap

# Multi-Theme Stylesheet System for AskDocs AI
def get_theme_css(theme_name: str) -> str:
    """
    Returns the exact custom CSS string based on the selected theme.
    Supported themes: "Amethyst Violet" (Default), "Cyberpunk Neon", "Deep Midnight", "Minimalist Light".
    """
    
    # 1. Base Styles common to all themes (Fonts, layout adjustments, timeline)
    BASE_STYLES = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&family=Share+Tech+Mono&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Plus Jakarta Sans', sans-serif;
        }
        
        /* Sidebar Profile Card */
        .profile-card {
            display: flex;
            align-items: center;
            gap: 15px;
            padding: 10px 5px;
            margin-bottom: 25px;
        }
        
        .profile-avatar {
            width: 44px;
            height: 44px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: 'Outfit', sans-serif;
            font-weight: 600;
            font-size: 1.2rem;
        }
        
        .profile-info {
            display: flex;
            flex-direction: column;
        }
        
        .profile-name {
            font-family: 'Outfit', sans-serif;
            font-weight: 600;
            font-size: 0.95rem;
        }
        
        .profile-email {
            font-size: 0.7rem;
        }
        
        /* Navigation Links */
        .nav-btn {
            display: block;
            width: 100%;
            text-align: left;
            background: none !important;
            border: none !important;
            padding: 10px 14px !important;
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            font-size: 0.85rem !important;
            border-radius: 10px !important;
            margin-bottom: 6px !important;
            cursor: pointer !important;
            transition: all 0.2s ease !important;
            box-shadow: none !important;
        }
        
        /* Suggested Pills */
        .capsule-chip {
            border-radius: 30px;
            padding: 8px 18px;
            font-size: 0.8rem;
            cursor: pointer;
            transition: all 0.2s ease;
            text-align: center;
            width: 100%;
            display: block;
            letter-spacing: 0.2px;
        }
        
        /* Chat bubble container */
        .chat-bubble-container {
            padding: 14px 18px;
            border-radius: 20px;
            margin-bottom: 12px;
            font-size: 0.92rem;
            line-height: 1.5;
        }
        
        /* Relevance dial bar */
        .cyber-meter {
            height: 5px;
            border-radius: 3px;
            overflow: hidden;
            margin-top: 8px;
        }
        .cyber-meter-fill {
            height: 100%;
            border-radius: 3px;
        }
        
        /* Citations and summaries */
        .source-citation-card {
            border-radius: 8px;
            padding: 10px 12px;
            margin-top: 8px;
            font-size: 0.78rem;
        }
        
        /* Ingestion timeline */
        .pipeline-item {
            display: flex;
            align-items: center;
            gap: 12px;
            font-size: 0.78rem;
            margin-bottom: 10px;
            transition: all 0.3s ease;
        }
        .pipeline-circle {
            width: 16px;
            height: 16px;
            border-radius: 50%;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-size: 0.65rem;
            font-weight: 700;
            transition: all 0.3s ease;
        }
        
        /* Main Headings */
        .main-title {
            font-family: 'Outfit', sans-serif;
            font-weight: 600;
            font-size: 2.3rem;
            letter-spacing: -0.5px;
            margin: 0;
            line-height: 1.25;
        }
        .main-subtitle {
            font-family: 'Outfit', sans-serif;
            font-weight: 500;
            font-size: 1.8rem;
            margin: 0 0 25px 0;
            line-height: 1.25;
        }
        
        .capsule-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            font-family: 'Share Tech Mono', sans-serif;
            padding: 5px 12px;
            border-radius: 30px;
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .cyber-footer {
            text-align: center;
            font-family: 'Outfit', sans-serif;
            font-size: 0.72rem;
            margin-top: 50px;
            letter-spacing: 0.5px;
        }
        
        /* Sidebar divider */
        .sidebar-divider {
            height: 1px;
            margin: 15px 0;
        }

        /* Sidebar Button Overrides for Navigation Deck */
        [data-testid="stSidebar"] .stButton > button {
            display: block !important;
            width: 100% !important;
            text-align: left !important;
            background: transparent !important;
            border: none !important;
            padding: 10px 14px !important;
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            font-size: 0.85rem !important;
            border-radius: 10px !important;
            margin-bottom: 6px !important;
            cursor: pointer !important;
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
            box-shadow: none !important;
        }

        /* Distinctive Styling for Ingest Action Buttons in Sidebar */
        .reset-db-btn-container .stButton > button {
            background: linear-gradient(135deg, #ef4444 0%, #b91c1c 100%) !important;
            color: white !important;
            border: none !important;
            text-align: center !important;
            font-weight: 600 !important;
            box-shadow: 0 4px 15px rgba(239, 68, 68, 0.2) !important;
        }
        .reset-db-btn-container .stButton > button:hover {
            background: linear-gradient(135deg, #f87171 0%, #ef4444 100%) !important;
            box-shadow: 0 6px 20px rgba(239, 68, 68, 0.35) !important;
        }
    </style>
    """
    
    # 2. Specific Theme Styling
    if theme_name == "Amethyst Violet":
        theme_css = """
        <style>
            /* 1. Main Background and text colors */
            .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
                background: linear-gradient(180deg, #1c083c 0%, #080315 65%, #002d35 100%) !important;
                color: #f8fafc !important;
            }
            
            .stApp p, .stApp span, .stApp label, .stApp li, .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6, .stApp strong {
                color: #f1f5f9 !important;
            }
            
            .stApp [data-testid="stMarkdownContainer"] p, 
            .stApp [data-testid="stMarkdownContainer"] span,
            .stApp [data-testid="stMarkdownContainer"] li,
            .stApp [data-testid="stMarkdownContainer"] strong,
            .stApp [data-testid="stMarkdownContainer"] h1,
            .stApp [data-testid="stMarkdownContainer"] h2,
            .stApp [data-testid="stMarkdownContainer"] h3,
            .stApp [data-testid="stMarkdownContainer"] h4 {
                color: #cbd5e1 !important;
            }
            
            /* 2. Sidebar overrides */
            [data-testid="stSidebar"], 
            section[data-testid="stSidebar"], 
            [data-testid="stSidebar"] > div, 
            [data-testid="stSidebarContent"], 
            [data-testid="stSidebarUserContent"],
            .stSidebarContent {
                background-color: #0c041e !important;
                background: #0c041e !important;
                border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
            }
            
            [data-testid="stSidebar"] p, 
            [data-testid="stSidebar"] span, 
            [data-testid="stSidebar"] label, 
            [data-testid="stSidebar"] li, 
            [data-testid="stSidebar"] h1, 
            [data-testid="stSidebar"] h2, 
            [data-testid="stSidebar"] h3, 
            [data-testid="stSidebar"] h4,
            [data-testid="stSidebar"] div,
            [data-testid="stSidebar"] button {
                color: #cbd5e1 !important;
            }
            
            [data-testid="stSidebar"] .profile-name {
                color: #ffffff !important;
                font-weight: 600 !important;
            }
            [data-testid="stSidebar"] .profile-email {
                color: rgba(255, 255, 255, 0.4) !important;
            }
            [data-testid="stSidebar"] .sidebar-header {
                color: #c084fc !important;
                font-weight: 600 !important;
            }
            
            [data-testid="stSidebar"] .stButton > button {
                color: rgba(255, 255, 255, 0.7) !important;
                background-color: transparent !important;
            }
            [data-testid="stSidebar"] .stButton > button:hover {
                background-color: rgba(255, 255, 255, 0.05) !important;
                color: #ffffff !important;
            }
            .sidebar-divider { background-color: rgba(255, 255, 255, 0.08); }
            
            /* File Uploader styling */
            div[data-testid="stFileUploader"] {
                background-color: rgba(121, 40, 202, 0.05) !important;
                border: 1px dashed rgba(121, 40, 202, 0.3) !important;
                border-radius: 12px !important;
                padding: 10px !important;
            }
            div[data-testid="stFileUploader"] * {
                color: #f1f5f9 !important;
            }
            
            /* Dropdown and Selectbox overrides */
            div[data-baseweb="select"] {
                background-color: rgba(121, 40, 202, 0.15) !important;
                border-radius: 8px !important;
            }
            div[data-baseweb="select"] * {
                background-color: transparent !important;
                color: #f1f5f9 !important;
            }
            div[role="listbox"] {
                background-color: #0c041e !important;
                border: 1px solid rgba(121, 40, 202, 0.3) !important;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4) !important;
            }
            div[role="option"] {
                background-color: #0c041e !important;
                color: #f1f5f9 !important;
            }
            div[role="option"]:hover {
                background-color: rgba(121, 40, 202, 0.3) !important;
                color: #ffffff !important;
            }
            div[role="option"] * {
                background-color: transparent !important;
                color: inherit !important;
            }
            
            /* Slider overrides */
            [data-testid="stSlider"] * {
                color: #f1f5f9 !important;
            }
            
            /* Floating glass cards */
            .glass-card,
            div.element-container:has(#settings-deck-anchor) + div,
            div.element-container:has(#contact-deck-anchor) + div {
                background: rgba(121, 40, 202, 0.07) !important;
                backdrop-filter: blur(20px) !important;
                border: 1px solid rgba(255, 255, 255, 0.06) !important;
                border-radius: 20px !important;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4) !important;
            }
            
            .glass-card *,
            div.element-container:has(#settings-deck-anchor) + div *,
            div.element-container:has(#contact-deck-anchor) + div * {
                color: #f1f5f9 !important;
            }
            
            .glass-card .card-stat-label, 
            .glass-card p, 
            .glass-card span {
                color: rgba(255, 255, 255, 0.55) !important;
            }
            .glass-card strong {
                color: #ffffff !important;
            }
            
            .main-title { color: #ffffff !important; }
            .main-subtitle { color: rgba(255, 255, 255, 0.6) !important; }
            .capsule-badge { background: rgba(255, 0, 127, 0.06); border: 1px solid rgba(255, 0, 127, 0.25); color: #ff007f !important; }
            .capsule-badge-active { background: rgba(0, 242, 254, 0.06); border-color: rgba(0, 242, 254, 0.3); color: #00f2fe !important; }
            
            .capsule-chip { background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.12); color: rgba(255, 255, 255, 0.8) !important; }
            .capsule-chip:hover { border-color: rgba(255, 255, 255, 0.4); background: rgba(255, 255, 255, 0.05); color: #ffffff !important; }
            
            .chat-bubble-user { background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.06); border-radius: 20px 20px 20px 4px; }
            .chat-bubble-ai { background: rgba(121, 40, 202, 0.06); border: 1px solid rgba(121, 40, 202, 0.15); border-radius: 20px 20px 4px 20px; }
            
            .cyber-meter { background: rgba(255, 255, 255, 0.08); }
            .cyber-meter-fill { background: linear-gradient(90deg, #8b5cf6, #00f2fe); }
            .source-citation-card { background: rgba(4, 2, 10, 0.6); border: 1px dashed rgba(0, 242, 254, 0.2); }
            
            .pipeline-item { color: rgba(255, 255, 255, 0.35) !important; }
            .pipeline-item.active { color: #f1f5f9 !important; }
            .pipeline-circle { border: 1.5px solid rgba(255, 255, 255, 0.2); color: rgba(255, 255, 255, 0.3) !important; }
            .pipeline-item.active .pipeline-circle { border-color: #8b5cf6; background: rgba(121, 40, 202, 0.2); color: #c084fc !important; }
            .pipeline-item.done .pipeline-circle { border-color: #00f2fe; background: rgba(0, 242, 254, 0.2); color: #22d3ee !important; }
            
            .stButton>button {
                background: linear-gradient(135deg, #8b5cf6 0%, #7928ca 100%);
                color: white !important;
                box-shadow: 0 4px 15px rgba(121, 40, 202, 0.3);
            }
            .stButton>button:hover {
                background: linear-gradient(135deg, #a78bfa 0%, #8b5cf6 100%);
            }
            .secondary-btn>div>button {
                background: rgba(255, 255, 255, 0.02) !important;
                border: 1px solid rgba(255, 255, 255, 0.15) !important;
                color: #cbd5e1 !important;
            }
            .secondary-btn>div>button:hover {
                background: rgba(255, 255, 255, 0.05) !important;
                border-color: rgba(255, 255, 255, 0.35) !important;
            }
            
            .cyber-footer { color: rgba(255, 255, 255, 0.2) !important; }
        </style>
        """
        
    elif theme_name == "Cyberpunk Neon":
        theme_css = """
        <style>
            /* 1. Main Background and text colors */
            .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
                background: radial-gradient(circle at 50% 50%, #03000a 0%, #000000 100%) !important;
                color: #e2e8f0 !important;
            }
            
            .stApp p, .stApp span, .stApp label, .stApp li, .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6, .stApp strong {
                color: #00f2fe !important;
            }
            
            .stApp [data-testid="stMarkdownContainer"] p, 
            .stApp [data-testid="stMarkdownContainer"] span,
            .stApp [data-testid="stMarkdownContainer"] li,
            .stApp [data-testid="stMarkdownContainer"] strong,
            .stApp [data-testid="stMarkdownContainer"] h1,
            .stApp [data-testid="stMarkdownContainer"] h2,
            .stApp [data-testid="stMarkdownContainer"] h3,
            .stApp [data-testid="stMarkdownContainer"] h4 {
                color: #e2e8f0 !important;
            }
            
            /* 2. Sidebar overrides */
            [data-testid="stSidebar"], 
            section[data-testid="stSidebar"], 
            [data-testid="stSidebar"] > div, 
            [data-testid="stSidebarContent"], 
            [data-testid="stSidebarUserContent"],
            .stSidebarContent {
                background-color: #03000a !important;
                background: #03000a !important;
                border-right: 1px solid rgba(0, 242, 254, 0.15) !important;
            }
            
            [data-testid="stSidebar"] p, 
            [data-testid="stSidebar"] span, 
            [data-testid="stSidebar"] label, 
            [data-testid="stSidebar"] li, 
            [data-testid="stSidebar"] h1, 
            [data-testid="stSidebar"] h2, 
            [data-testid="stSidebar"] h3, 
            [data-testid="stSidebar"] h4,
            [data-testid="stSidebar"] div,
            [data-testid="stSidebar"] button {
                color: #00f2fe !important;
            }
            
            [data-testid="stSidebar"] .profile-name {
                color: #ffffff !important;
                font-weight: 600 !important;
            }
            [data-testid="stSidebar"] .profile-email {
                color: #00f2fe !important;
            }
            [data-testid="stSidebar"] .sidebar-header {
                color: #00f2fe !important;
                font-weight: 700 !important;
            }
            
            [data-testid="stSidebar"] .stButton > button {
                color: #cbd5e1 !important;
                background-color: transparent !important;
            }
            [data-testid="stSidebar"] .stButton > button:hover {
                background-color: rgba(0, 242, 254, 0.04) !important;
                color: #00f2fe !important;
            }
            .sidebar-divider { background-color: rgba(0, 242, 254, 0.15); }
            
            /* File Uploader styling */
            div[data-testid="stFileUploader"] {
                background-color: rgba(0, 242, 254, 0.02) !important;
                border: 1px dashed rgba(0, 242, 254, 0.25) !important;
                border-radius: 12px !important;
                padding: 10px !important;
            }
            div[data-testid="stFileUploader"] * {
                color: #e2e8f0 !important;
            }
            
            /* Dropdown and Selectbox overrides */
            div[data-baseweb="select"] {
                background-color: rgba(0, 242, 254, 0.05) !important;
                border-radius: 8px !important;
            }
            div[data-baseweb="select"] * {
                background-color: transparent !important;
                color: #00f2fe !important;
            }
            div[role="listbox"] {
                background-color: #03000a !important;
                border: 1px solid rgba(0, 242, 254, 0.25) !important;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.6) !important;
            }
            div[role="option"] {
                background-color: #03000a !important;
                color: #00f2fe !important;
            }
            div[role="option"]:hover {
                background-color: rgba(0, 242, 254, 0.2) !important;
                color: #ffffff !important;
            }
            div[role="option"] * {
                background-color: transparent !important;
                color: inherit !important;
            }
            
            /* Slider overrides */
            [data-testid="stSlider"] * {
                color: #00f2fe !important;
            }
            
            /* Floating glass cards */
            .glass-card,
            div.element-container:has(#settings-deck-anchor) + div,
            div.element-container:has(#contact-deck-anchor) + div {
                background: rgba(10, 8, 20, 0.85) !important;
                border: 1px solid rgba(0, 242, 254, 0.15) !important;
                border-radius: 16px !important;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.65), 0 0 15px rgba(0, 242, 254, 0.05) !important;
            }
            
            .glass-card *,
            div.element-container:has(#settings-deck-anchor) + div *,
            div.element-container:has(#contact-deck-anchor) + div * {
                color: #00f2fe !important;
            }
            
            .glass-card .card-stat-label, 
            .glass-card p, 
            .glass-card span {
                color: #bae6fd !important;
            }
            .glass-card strong {
                color: #ffffff !important;
            }
            
            .main-title { color: #ffffff !important; text-shadow: 0 0 15px rgba(0, 242, 254, 0.3); }
            .main-subtitle { color: #00f2fe !important; }
            .capsule-badge { background: rgba(255, 0, 127, 0.1); border: 1px solid #ff007f; color: #ff007f !important; text-shadow:0 0 5px rgba(255,0,127,0.3); }
            .capsule-badge-active { background: rgba(0, 242, 254, 0.1); border-color: #00f2fe; color: #00f2fe !important; text-shadow:0 0 5px rgba(0,242,254,0.3); }
            
            .capsule-chip { background: rgba(0, 242, 254, 0.02); border: 1px solid rgba(0, 242, 254, 0.2); color: #bae6fd !important; }
            .capsule-chip:hover { border-color: #ff007f; background: rgba(255, 0, 127, 0.04); color: #ff007f !important; box-shadow: 0 0 10px rgba(255,0,127,0.2); }
            
            .chat-bubble-user { background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.05); border-left: 4px solid #ff007f; border-radius: 16px 16px 16px 4px; }
            .chat-bubble-ai { background: rgba(0, 242, 254, 0.03); border: 1px solid rgba(0, 242, 254, 0.1); border-left: 4px solid #00f2fe; border-radius: 16px 16px 4px 16px; }
            
            .cyber-meter { background: #110c22; }
            .cyber-meter-fill { background: linear-gradient(90deg, #ff007f, #00f2fe); box-shadow: 0 0 8px rgba(0,242,254,0.5); }
            .source-citation-card { background: rgba(6, 3, 12, 0.6); border: 1px dashed rgba(255, 0, 127, 0.25); }
            
            .pipeline-item { color: rgba(255, 255, 255, 0.25) !important; }
            .pipeline-item.active { color: #ffffff !important; }
            .pipeline-circle { border: 1.5px solid rgba(255, 255, 255, 0.15); color: rgba(255, 255, 255, 0.25) !important; }
            .pipeline-item.active .pipeline-circle { border-color: #ff007f; background: rgba(255, 0, 127, 0.1); color: #ff007f !important; }
            .pipeline-item.done .pipeline-circle { border-color: #00f2fe; background: rgba(0, 242, 254, 0.1); color: #00f2fe !important; }
            
            .stButton>button {
                background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%);
                color: #030008 !important;
                box-shadow: 0 4px 15px rgba(0, 242, 254, 0.25);
                font-family: 'Share Tech Mono', sans-serif;
            }
            .stButton>button:hover {
                background: linear-gradient(135deg, #ff007f 0%, #7928ca 100%);
                color: white !important;
                box-shadow: 0 6px 20px rgba(255, 0, 127, 0.45);
            }
            .secondary-btn>div>button {
                background: rgba(14, 11, 28, 0.8) !important;
                border: 1px solid rgba(255, 0, 127, 0.3) !important;
                color: #cbd5e1 !important;
            }
            .secondary-btn>div>button:hover {
                border-color: #ff007f !important;
                background: rgba(255, 0, 127, 0.08) !important;
            }
            
            .cyber-footer { color: #334155; }
        </style>
        """
        
    elif theme_name == "Deep Midnight":
        theme_css = """
        <style>
            /* 1. Main Background and text colors */
            .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
                background-color: #000000 !important;
                background: #000000 !important;
                color: #e2e8f0 !important;
            }
            
            .stApp p, .stApp span, .stApp label, .stApp li, .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6, .stApp strong {
                color: #ffffff !important;
            }
            
            .stApp [data-testid="stMarkdownContainer"] p, 
            .stApp [data-testid="stMarkdownContainer"] span,
            .stApp [data-testid="stMarkdownContainer"] li,
            .stApp [data-testid="stMarkdownContainer"] strong,
            .stApp [data-testid="stMarkdownContainer"] h1,
            .stApp [data-testid="stMarkdownContainer"] h2,
            .stApp [data-testid="stMarkdownContainer"] h3,
            .stApp [data-testid="stMarkdownContainer"] h4 {
                color: #cbd5e1 !important;
            }
            
            /* 2. Sidebar overrides */
            [data-testid="stSidebar"], 
            section[data-testid="stSidebar"], 
            [data-testid="stSidebar"] > div, 
            [data-testid="stSidebarContent"], 
            [data-testid="stSidebarUserContent"],
            .stSidebarContent {
                background-color: #050505 !important;
                background: #050505 !important;
                border-right: 1px solid rgba(255, 255, 255, 0.06) !important;
            }
            
            [data-testid="stSidebar"] p, 
            [data-testid="stSidebar"] span, 
            [data-testid="stSidebar"] label, 
            [data-testid="stSidebar"] li, 
            [data-testid="stSidebar"] h1, 
            [data-testid="stSidebar"] h2, 
            [data-testid="stSidebar"] h3, 
            [data-testid="stSidebar"] h4,
            [data-testid="stSidebar"] div,
            [data-testid="stSidebar"] button {
                color: rgba(255, 255, 255, 0.6) !important;
            }
            
            [data-testid="stSidebar"] .profile-name {
                color: #ffffff !important;
                font-weight: 600 !important;
            }
            [data-testid="stSidebar"] .profile-email {
                color: rgba(255, 255, 255, 0.35) !important;
            }
            [data-testid="stSidebar"] .sidebar-header {
                color: #ffffff !important;
                font-weight: 500 !important;
            }
            
            [data-testid="stSidebar"] .stButton > button {
                color: rgba(255, 255, 255, 0.6) !important;
                background-color: transparent !important;
            }
            [data-testid="stSidebar"] .stButton > button:hover {
                background-color: rgba(255, 255, 255, 0.03) !important;
                color: #ffffff !important;
            }
            .sidebar-divider { background-color: rgba(255, 255, 255, 0.06); }
            
            /* File Uploader styling */
            div[data-testid="stFileUploader"] {
                background-color: rgba(255, 255, 255, 0.015) !important;
                border: 1px dashed rgba(255, 255, 255, 0.15) !important;
                border-radius: 12px !important;
                padding: 10px !important;
            }
            div[data-testid="stFileUploader"] * {
                color: #cbd5e1 !important;
            }
            
            /* Dropdown and Selectbox overrides */
            div[data-baseweb="select"] {
                background-color: rgba(255, 255, 255, 0.03) !important;
                border-radius: 8px !important;
            }
            div[data-baseweb="select"] * {
                background-color: transparent !important;
                color: #ffffff !important;
            }
            div[role="listbox"] {
                background-color: #050505 !important;
                border: 1px solid rgba(255, 255, 255, 0.15) !important;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.7) !important;
            }
            div[role="option"] {
                background-color: #050505 !important;
                color: #ffffff !important;
            }
            div[role="option"]:hover {
                background-color: rgba(255, 255, 255, 0.1) !important;
                color: #ffffff !important;
            }
            div[role="option"] * {
                background-color: transparent !important;
                color: inherit !important;
            }
            
            /* Slider overrides */
            [data-testid="stSlider"] * {
                color: #ffffff !important;
            }
            
            /* Floating glass cards */
            .glass-card,
            div.element-container:has(#settings-deck-anchor) + div,
            div.element-container:has(#contact-deck-anchor) + div {
                background: rgba(255, 255, 255, 0.015) !important;
                border: 1px solid rgba(255, 255, 255, 0.07) !important;
                border-radius: 12px !important;
                box-shadow: 0 10px 40px rgba(0, 0, 0, 0.85) !important;
            }
            
            .glass-card *,
            div.element-container:has(#settings-deck-anchor) + div *,
            div.element-container:has(#contact-deck-anchor) + div * {
                color: #ffffff !important;
            }
            
            .glass-card .card-stat-label, 
            .glass-card p, 
            .glass-card span {
                color: rgba(255, 255, 255, 0.5) !important;
            }
            .glass-card strong {
                color: #ffffff !important;
            }
            
            .main-title { color: #ffffff !important; }
            .main-subtitle { color: rgba(255, 255, 255, 0.5) !important; }
            .capsule-badge { background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.2); color: #ffffff !important; }
            .capsule-badge-active { background: rgba(255, 255, 255, 0.08); border-color: rgba(255,255,255,0.4); color: #ffffff !important; }
            
            .capsule-chip { background: rgba(255, 255, 255, 0.01); border: 1px solid rgba(255, 255, 255, 0.08); color: rgba(255, 255, 255, 0.7) !important; }
            .capsule-chip:hover { border-color: #ffffff; background: rgba(255, 255, 255, 0.03); color: #ffffff !important; }
            
            .chat-bubble-user { background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.05); border-radius: 12px 12px 12px 2px; }
            .chat-bubble-ai { background: rgba(255, 255, 255, 0.04); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 12px 12px 2px 12px; }
            
            .cyber-meter { background: rgba(255, 255, 255, 0.05); }
            .cyber-meter-fill { background: #ffffff; }
            .source-citation-card { background: rgba(255, 255, 255, 0.02); border: 1px dashed rgba(255, 255, 255, 0.15); }
            
            .pipeline-item { color: rgba(255, 255, 255, 0.25) !important; }
            .pipeline-item.active { color: #ffffff !important; }
            .pipeline-circle { border: 1px solid rgba(255, 255, 255, 0.15); color: rgba(255, 255, 255, 0.25) !important; }
            .pipeline-item.active .pipeline-circle { border-color: #ffffff; color: #ffffff !important; }
            .pipeline-item.done .pipeline-circle { border-color: #ffffff; background: rgba(255, 255, 255, 0.1); color: #ffffff !important; }
            
            .stButton>button {
                background: #ffffff;
                color: #000000 !important;
                font-weight: 600;
            }
            .stButton>button:hover {
                background: rgba(255, 255, 255, 0.85);
            }
            .secondary-btn>div>button {
                background: none !important;
                border: 1px solid rgba(255, 255, 255, 0.2) !important;
                color: rgba(255, 255, 255, 0.7) !important;
            }
            .secondary-btn>div>button:hover {
                border-color: #ffffff !important;
                color: #ffffff !important;
            }
            
            .cyber-footer { color: #1e293b !important; }
        </style>
        """

    return textwrap.dedent(BASE_STYLES) + textwrap.dedent(theme_css)

# Default compatibility export to prevent import crashes
CUSTOM_CSS = get_theme_css("Amethyst Violet")
