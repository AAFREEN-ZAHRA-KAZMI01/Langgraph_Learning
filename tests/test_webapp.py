from unittest.mock import MagicMock, patch

import app as webapp


def client():
    webapp.app.testing = True
    return webapp.app.test_client()


def test_index_page_loads():
    r = client().get("/")
    assert r.status_code == 200
    assert b"AgenticAI Dashboard" in r.data


def test_chat_route():
    with patch.object(webapp, "llm", return_value=MagicMock(content="hi there")):
        r = client().post("/chat", data={"message": "hello"})
    assert r.status_code == 200
    assert b"hi there" in r.data


def test_email_send_route_success():
    with patch.object(webapp, "send_email", return_value=True):
        r = client().post("/email/send", data={"to_email": "x@example.com", "subject": "s", "body": "b"})
    assert r.status_code == 200
    assert b"Email sent" in r.data


def test_email_send_route_failure():
    with patch.object(webapp, "send_email", return_value=False):
        r = client().post("/email/send", data={"to_email": "x@example.com", "subject": "s", "body": "b"})
    assert r.status_code == 200
    assert b"Failed to send email" in r.data


def test_whatsapp_send_route():
    with patch.object(webapp, "send_whatsapp_message", return_value=True):
        r = client().post("/whatsapp/send", data={"to_number": "whatsapp:+10000000000", "message": "hi"})
    assert r.status_code == 200
    assert b"WhatsApp message sent" in r.data


def test_whatsapp_webhook_returns_twiml():
    with patch.object(webapp, "generate_whatsapp_reply", return_value="Hello back"):
        r = client().post("/whatsapp/webhook", data={"Body": "hi", "From": "whatsapp:+10000000000"})
    assert r.status_code == 200
    assert r.content_type == "application/xml"
    assert b"Hello back" in r.data


def test_notion_generate_without_page_id_does_not_save():
    with patch.object(webapp, "generate_document_content", return_value="doc content") as mock_gen, \
         patch.object(webapp, "save_to_notion") as mock_save:
        r = client().post("/notion/generate", data={"topic": "topic", "page_id": ""})

    assert r.status_code == 200
    assert b"doc content" in r.data
    mock_gen.assert_called_once()
    mock_save.assert_not_called()


def test_notion_generate_with_page_id_saves():
    with patch.object(webapp, "generate_document_content", return_value="doc content"), \
         patch.object(webapp, "save_to_notion", return_value=True) as mock_save:
        r = client().post("/notion/generate", data={"topic": "topic", "page_id": "page-123"})

    assert r.status_code == 200
    assert b"Saved to Notion" in r.data
    mock_save.assert_called_once_with("topic", "doc content", "page-123")
