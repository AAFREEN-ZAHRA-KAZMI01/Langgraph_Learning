import os
import smtplib
from dotenv import load_dotenv
from email.mime.text import MIMEText
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage

# ------------------------------
# 📌 Load sensitive credentials from .env file
# ------------------------------
load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")        # Your Gmail address
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")      # Gmail app password
GROQ_API_KEY = os.getenv("GROQ_API_KEY")          # Your Groq API key

# ------------------------------
# 🧠 Initialize Groq LLM (LLaMA3)
# ------------------------------
llm = ChatGroq(
    temperature=0.3,
    groq_api_key=GROQ_API_KEY,
    model_name="llama3-8b-8192"  # Lightweight and fast model
)

# ------------------------------
# 📤 Function to send email
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
# 🤖 Main chatbot loop
# ------------------------------
def main():
    print("🤖 Welcome to the Groq-Powered Email Chatbot!")
    print("Type your message. Type 'exit' to quit.\n")

    while True:
        # 🔹 Take user input
        user_input = input("🧑 You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("👋 Goodbye!")
            break

        # 🔹 Get response from LLM
        response = llm([HumanMessage(content=user_input)])
        print("🤖 Bot:", response.content)

        # 🔹 Ask whether to send the response via email
        send_choice = input("📩 Do you want to send this reply via email? (y/n): ").strip().lower()
        if send_choice == "y":
            to_email = input("📧 Enter recipient's email address: ").strip()
            send_email(subject="Message from Your AI Chatbot", body=response.content, to_email=to_email)

# ------------------------------
# 🚀 Run the chatbot
# ------------------------------
if __name__ == "__main__":
    main()
