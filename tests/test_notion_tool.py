from unittest.mock import MagicMock, patch

import notion_tool


def test_generate_document_content():
    mock_llm = MagicMock()
    mock_llm.invoke.return_value = MagicMock(content="Generated doc")

    with patch.object(notion_tool, "llm", mock_llm):
        result = notion_tool.generate_document_content("test topic")

    assert result == "Generated doc"
    mock_llm.invoke.assert_called_once()


def test_save_to_notion_success():
    with patch.object(notion_tool.notion.pages, "create", return_value={}) as mock_create:
        result = notion_tool.save_to_notion("Title", "Content", "page-123")

    assert result is True
    mock_create.assert_called_once()


def test_save_to_notion_failure_returns_false():
    with patch.object(notion_tool.notion.pages, "create", side_effect=Exception("boom")):
        result = notion_tool.save_to_notion("Title", "Content", "page-123")

    assert result is False


def test_summarize_notion_page():
    blocks_response = {
        "results": [
            {
                "type": "paragraph",
                "paragraph": {"rich_text": [{"plain_text": "Hello world"}]},
                "has_children": False,
            }
        ]
    }
    mock_llm = MagicMock()
    mock_llm.invoke.return_value = MagicMock(content="Summary text")

    with patch.object(notion_tool.notion.blocks.children, "list", return_value=blocks_response), \
         patch.object(notion_tool, "llm", mock_llm):
        result = notion_tool.summarize_notion_page("page-123")

    assert result == "Summary text"
    assert "Hello world" in mock_llm.invoke.call_args[0][0][0].content
