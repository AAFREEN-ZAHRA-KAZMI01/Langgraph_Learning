import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from notion_client import Client as NotionClient

# Load credentials
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
NOTION_API_KEY = os.getenv("NOTION_API_KEY")

# Initialize LLM
llm = ChatGroq(api_key=GROQ_API_KEY, model_name="llama3-70b-8192")

# Initialize Notion client
notion = NotionClient(auth=NOTION_API_KEY)

# --- Function to save to Notion ---
def save_to_notion(title, content):
    try:
        page_id = input("📄 Enter Notion page ID where you want to save: ").strip()

        notion.pages.create(
            parent={"type": "page_id", "page_id": page_id},
            properties={
                "title": [{"type": "text", "text": {"content": title}}],
            },
            children=[{
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": content}}]
                }
            }]
        )
        print(f"✅ Saved to Notion page titled '{title}'")
    except Exception as e:
        print(f"❌ Error saving to Notion: {e}")

# --- Generate professional document ---
def generate_new_document():
    topic = input("🧠 Enter topic to generate document: ").strip()
    print("📄 Generating document...")

    try:
        prompt = f"Write a detailed professional technical documentation about: {topic}"
        result = llm.invoke([HumanMessage(content=prompt)]).content
        print("\n📄 Generated Document:\n")
        print(result)

        save = input("\n💾 Save this document to Notion? (yes/no): ").strip().lower()
        if save == "yes":
            title = input("📌 Enter title for Notion page: ").strip()
            save_to_notion(title, result)
    except Exception as e:
        print(f"❌ Error generating document: {e}")

# --- Summarize a Notion document ---
def summarize_existing_notion():
    page_id = input("📄 Enter Notion Page ID to summarize: ").strip()

    try:
        blocks = notion.blocks.children.list(block_id=page_id)["results"]
    except Exception as e:
        print(f"❌ Failed to fetch Notion content: {e}")
        return

    # Extract all text
    def extract_text(blocks):
        text = []
        for block in blocks:
            t = block.get(block["type"], {}).get("rich_text", [])
            text.extend([x.get("plain_text", "") for x in t])
            if block.get("has_children"):
                children = notion.blocks.children.list(block["id"]).get("results", [])
                text.extend(extract_text(children))
        return text

    content = "\n".join(extract_text(blocks))

    print("🧠 Generating summary...")
    try:
        summary = llm.invoke([HumanMessage(content=f"Summarize this Notion content:\n\n{content}")]).content
        print("\n📌 Summary:\n", summary)

        save = input("\n💾 Save this summary to Notion? (yes/no): ").strip().lower()
        if save == "yes":
            title = input("📌 Enter title for summary page: ").strip()
            save_to_notion(title, summary)
    except Exception as e:
        print(f"❌ Error summarizing document: {e}")

# --- Main menu loop ---
def main():
    print("📘 Notion + LLM Document Assistant")
    print("----------------------------------")
    while True:
        print("\n1. ✍️  Generate new document from topic")
        print("2. 📚 Summarize existing Notion document")
        print("3. ❌ Exit")
        choice = input("👉 Choose an option (1/2/3): ").strip()

        if choice == "1":
            generate_new_document()
        elif choice == "2":
            summarize_existing_notion()
        elif choice == "3" or choice.lower() == "exit":
            print("👋 Exiting. Bye!")
            break
        else:
            print("❌ Invalid option. Please choose 1, 2, or 3.")

if __name__ == "__main__":
    main()
