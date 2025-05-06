import streamlit as st
import os
from pdf_processor import PDFProcessor
from langchain.chains import ConversationalRetrievalChain
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Assistant PDF", layout="wide")

def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "vector_store" not in st.session_state:
        st.session_state.vector_store = None

def main():
    st.title("Assistant PDF Intelligent")
    
    # Initialisation de l'état de la session
    initialize_session_state()
    
    # Sidebar pour le téléchargement des PDF
    with st.sidebar:
        st.header("Gestion des Documents")
        uploaded_files = st.file_uploader("Téléchargez vos PDFs", type="pdf", accept_multiple_files=True)
        
        if uploaded_files:
            processor = PDFProcessor()
            for uploaded_file in uploaded_files:
                # Sauvegarder le fichier temporairement
                with open(os.path.join("data", uploaded_file.name), "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # Traiter le PDF
                texts = processor.process_pdf(os.path.join("data", uploaded_file.name))
                if st.session_state.vector_store is None:
                    st.session_state.vector_store = processor.create_vector_store(
                        texts, "main_collection"
                    )
                else:
                    # Ajouter les nouveaux documents au vector store existant
                    st.session_state.vector_store.add_documents(texts)
            
            st.success("PDFs traités avec succès!")
    
    # Zone de chat principale
    st.header("Chat avec vos documents")
    
    # Afficher l'historique des messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Zone de saisie pour les questions
    if prompt := st.chat_input("Posez votre question ici..."):
        # Ajouter le message de l'utilisateur
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Préparer la chaîne de conversation
        if st.session_state.vector_store:
            llm = ChatOpenAI(temperature=0)
            qa_chain = ConversationalRetrievalChain.from_llm(
                llm=llm,
                retriever=st.session_state.vector_store.as_retriever()
            )
            
            # Obtenir la réponse
            response = qa_chain({"question": prompt, "chat_history": []})
            
            # Afficher la réponse
            with st.chat_message("assistant"):
                st.markdown(response["answer"])
                st.session_state.messages.append({"role": "assistant", "content": response["answer"]})

if __name__ == "__main__":
    main() 