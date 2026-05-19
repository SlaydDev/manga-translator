import streamlit as st
import google.generativeai as genai
from groq import Groq
from PIL import Image
import io
import time

# --- STAGE 0: CORE WINDOW & RESPONSIVE CONFIG ---
st.set_page_config(
    page_title="Manga Translator", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# --- ADVANCED CATPPUCCIN MOCHA STYLING & ANIMATIONS ---
st.markdown("""
    <style>
    /* Responsive Root Setup */
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #11111b !important;
        color: #cdd6f4 !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Elegant Boot Splash Screen Overlay */
    #boot-splash {
        position: fixed;
        top: 0; left: 0; width: 100vw; height: 100vh;
        background-color: #11111b;
        z-index: 999999;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        animation: fadeOut 1s ease-in-out 3.5s forwards;
        pointer-events: none;
    }
    .boot-logo {
        width: 140px;
        height: 140px;
        border-radius: 50%;
        border: 4px solid #89b4fa;
        box-shadow: 0 0 20px #89b4fa;
        animation: spinZoom 2.5s cubic-bezier(0.25, 1, 0.5, 1) 0.5s forwards;
        opacity: 0;
        transform: scale(0.3) rotate(0deg);
    }
    .boot-text {
        margin-top: 25px;
        text-align: center;
        opacity: 0;
        animation: fadeInUp 1.2s ease-out 1.8s forwards;
    }
    .boot-title {
        font-size: 1.6rem;
        font-weight: 700;
        color: #b4befe;
        letter-spacing: 2px;
        margin-bottom: 4px;
    }
    .boot-subtitle {
        font-size: 1rem;
        color: #a6adc8;
        font-weight: 300;
    }

    /* Key Entry & Control Cards */
    .glass-card {
        background: #1e1e2e;
        border: 1px solid #313244;
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
    }
    
    /* Clean Mobile-Friendly Form Overrides */
    .stButton>button {
        width: 100% !important;
        background: linear-gradient(135deg, #cba6f7 0%, #89b4fa 100%) !important;
        color: #11111b !important;
        border-radius: 12px !important;
        border: none !important;
        padding: 12px 24px !important;
        font-weight: bold !important;
        font-size: 1rem !important;
        box-shadow: 0 4px 15px rgba(203, 166, 247, 0.2);
        transition: all 0.3s ease;
    }
    .stButton>button:active {
        transform: scale(0.98);
    }
    
    /* Animations Keyframes */
    @keyframes spinZoom {
        0% { transform: scale(0.3) rotate(0deg); opacity: 0; }
        50% { opacity: 1; }
        100% { transform: scale(1) rotate(360deg); opacity: 1; }
    }
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes fadeOut {
        from { opacity: 1; visibility: visible; }
        to { opacity: 0; visibility: hidden; display: none; }
    }
    </style>
    
    <div id="boot-splash">
        <img class="boot-logo" src="https://i.postimg.cc/2Sdb2GX0/channels4-profile.jpg" onerror="this.src='https://yt3.googleusercontent.com/dyS7hyzcNE0xSfVDOVkRfsv8mqRr5ke-oEfA1koh5u5qPLK9kpjj1E73-AxbiFZM9OE5_e529g=s160-c-k-c0x00ffffff-no-rj'">
        <div class="boot-text">
            <div class="boot-title">CaptainEXE Studios</div>
            <div class="boot-subtitle">Slayd Development</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- STATE SESSION STORAGE CONTROL ---
if 'keys_verified' not in st.session_state:
    st.session_state['keys_verified'] = False

# --- WINDOW 1: KEY ACCREDITATION AND SUBMISSION SCREEN ---
if not st.session_state['keys_verified']:
    st.markdown("<div style='height: 8vh;'></div>", unsafe_allow_html=True)
    
    col_l, col_m, col_r = st.columns([1, 10, 1])
    with col_m:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; margin-top:0; color:#89b4fa;'>System Authentication</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color:#a6adc8;'>Securely supply processing endpoints to unlock the core engine layer.</p>", unsafe_allow_html=True)
        
        in_gemini = st.text_input("Google AI Key", type="password", help="Input valid Gemini API token environment sequence.")
        in_groq = st.text_input("Groq Link Key", type="password", help="Input valid Groq environment authentication token.")
        
        st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
        
        if st.button("Unlock Core Engine"):
            if in_gemini.strip() and in_groq.strip():
                st.session_state['gemini_key'] = in_gemini.strip()
                st.session_state['groq_key'] = in_groq.strip()
                st.session_state['keys_verified'] = True
                st.rerun()
            else:
                st.error("Both parameter strings must be populated prior to engine access.")
        st.markdown('</div>', unsafe_allow_html=True)

# --- WINDOW 2: TRANSLATION ENGINE PRODUCTION LAYER ---
else:
    st.markdown("<h2 style='margin:0; padding:0; color:#cba6f7;'>Translator Interface</h2>", unsafe_allow_html=True)
    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

    # UI Splitting across screen scales
    layout_left, layout_right = st.columns([1, 1])

    with layout_left:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("<h4 style='margin-top:0; color:#89b4fa;'>Config & Mode</h4>", unsafe_allow_html=True)
        
        mode = st.radio(
            "Translation Mode Select:", 
            ("ECO Mode (Raw Text)", "PRO Mode (Image Regen Output)"),
            label_visibility="collapsed"
        )
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("<h4 style='margin-top:0; color:#89b4fa;'>Image Source Selection</h4>", unsafe_allow_html=True)
        
        source_type = st.segmented_control(
            "Source", ["Upload File", "Use Camera"], default="Upload File", label_visibility="collapsed"
        )
        
        uploaded_file = None
        if source_type == "Upload File":
            uploaded_file = st.file_uploader("Choose Japanese Manga File", type=["jpg", "jpeg", "png"], label_visibility="collapsed")
        else:
            uploaded_file = st.camera_input("Capture Panel Screen Frame")
        st.markdown('</div>', unsafe_allow_html=True)

    with layout_right:
        if uploaded_file:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("<h4 style='margin-top:0; color:#a6adc8;'>Engine Trigger</h4>", unsafe_allow_html=True)
            
            if st.button("Execute Engine Translation"):
                genai.configure(api_key=st.session_state['gemini_key'])
                groq_client = Groq(api_key=st.session_state['groq_key'])
                
                img_data = Image.open(uploaded_file)
                
                with st.spinner("Processing structural matrix..."):
                    try:
                        # Extract utilizing Gemini 3.1 Flash Lite
                        model = genai.GenerativeModel('gemini-3.1-flash-lite')
                        ocr_prompt = "Parse this file. Extract structural dialogue bubbles, narration, and raw text context directly from right-to-left layout constraints."
                        response = model.generate_content([ocr_prompt, img_data])
                        raw_japanese = response.text

                        # Transference directly to Groq Llama 3.1 8B Instant
                        localization_job = groq_client.chat.completions.create(
                            messages=[
                                {
                                    "role": "system",
                                    "content": "You are an specialized manga structural translation parser. Adapt dialogue sequences into clean, localized conversational English."
                                },
                                {
                                    "role": "user",
                                    "content": f"Source structural text to process:\n{raw_japanese}"
                                }
                            ],
                            model="llama-3.1-8b-instant",
                        )
                        english_result = localization_job.choices[0].message.content

                        if "ECO" in mode:
                            st.markdown("### Localized Content Output")
                            st.write(english_result)
                        else:
                            st.markdown("### Reconstructed Structural Layout")
                            st.image(img_data, use_container_width=True)
                            st.markdown("#### English Overlay Text Map Layer")
                            st.code(english_result, language="markdown")
                            
                    except Exception as failure_node:
                        st.error(f"Execution fault thrown within engine array: {failure_node}")
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown("<p style='text-align:center; color:#585b70; margin-top:40px;'>Awaiting input stream target selection...</p>", unsafe_allow_html=True)

    # --- BRANDING & FOOTER INFRASTRUCTURE ---
    st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
    st.markdown("""
        <hr style='border: 0; height: 1px; background: #313244;'>
        <div style='text-align: center; color: #a6adc8; font-size: 0.9rem;'>
            <p style='margin:4px;'>Application Architecture curated by <b>CaptainEXE Studios</b> × <b>Slayd Development</b></p>
            <p style='margin:4px;'>
                <a href="https://github.com/slayddev" target="_blank" style="text-decoration:none;">GitHub</a> | 
                <a href="https://youtube.com/@itscaptainexe" target="_blank" style="text-decoration:none;">YouTube</a>
            </p>
        </div>
    """, unsafe_allow_html=True)