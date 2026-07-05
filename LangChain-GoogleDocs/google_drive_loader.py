import os
import io
import logging
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from langchain_community.llms import HuggingFaceEndpoint
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Constants
SERVICE_ACCOUNT_FILE = "credentials.json"
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
FILE_ID = "1YW8GoolzMUYpM1AHXxU3bIu5xne551QjoesJQt2M5YQ"
MODEL_NAME = "llama3-8b-8192"

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Authenticate and build service
def authenticate_gdrive():
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('drive', 'v3', credentials=creds)
    return service

# Export and download Google Docs content
def export_google_doc(service, file_id):
    request = service.files().export_media(fileId=file_id, mimeType='text/plain')
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)

    done = False
    while not done:
        status, done = downloader.next_chunk()

    content = fh.getvalue().decode("utf-8")
    return content

# Setup LLaMA (via HuggingFace/Groq)
def setup_llama():
    from langchain_groq import ChatGroq
    return ChatGroq(
        temperature=0,
        model=MODEL_NAME,
        api_key=os.getenv("GROQ_API_KEY")
    )

# Main logic
if __name__ == "__main__":
    logger.info("🚀 Downloading document from Google Drive...")
    try:
        service = authenticate_gdrive()
        doc_content = export_google_doc(service, FILE_ID)

        logger.info("✅ Document downloaded successfully.")
        logger.info("🤖 Summarizing with LLaMA...")

        doc = Document(page_content=doc_content)

        llm = setup_llama()
        chain = load_summarize_chain(llm, chain_type="stuff")
        summary = chain.run([doc])

        print("\n📄 Summary:\n")
        print(summary)

    except Exception as e:
        logger.error(f"❌ Error: {e}")
