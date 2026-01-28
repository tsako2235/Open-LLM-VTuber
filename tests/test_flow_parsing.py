
import pytest
import asyncio
from src.open_llm_vtuber.agent.transformers import (
    sentence_divider,
    display_processor,
    tts_filter,
    actions_extractor,
)
from src.open_llm_vtuber.agent.output_types import SentenceOutput


# Mock Live2D model for actions extractor if needed, but here we focus on parsing
class MockLive2dModel:
    def extract_emotion(self, text):
        return []
    @property
    def emo_str(self):
        return ""

@pytest.mark.asyncio
async def test_flow_parsing_logic():
    # Input stream simulating LLM output
    # "<think>Thinking process...</think><judgment>Judgment process...</judgment>Action!"
    input_tokens = [
        "<", "think", ">", "Thinking", " process", "...", "</", "think", ">",
        "<", "judgment", ">", "Judgment", " process", "...", "</", "judgment", ">",
        "Action", "!"
    ]

    async def mock_llm_stream():
        for token in input_tokens:
            yield token
            await asyncio.sleep(0.001)

    # Mock config
    from src.open_llm_vtuber.config_manager.tts_preprocessor import TTSPreprocessorConfig, TranslatorConfig
    
    mock_config = TTSPreprocessorConfig(
        remove_special_char=False,
        translator_config=TranslatorConfig(
            translate_audio=False,
            translate_provider="deeplx"
        )
    )

    @tts_filter(tts_preprocessor_config=mock_config)
    @display_processor()
    @actions_extractor(live2d_model=MockLive2dModel())
    @sentence_divider(valid_tags=["think", "judgment"])
    async def chat_pipeline():
        async for token in mock_llm_stream():
            yield token

    outputs = []
    async for output in chat_pipeline():
        outputs.append(output)

    print(f"\nCaptured outputs: {outputs}")

    assert len(outputs) >= 3

    # Helper to find output by content
    def find_output_with_text(text_snippet):
        for out in outputs:
            if isinstance(out, SentenceOutput) and text_snippet in out.display_text.text:
                return out
        return None

    # Analyze Think (New Format)
    think_start = find_output_with_text("[Thinking: ")
    assert think_start is not None
    assert think_start.tts_text == "" 
    
    think_content = find_output_with_text("Thinking process...")
    assert think_content is not None
    assert think_content.tts_text == ""

    # Analyze Judgment
    judgment_start = find_output_with_text("[Judgment: ")
    assert judgment_start is not None
    assert judgment_start.tts_text == ""

    # Analyze Action
    action_output = find_output_with_text("Action!")
    assert action_output is not None
    assert "Action!" in action_output.tts_text

if __name__ == "__main__":
    asyncio.run(test_flow_parsing_logic())
