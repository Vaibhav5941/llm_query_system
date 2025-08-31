# import os
# import django

# # Setup Django environment before imports
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "llm_query_system.settings")
# django.setup()

# from core.models import Document
# from core.logic.cache import check_cache_or_query_llm

# import streamlit as st

# # Page config (must be first Streamlit command)
# st.set_page_config(page_title="LLM Document Query System", layout="wide")
# # Custom title with image + futuristic font
# st.markdown("""
#     <style>
#     @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&display=swap');
    
#  .custom-title {
#         font-family: 'Orbitron', sans-serif;
#         font-size: clamp(20px, 4vw, 38px); /* Responsive font size */
#         font-weight: bold;
#         color: #485460;
#         display: flex;
#         align-items: center;
#         gap: 12px;
#         text-shadow: 0 0 10px rgba(0, 234, 255, 0.7);
#         flex-wrap: wrap; /* Allows wrapping on smaller screens */
#     }

#     .custom-title img {
#         height: clamp(35px, 5vw, 55px); /* Responsive image size */
#         width: clamp(35px, 5vw, 55px);
#     }

#     @media (max-width: 480px) {
#         .custom-title {
#             flex-direction: column; /* Stack logo above text on very small screens */
#             text-align: center;
#         }
#     }
#     </style>
#     <div class="custom-title">
#         <img src="https://cdn-icons-png.flaticon.com/512/3558/3558866.png" alt="Logo">
#         LLM-Powered Document Query Assistant
#     </div>
# """, unsafe_allow_html=True)


# # Load custom CSS
# def local_css(css_text):
#     st.markdown(f"<style>{css_text}</style>", unsafe_allow_html=True)

# local_css("""
# @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');

# html, body, [class*="css"] {
#     font-family: 'Montserrat', sans-serif;
#     background: linear-gradient(135deg, #0a1f44, #001233);
#     color: white;
#     margin: 0;
#     padding: 0;
# }

# h1, h2, h3, h4 {
#     color: #00eaff;
#     font-weight: 700;
# }

# .stChatMessage {
#     background-color: rgba(0, 234, 255, 0.07);
#     border: 1px solid rgba(0, 234, 255, 0.3);
#     border-radius: 10px;
#     padding: 10px;
#     margin-bottom: 10px;
# }

# /* Buttons */
# button[kind="primary"], .stButton button {
#     background: linear-gradient(135deg, #00f7ff, #0066ff) !important;
#     color: #ffffff !important;
#     border-radius: 10px !important;
#     font-weight: bold !important;
#     border: none !important;
#     box-shadow: 0 0 10px rgba(0, 247, 255, 0.4);
#     transition: all 0.2s ease;
# }

# button[kind="primary"]:hover, .stButton button:hover {
#     background: linear-gradient(135deg, #00d5ff, #0044aa) !important;
#     box-shadow: 0 0 16px rgba(0, 247, 255, 0.7);
#     transform: scale(1.03);
# }

# /* Inputs */
# .stTextInput textarea, .stTextInput input {
#     background-color: rgba(255,255,255,0.1) !important;
#     color: white !important;
#     border: 1px solid #00eaff !important;
# }

# .stSelectbox div[data-baseweb="select"] {
#     background-color: rgba(255,255,255,0.05);
#     border: 1px solid #00eaff;
#     border-radius: 8px;
#     color: white;
# }

# /* Responsive layout */
# @media (max-width: 768px) {
#     .custom-title {
#         font-size: 22px !important;
#         flex-direction: column;
#         text-align: center;
#     }
#     .custom-title img {
#         height: 45px;
#         width: 45px;
#     }
#     .stChatMessage {
#         font-size: 14px;
#     }
#     button[kind="primary"], .stButton button {
#         font-size: 14px !important;
#         padding: 6px 12px !important;
#     }
# }
# """)

# # Load documents
# documents = Document.objects.all()
# doc_options = {doc.title: doc.id for doc in documents}

# # Initialize chat history
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []

# # Add Clear Chat button


