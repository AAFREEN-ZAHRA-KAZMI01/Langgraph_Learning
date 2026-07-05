
import os
import smtplib
from dotenv import load_dotenv
from email.mime.text import MIMEText
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage
from langsmith import traceable

# ------------------------------
# 🔐 Load Environment Variables
# ------------------------------
load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
LANGCHAIN_PROJECT = os.getenv("LANGCHAIN_PROJECT", "my-email-chatbot-project")
LANGCHAIN_ENDPOINT = os.getenv("LANGCHAIN_ENDPOINT", "https://api.smith.langchain.com")

# Set LangSmith environment variables
os.environ["LANGCHAIN_API_KEY"] = LANGCHAIN_API_KEY
os.environ["LANGCHAIN_PROJECT"] = LANGCHAIN_PROJECT
os.environ["LANGCHAIN_ENDPOINT"] = LANGCHAIN_ENDPOINT

# ------------------------------
# 🤖 Initialize LLM (Groq + LLaMA3)
# ------------------------------
llm = ChatGroq(
    temperature=0.3,
    groq_api_key=GROQ_API_KEY,
    model_name="llama3-8b-8192"
)

# ------------------------------
# 🔁 Chat Function with LangSmith Tracing
# ------------------------------
@traceable
def chat_with_llm(user_input):
    return llm([HumanMessage(content=user_input)])

# ------------------------------
# 📤 Email Function
# ------------------------------
def send_email(subject, body, to_email):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, to_email, msg.as_string())
        print("✅ Email sent successfully.")
    except Exception as e:
        print("❌ Failed to send email:", str(e))

# ------------------------------
# 🧠 Main Chatbot Loop
# ------------------------------
def main():
    print("🤖 Welcome to the Groq + LangSmith Email Chatbot!")
    print("Type your message. Type 'exit' to quit.\n")

    while True:
        user_input = input("🧑 You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("👋 Goodbye!")
            break

        # Generate LLM response with LangSmith trace
        response = chat_with_llm(user_input)
        print("🤖 Bot:", response.content)

        # Ask if user wants to send email
        send_choice = input("📩 Send this reply via email? (y/n): ").strip().lower()
        if send_choice == "y":
            to_email = input("📧 Enter recipient email: ").strip()
            send_email(subject="AI Chatbot Response", body=response.content, to_email=to_email)

# ------------------------------
# 🚀 Run the Program
# ------------------------------
if __name__ == "__main__":
    main()
