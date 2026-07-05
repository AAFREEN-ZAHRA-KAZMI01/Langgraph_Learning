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
llm = ChatGroq(api_key=GROQ_API_KEY, model_name="llama-3.3-70b-versatile")

# Initialize Notion client
notion = NotionClient(auth=NOTION_API_KEY)


# --- Save content to an existing Notion page ---
def save_to_notion(title, content, page_id):
    try:
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
        return True
    except Exception as e:
        print(f"❌ Error saving to Notion: {e}")
        return False


# --- Generate a document for a topic ---
def generate_document_content(topic):
    prompt = f"Write a detailed professional technical documentation about: {topic}"
    return llm.invoke([HumanMessage(content=prompt)]).content


def generate_new_document():
    topic = input("🧠 Enter topic to generate document: ").strip()
    print("📄 Generating document...")

    try:
        result = generate_document_content(topic)
        print("\n📄 Generated Document:\n")
        print(result)

        save = input("\n💾 Save this document to Notion? (yes/no): ").strip().lower()
        if save == "yes":
            title = input("📌 Enter title for Notion page: ").strip()
            page_id = input("📄 Enter Notion page ID where you want to save: ").strip()
            save_to_notion(title, result, page_id)
    except Exception as e:
        print(f"❌ Error generating document: {e}")


# --- Summarize an existing Notion document ---
def _extract_text(notion_client, blocks):
    text = []
    for block in blocks:
        t = block.get(block["type"], {}).get("rich_text", [])
        text.extend([x.get("plain_text", "") for x in t])
        if block.get("has_children"):
            children = notion_client.blocks.children.list(block["id"]).get("results", [])
            text.extend(_extract_text(notion_client, children))
    return text


def summarize_notion_page(page_id):
    blocks = notion.blocks.children.list(block_id=page_id)["results"]
    content = "\n".join(_extract_text(notion, blocks))
    return llm.invoke([HumanMessage(content=f"Summarize this Notion content:\n\n{content}")]).content


def summarize_existing_notion():
    page_id = input("📄 Enter Notion Page ID to summarize: ").strip()

    try:
        summary = summarize_notion_page(page_id)
    except Exception as e:
        print(f"❌ Failed to fetch/summarize Notion content: {e}")
        return

    print("\n📌 Summary:\n", summary)

    save = input("\n💾 Save this summary to Notion? (yes/no): ").strip().lower()
    if save == "yes":
        title = input("📌 Enter title for summary page: ").strip()
        target_page_id = input("📄 Enter Notion page ID where you want to save: ").strip()
        save_to_notion(title, summary, target_page_id)


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
