from unittest.mock import MagicMock, patch

import whatsapp_tool


def test_send_whatsapp_message_success():
    with patch("whatsapp_tool.Client") as mock_client_cls:
        mock_client = MagicMock()
        mock_client.messages.create.return_value = MagicMock(sid="SM123")
        mock_client_cls.return_value = mock_client

        result = whatsapp_tool.send_whatsapp_message("hello", "whatsapp:+10000000000")

    assert result is True
    mock_client.messages.create.assert_called_once()


def test_send_whatsapp_message_failure_returns_false():
    with patch("whatsapp_tool.Client", side_effect=Exception("boom")):
        result = whatsapp_tool.send_whatsapp_message("hello", "whatsapp:+10000000000")

    assert result is False
