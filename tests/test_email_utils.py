import email
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from unittest.mock import MagicMock, patch

import email_utils


def _make_message(subject, body, multipart=False):
    if multipart:
        msg = MIMEMultipart()
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))
    else:
        msg = MIMEText(body)
        msg["Subject"] = subject
    return email.message_from_bytes(msg.as_bytes())


def test_decode_email_subject_plain():
    msg = _make_message("Hello World", "body")
    assert email_utils.decode_email_subject(msg) == "Hello World"


def test_get_email_body_simple():
    msg = _make_message("Subj", "Hello there")
    assert email_utils.get_email_body(msg).strip() == "Hello there"


def test_get_email_body_multipart():
    msg = _make_message("Subj", "Multipart body", multipart=True)
    assert "Multipart body" in email_utils.get_email_body(msg)


def test_send_email_success():
    with patch("email_utils.smtplib.SMTP_SSL") as mock_smtp_ssl:
        server = MagicMock()
        mock_smtp_ssl.return_value.__enter__.return_value = server
        result = email_utils.send_email("Subject", "Body", "to@example.com")

    assert result is True
    server.login.assert_called_once()
    server.sendmail.assert_called_once()


def test_send_email_failure_returns_false():
    with patch("email_utils.smtplib.SMTP_SSL", side_effect=Exception("boom")):
        result = email_utils.send_email("Subject", "Body", "to@example.com")

    assert result is False


def test_setup_langsmith_tracing_noop_without_key(monkeypatch):
    # Regression test: os.environ[...] = os.getenv(...) used to raise
    # TypeError when LANGCHAIN_API_KEY wasn't set, because os.environ
    # rejects None values.
    monkeypatch.delenv("LANGCHAIN_API_KEY", raising=False)
    email_utils.setup_langsmith_tracing()  # should not raise


def test_setup_langsmith_tracing_sets_env_when_key_present(monkeypatch):
    monkeypatch.setenv("LANGCHAIN_API_KEY", "dummy-langsmith-key")
    monkeypatch.delenv("LANGCHAIN_PROJECT", raising=False)

    email_utils.setup_langsmith_tracing(default_project="test-project")

    assert os.environ["LANGCHAIN_PROJECT"] == "test-project"
    assert os.environ["LANGCHAIN_ENDPOINT"] == "https://api.smith.langchain.com"
