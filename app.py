import io
import streamlit as st
from pypdf import PdfReader
from docx import Document
from services.ai_analyzer import ask_ollama, analyze_image
from services.vector_store import add_document, search_documents
# --------------------------------------------------
# PAGE SETTINGS
# --------------------------------------------------
st.set_page_config(
    page_title="ThinkVault",
    page_icon="✦",
    layout="wide"
)
# --------------------------------------------------
# CUSTOM DESIGN
# --------------------------------------------------
st.markdown("""
<style>
/* ================================================
   MAIN APP
================================================ */
.stApp {
    background:
        radial-gradient(circle at 10% 10%, #eadcff 0%, transparent 25%),
        radial-gradient(circle at 90% 15%, #cfeeff 0%, transparent 25%),
        radial-gradient(circle at 50% 100%, #ffe5c7 0%, transparent 30%),
        #f8f7fc;
    font-family: "Trebuchet MS", "Segoe UI", sans-serif;
}
/* ================================================
   PAGE WIDTH
================================================ */
.block-container {
    max-width: 1400px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}
/* ================================================
   THINKVAULT TITLE
================================================ */
.main-title {
    text-align: center;
    font-family: "Trebuchet MS", "Segoe UI", sans-serif;
    font-size: 3.2rem;
    font-weight: 800;
    color: #272343;
    margin-bottom: 0.2rem;
    letter-spacing: 1.5px;
}
.tagline {
    text-align: center;
    font-family: "Trebuchet MS", "Segoe UI", sans-serif;
    font-size: 1.05rem;
    color: #77738a;
    margin-bottom: 2rem;
    letter-spacing: 0.3px;
}
/* ================================================
   MAIN CARDS
================================================ */
.card {
    background: rgba(255, 255, 255, 0.88);
    border-radius: 20px;
    padding: 1.4rem;
    box-shadow: 0 8px 30px rgba(60, 50, 90, 0.08);
    margin-bottom: 1rem;
}
.card-title {
    font-family: "Trebuchet MS", "Segoe UI", sans-serif;
    font-size: 1.35rem;
    font-weight: 700;
    color: #272343;
    margin-bottom: 0.4rem;
}
.card-description {
    font-family: "Trebuchet MS", "Segoe UI", sans-serif;
    color: #77738a;
    font-size: 0.95rem;
}
/* ================================================
   FILE CARDS
================================================ */
.file-card {
    background: #eeeaf5;
    border-radius: 14px;
    padding: 0.75rem 0.9rem;
    margin-bottom: 0.6rem;
    color: #38354d;
    font-family: "Trebuchet MS", "Segoe UI", sans-serif;
    font-weight: 600;
}
/* ================================================
   ALL BUTTONS
================================================ */
.stButton > button {
    background-color: #e2ddea;
    color: #38354d;
    border: 1px solid #cfc6db;
    border-radius: 14px;
    min-height: 45px;
    font-family: "Trebuchet MS", "Segoe UI", sans-serif;
    font-size: 0.96rem;
    font-weight: 700;
    box-shadow: 0 3px 8px rgba(60, 50, 90, 0.08);
    transition:
        background-color 0.2s ease,
        border-color 0.2s ease,
        transform 0.15s ease,
        box-shadow 0.15s ease;
}
/* ================================================
   BUTTON HOVER
================================================ */
.stButton > button:hover {
    background-color: #d8d0e3;
    border-color: #c1b7cf;
    transform: translateY(-1px);
    box-shadow: 0 5px 12px rgba(60, 50, 90, 0.12);
}
/* ================================================
   BUTTON PRESS
================================================ */
.stButton > button:active {
    transform: translateY(0px);
}
/* ================================================
   FILE UPLOADER
================================================ */
[data-testid="stFileUploader"] {
    background: #f0edf5;
    border-radius: 16px;
    padding: 0.6rem;
}
/* ================================================
   TEXT INPUT
================================================ */
.stTextInput input {
    background-color: #ffffff;
    border-radius: 14px;
    border: 1px solid #d5cfdf;
    font-family: "Trebuchet MS", "Segoe UI", sans-serif;
    font-size: 0.95rem;
}
/* ================================================
   TEXT AREA
================================================ */
.stTextArea textarea {
    background-color: #ffffff;
    border-radius: 14px;
    border: 1px solid #d5cfdf;
    font-family: "Trebuchet MS", "Segoe UI", sans-serif;
}
/* ================================================
   GENERAL TEXT
================================================ */
body,
p,
div,
span,
label {
    font-family: "Trebuchet MS", "Segoe UI", sans-serif;
}
/* ================================================
   HEADINGS
================================================ */
h1,
h2,
h3,
h4 {
    font-family: "Trebuchet MS", "Segoe UI", sans-serif;
    color: #272343;
}
</style>
""", unsafe_allow_html=True)
# --------------------------------------------------
# HEADER
# --------------------------------------------------
st.markdown(
    '<div class="main-title">✦ ThinkVault ✦</div>',
    unsafe_allow_html=True
)
st.markdown(
    '<div class="tagline">'
    'Think smarter. Work better. Discover more.'
    '</div>',
    unsafe_allow_html=True
)
# --------------------------------------------------
# SESSION STORAGE
# --------------------------------------------------
if "files" not in st.session_state:
    st.session_state.files = {}
if "selected_file" not in st.session_state:
    st.session_state.selected_file = None
if "ai_open" not in st.session_state:
    st.session_state.ai_open = False
