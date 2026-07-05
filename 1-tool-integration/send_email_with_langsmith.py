from langchain.schema import HumanMessage
from langsmith import traceable
from email_utils import get_llm, setup_langsmith_tracing, send_email

setup_langsmith_tracing(default_project="my-email-chatbot-project")
llm = get_llm()

# ------------------------------
# 🔁 Chat Function with LangSmith Tracing
# ------------------------------
@traceable
def chat_with_llm(user_input):
    return llm([HumanMessage(content=user_input)])

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
