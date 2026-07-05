from langchain.schema import HumanMessage
from email_utils import get_llm, setup_langsmith_tracing, send_email

setup_langsmith_tracing()
llm = get_llm()

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
