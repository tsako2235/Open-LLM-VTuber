import re


def clean_ai_memory_content(content: str) -> str:
    """
    Clean the AI memory content by removing <think> and <judgment> tags and their content.

    Args:
        content (str): The original content from the LLM.

    Returns:
        str: The cleaned content with specific tags removed.
    """
    # Pattern to match <think>...</think> and <judgment>...</judgment> blocks
    # re.DOTALL is used to match across multiple lines
    pattern = r"<(think|judgment)>.*?</\1>"
    cleaned_content = re.sub(pattern, "", content, flags=re.DOTALL)
    
    # helper for cleanup double newlines that might be left over
    # but strictly speaking, we just want to remove the tags content.
    # The requirement is to remove tags and their content.
    # We might want to strip leading/trailing whitespace if the entire message was just the tag.
    
    return cleaned_content.strip()