# if not doc_options:
#     st.warning("No documents found in database. Please run ingest_pdfs.py to add documents.")
# else:
#     selected_title = st.selectbox("Choose a policy document", options=list(doc_options.keys()))
#     selected_document_id = doc_options[selected_title]



#     # Display previous messages
#     for msg in st.session_state.chat_history:
#         with st.chat_message(msg["role"]):
#             st.markdown(msg["content"])

#     # Chat input
#     question = st.chat_input("Ask your question...")

#     if question:
#         # Append user message
#         st.session_state.chat_history.append({"role": "user", "content": question})

#         # Display user message
#         with st.chat_message("user"):
#             st.markdown(question)

#         # Prepare conversation text
#         conversation_text = ""
#         for m in st.session_state.chat_history:
#             conversation_text += f"{m['role'].capitalize()}: {m['content']}\n"

#         # Call LLM
#         with st.spinner("Thinking..."):
#             response = check_cache_or_query_llm(
#                 question.strip(),
#                 selected_document_id
#             )

#         llm_text = (
#             f"Decision: {response['decision']}\n\n"
#             f"Amount: {response.get('amount', 'N/A')}\n\n"
#             f"**Justification:**\n{response['llm_response']}\n\n"
#             f"**Cached:** `{response['cached']}`"
#         )

#         # Append assistant reply
#         st.session_state.chat_history.append({"role": "assistant", "content": llm_text})

#         # Display assistant reply
#         with st.chat_message("assistant"):
#             st.markdown(
#                 f"<div style='display:flex;align-items:center;'>"
#                 f"<img src='https://cdn-icons-png.flaticon.com/512/4712/4712107.png' width='30' style='margin-right:10px;'>"
#                 f"<span>{llm_text}</span></div>",
#                 unsafe_allow_html=True
#             )
# if st.button("Clear Chat", type="primary"):
#     st.session_state.chat_history = []
#     st.rerun()            

import os
import streamlit as st

# Page config (must be first Streamlit command)
st.set_page_config(page_title="LLM Document Query System", layout="wide")

# Initialize variables
django_available = False
documents = []
doc_options = {}
Document = None
check_cache_or_query_llm = None

# Try to setup Django and import models
try:
    import django
    # Setup Django environment before imports
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "llm_query_system.settings")
    django.setup()
    
    from core.models import Document
    from core.logic.cache import check_cache_or_query_llm
    
    # Test database connection
    documents = Document.objects.all()
    doc_options = {doc.title: doc.id for doc in documents}
    django_available = True
    
except Exception as e:
    st.error(f"⚠️ Database/Django setup failed: {str(e)}")
    st.info("The app is running but database features are unavailable. Please check your Django configuration and database connection.")
    django_available = False

# Custom title with image + futuristic font
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&display=swap');
    
 .custom-title {
        font-family: 'Orbitron', sans-serif;
        font-size: clamp(20px, 4vw, 38px); /* Responsive font size */
        font-weight: bold;
        color: #485460;
        display: flex;
        align-items: center;
        gap: 12px;
        text-shadow: 0 0 10px rgba(0, 234, 255, 0.7);
        flex-wrap: wrap; /* Allows wrapping on smaller screens */
    }

    .custom-title img {
        height: clamp(35px, 5vw, 55px); /* Responsive image size */
        width: clamp(35px, 5vw, 55px);
    }

    @media (max-width: 480px) {
        .custom-title {
            flex-direction: column; /* Stack logo above text on very small screens */
            text-align: center;
        }
    }
    </style>
    <div class="custom-title">
        <img src="https://cdn-icons-png.flaticon.com/512/3558/3558866.png" alt="Logo">
        LLM-Powered Document Query Assistant
    </div>
""", unsafe_allow_html=True)

# Load custom CSS
def local_css(css_text):
    st.markdown(f"<style>{css_text}</style>", unsafe_allow_html=True)

local_css("""
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Montserrat', sans-serif;
    background: linear-gradient(135deg, #0a1f44, #001233);
    color: white;
    margin: 0;
    padding: 0;
}

h1, h2, h3, h4 {
    color: #00eaff;
    font-weight: 700;
}