# --------------------------------------------------
# TWO COLUMN LAYOUT
# --------------------------------------------------
main_area, vault_area = st.columns(
    [2.3, 1],
    gap="large"
)
# ==================================================
# MAIN WORKSPACE
# ==================================================
with main_area:
    st.markdown("""
    <div class="card">
        <div class="card-title">✦ Your Workspace</div>
        <div class="card-description">
            Upload documents or images and explore your content.
        </div>
    </div>
    """, unsafe_allow_html=True)
    # --------------------------------------------------
    # FILE UPLOAD
    # --------------------------------------------------
    uploaded_file = st.file_uploader(
        "📤 Upload a file",
        type=["pdf", "docx", "png", "jpg", "jpeg"]
    )
    # --------------------------------------------------
    # WHEN A FILE IS UPLOADED
    # --------------------------------------------------
    if uploaded_file is not None:
        file_name = uploaded_file.name
        file_data = uploaded_file.getvalue()
        # --------------------------------------------------
        # SAVE FILE IN SESSION
        # --------------------------------------------------
        if file_name not in st.session_state.files:
            st.session_state.files[file_name] = {
                "name": file_name,
                "type": uploaded_file.type,
                "data": file_data
            }
        st.session_state.selected_file = file_name
        st.success(
            f"✓ {file_name} uploaded successfully."
        )
        # --------------------------------------------------
        # PDF
        # --------------------------------------------------
        if file_name.lower().endswith(".pdf"):
            reader = PdfReader(
                io.BytesIO(file_data)
            )
            text = ""
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            if text.strip():
                add_document(file_name, text)
            st.markdown(
                '<div class="card-title">📄 Document</div>',
                unsafe_allow_html=True
            )
            if text.strip():
                st.text_area(
                    "Document content",
                    text,
                    height=400
                )
            else:
                st.info(
                    "This PDF does not contain readable text."
                )
        # --------------------------------------------------
        # DOCX
        # --------------------------------------------------
        elif file_name.lower().endswith(".docx"):
            document = Document(
                io.BytesIO(file_data)
            )
            text = ""
            for paragraph in document.paragraphs:
                if paragraph.text.strip():
                    text += paragraph.text + "\n"
            if text.strip():
                add_document(file_name, text)
            st.markdown(
                '<div class="card-title">📝 Document</div>',
                unsafe_allow_html=True
            )
            if text.strip():
                st.text_area(
                    "Document content",
                    text,
                    height=400
                )
            else:
                st.info(
                    "No readable text was found."
                )
        # --------------------------------------------------
        # IMAGE
        # --------------------------------------------------
        elif file_name.lower().endswith(
            (".png", ".jpg", ".jpeg")
        ):
            st.markdown(
                '<div class="card-title">🖼️ Image</div>',
                unsafe_allow_html=True
            )
            st.image(
                file_data,
                use_container_width=True
            )
        # --------------------------------------------------
        # ASK THINKVAULT BUTTON
        # --------------------------------------------------
        st.markdown(
            "<br>",
            unsafe_allow_html=True
        )
        if st.button(
            "✦ Ask ThinkVault",
            use_container_width=True
        ):
            st.session_state.ai_open = True
        # --------------------------------------------------
        # AI ASSISTANT AREA
        # --------------------------------------------------
        if st.session_state.get("ai_open", False):
            st.markdown("### ✦ ThinkVault")
            question = st.text_input(
                "What would you like to know?",
                placeholder="Ask something about your content..."
            )
            if st.button(
                "Ask ✦",
                use_container_width=True
            ):
                if question.strip():
                    try:
                        # ----------------------------------
                        # IMAGE QUESTION
                        # ----------------------------------
                        if file_name.lower().endswith(
                            (".png", ".jpg", ".jpeg")
                        ):
                            with st.spinner(
                                "ThinkVault is analyzing the image..."
                            ):
                                answer = analyze_image(
                                    question,
                                    file_data
                                )
                        # ----------------------------------
                        # PDF / DOCX QUESTION
                        # ----------------------------------
                        else:
                            with st.spinner(
                                "ThinkVault is thinking..."
                            ):
                                results = search_documents(
                                    question,
                                    n_results=5,
                                    file_name=file_name
                                )

                                relevant_chunks = []

                                for document, metadata in results:

                                    if metadata.get("file_name") == file_name:

                                        relevant_chunks.append(document)

                                context = "\n\n".join(
                                    relevant_chunks
                                )

                                answer = ask_ollama(
                                    question=question,
                                    context=context
                                )
                        # ----------------------------------
                        # DISPLAY ANSWER
                        # ----------------------------------
                        st.markdown(
                            "### ✦ ThinkVault"
                        )
                        st.write(answer)
                    except Exception as e:
                        st.error(
                            "ThinkVault could not process your request."
                        )
                        st.caption(
                            f"Error: {e}"
                        )
                else:
                    st.warning(
                        "Please enter a question."
                    )
# ==================================================
# RIGHT SIDE — YOUR VAULT
# ==================================================
with vault_area:
    st.markdown("""
    <div class="card">
        <div class="card-title">📚 Your Vault</div>
        <div class="card-description">
            Your uploaded files.
        </div>
    </div>
    """, unsafe_allow_html=True)
    # --------------------------------------------------
    # DISPLAY FILES
    # --------------------------------------------------
    if st.session_state.files:
        for file_name in st.session_state.files:
            if file_name.lower().endswith(
                (".png", ".jpg", ".jpeg")
            ):
                icon = "🖼️"
            elif file_name.lower().endswith(".docx"):
                icon = "📝"
            else:
                icon = "📄"
            if st.button(
                f"{icon}  {file_name}",
                key=f"file_{file_name}",
                use_container_width=True
            ):
                st.session_state.selected_file = file_name
    else:
        st.markdown("""
        <div class="file-card">
            📭 No files uploaded yet.
        </div>
        """, unsafe_allow_html=True)