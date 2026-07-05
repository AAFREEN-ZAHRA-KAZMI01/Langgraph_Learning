"""Flask dashboard for the tools in 1-tool-integration/.

One page with a chat box (talks to the Groq LLM) plus forms to trigger
email, WhatsApp, and Notion actions. Also hosts the Twilio WhatsApp
inbound webhook, since it needs an HTTP server just like the dashboard.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "1-tool-integration"))

from flask import Flask, render_template, request  # noqa: E402
from langchain.schema import HumanMessage  # noqa: E402
from twilio.twiml.messaging_response import MessagingResponse  # noqa: E402

from email_utils import get_llm, send_email  # noqa: E402
from fetch_email_tool import fetch_email_summary, auto_reply_to_unread  # noqa: E402
from whatsapp_tool import send_whatsapp_message, generate_whatsapp_reply  # noqa: E402
from notion_tool import generate_document_content, save_to_notion  # noqa: E402

app = Flask(__name__)
llm = get_llm()


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    message = request.form.get("message", "").strip()
    reply = llm([HumanMessage(content=message)]).content if message else ""
    return render_template("index.html", chat_message=message, chat_reply=reply)


@app.route("/email/summary", methods=["POST"])
def email_summary():
    try:
        count = int(request.form.get("count", "5"))
    except ValueError:
        count = 0
    result = fetch_email_summary(count)
    return render_template("index.html", email_summary_result=result)


@app.route("/email/auto-reply", methods=["POST"])
def email_auto_reply():
    result = auto_reply_to_unread()
    return render_template("index.html", email_auto_reply_result=result)


@app.route("/email/send", methods=["POST"])
def email_send():
    subject = request.form.get("subject", "")
    body = request.form.get("body", "")
    to_email = request.form.get("to_email", "")
    ok = send_email(subject, body, to_email)
    result = "✅ Email sent." if ok else "❌ Failed to send email. Check server logs."
    return render_template("index.html", email_send_result=result)


@app.route("/whatsapp/send", methods=["POST"])
def whatsapp_send():
    message = request.form.get("message", "")
    to_number = request.form.get("to_number", "")
    ok = send_whatsapp_message(message, to_number)
    result = "✅ WhatsApp message sent." if ok else "❌ Failed to send WhatsApp message. Check server logs."
    return render_template("index.html", whatsapp_send_result=result)


@app.route("/whatsapp/webhook", methods=["POST"])
def whatsapp_webhook():
    """Twilio calls this when a WhatsApp message arrives; we auto-reply via the LLM."""
    incoming_body = request.form.get("Body", "")
    reply_text = generate_whatsapp_reply(incoming_body) if incoming_body.strip() else "Sorry, I didn't get that."

    twiml = MessagingResponse()
    twiml.message(reply_text)
    return str(twiml), 200, {"Content-Type": "application/xml"}


@app.route("/notion/generate", methods=["POST"])
def notion_generate():
    topic = request.form.get("topic", "")
    page_id = request.form.get("page_id", "").strip()

    content = generate_document_content(topic)
    saved_result = ""
    if page_id:
        ok = save_to_notion(topic, content, page_id)
        saved_result = "✅ Saved to Notion." if ok else "❌ Failed to save to Notion."

    return render_template("index.html", notion_result=content, notion_saved_result=saved_result)


if __name__ == "__main__":
    app.run(debug=True)