.stChatMessage {
    background-color: rgba(0, 234, 255, 0.07);
    border: 1px solid rgba(0, 234, 255, 0.3);
    border-radius: 10px;
    padding: 10px;
    margin-bottom: 10px;
}

/* Buttons */
button[kind="primary"], .stButton button {
    background: linear-gradient(135deg, #00f7ff, #0066ff) !important;
    color: #ffffff !important;
    border-radius: 10px !important;
    font-weight: bold !important;
    border: none !important;
    box-shadow: 0 0 10px rgba(0, 247, 255, 0.4);
    transition: all 0.2s ease;
}

button[kind="primary"]:hover, .stButton button:hover {
    background: linear-gradient(135deg, #00d5ff, #0044aa) !important;
    box-shadow: 0 0 16px rgba(0, 247, 255, 0.7);
    transform: scale(1.03);
}

/* Inputs */
.stTextInput textarea, .stTextInput input {
    background-color: rgba(255,255,255,0.1) !important;
    color: white !important;
    border: 1px solid #00eaff !important;
}

.stSelectbox div[data-baseweb="select"] {
    background-color: rgba(255,255,255,0.05);
    border: 1px solid #00eaff;
    border-radius: 8px;
    color: white;
}

/* Responsive layout */
@media (max-width: 768px) {
    .custom-title {
        font-size: 22px !important;
        flex-direction: column;
        text-align: center;
    }
    .custom-title img {
        height: 45px;
        width: 45px;
    }
    .stChatMessage {
        font-size: 14px;
    }
    button[kind="primary"], .stButton button {
        font-size: 14px !important;
        padding: 6px 12px !important;
    }
}
""")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Show different content based on Django availability
if not django_available:
    st.warning("⚠️ Database connection unavailable. Please check your Django configuration.")
    st.info("💡 Possible fixes:\n- Check DATABASE_URL environment variable\n- Verify Django settings\n- Ensure database is accessible")
    
    # Show a basic interface even without database
    st.subheader("Demo Mode")
    question = st.chat_input("Ask your question (demo mode - no database)...")
    if question:
        st.chat_message("user").write(question)
        st.chat_message("assistant").write("Database is unavailable. Please fix the connection to use the full functionality.")

elif not doc_options:
    st.warning("No documents found in database. Please run ingest_pdfs.py to add documents.")
    
else:
    # Full functionality when Django is available
    selected_title = st.selectbox("Choose a policy document", options=list(doc_options.keys()))
    selected_document_id = doc_options[selected_title]

    # Display previous messages
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input
    question = st.chat_input("Ask your question...")

    if question:
        # Append user message
        st.session_state.chat_history.append({"role": "user", "content": question})

        # Display user message
        with st.chat_message("user"):
            st.markdown(question)

        # Prepare conversation text
        conversation_text = ""
        for m in st.session_state.chat_history:
            conversation_text += f"{m['role'].capitalize()}: {m['content']}\n"

        # Call LLM with error handling
        try:
            with st.spinner("Thinking..."):
                response = check_cache_or_query_llm(
                    question.strip(),
                    selected_document_id
                )

            llm_text = (
                f"Decision: {response['decision']}\n\n"
                f"Amount: {response.get('amount', 'N/A')}\n\n"
                f"**Justification:**\n{response['llm_response']}\n\n"
                f"**Cached:** `{response['cached']}`"
            )

            # Append assistant reply
            st.session_state.chat_history.append({"role": "assistant", "content": llm_text})

            # Display assistant reply
            with st.chat_message("assistant"):
                st.markdown(
                    f"<div style='display:flex;align-items:center;'>"
                    f"<img src='https://cdn-icons-png.flaticon.com/512/4712/4712107.png' width='30' style='margin-right:10px;'>"
                    f"<span>{llm_text}</span></div>",
                    unsafe_allow_html=True
                )
                
        except Exception as e:
            st.error(f"Error processing your question: {str(e)}")
            st.session_state.chat_history.append({"role": "assistant", "content": f"Sorry, I encountered an error: {str(e)}"})

# Clear Chat button
if st.button("Clear Chat", type="primary"):
    st.session_state.chat_history = []
    st.rerun()