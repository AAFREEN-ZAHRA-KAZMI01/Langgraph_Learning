import fetch_email_tool


def test_fetch_email_summary_rejects_non_positive_count():
    assert fetch_email_tool.fetch_email_summary(0) == "❗ Invalid number entered."
    assert fetch_email_tool.fetch_email_summary(-3) == "❗ Invalid number entered."
