from open_llm_vtuber.utils.cleaner import clean_ai_memory_content

def test_clean_ai_memory_content_think_tag():
    content = "Here is some content. <think>This is internal thought.</think> And this is more content."
    expected = "Here is some content.  And this is more content."
    assert clean_ai_memory_content(content) == expected.strip()

def test_clean_ai_memory_content_judgment_tag():
    content = "<judgment>Decision: Proceed.</judgment>Okay, let's go."
    expected = "Okay, let's go."
    assert clean_ai_memory_content(content) == expected

def test_clean_ai_memory_content_multiline():
    content = """Start.
<think>
Multiline
thought
</think>
End."""
    expected = """Start.

End."""
    assert clean_ai_memory_content(content) == expected.strip()

def test_clean_ai_memory_content_nested_tags_not_supported_but_multiple_tags():
    content = "Text <think>msg1</think> Text <judgment>msg2</judgment>"
    expected = "Text  Text" # double space remains, which is expected regex behavior
    assert clean_ai_memory_content(content) == expected

def test_clean_ai_memory_content_no_tags():
    content = "Just clear text."
    assert clean_ai_memory_content(content) == "Just clear text."

def test_clean_ai_memory_content_only_tags():
    content = "<think>Only thought.</think>"
    assert clean_ai_memory_content(content) == ""
