"""
generator.py
Backend module for AI-Powered Blog Content Generator using Ollama.
Course: 24CS2506 - Building Applications using GPT-4
Experiment 2: AI-Powered Blog Content Generator using Ollama
"""

import ollama
from typing import Generator, List, Dict, Any, Optional

DEFAULT_MODEL = "llama3.2"

class BlogGenerator:
    """
    Blog Generator class interfacing with local Ollama instance.
    Implements prompt engineering components and LLM generation capabilities:
    - Blog Generation
    - Text Summarization
    - Article Rewriting
    - Question Answering
    """

    def __init__(self, model_name: str = DEFAULT_MODEL, host: str = "http://localhost:11434"):
        self.model_name = model_name
        self.host = host
        self.client = ollama.Client(host=self.host)

    def get_available_models(self) -> List[str]:
        """
        Retrieves list of locally installed models in Ollama.
        """
        try:
            response = self.client.list()
            models = []
            if hasattr(response, "models"):
                for m in response.models:
                    name = getattr(m, "model", None) or getattr(m, "name", "")
                    if name:
                        models.append(name)
            elif isinstance(response, dict) and "models" in response:
                for m in response["models"]:
                    name = m.get("model") or m.get("name")
                    if name:
                        models.append(name)
            return models
        except Exception as e:
            return []

    def set_model(self, model_name: str) -> None:
        """
        Sets the active Ollama model name.
        """
        self.model_name = model_name

    def build_prompt(
        self,
        topic: str,
        writing_style: str = "Professional",
        tone: str = "Friendly",
        word_count: int = 500,
        audience: str = "Engineering Students",
        use_simple_english: bool = True,
        include_sections: bool = True,
        additional_instructions: Optional[str] = None
    ) -> str:
        """
        Constructs a structured prompt based on Section 6 of the lab document:
        - Topic
        - Writing Style
        - Tone
        - Word Count
        - Audience
        - Structure (Introduction, Main Content, Conclusion)
        - Language constraint (Simple English)
        """
        prompt_parts = [
            f"Write a {word_count}-word {writing_style.lower()} blog on {topic} for {audience.lower()}."
        ]

        if tone:
            prompt_parts.append(f"Maintain a {tone.lower()} tone throughout the blog.")

        if use_simple_english:
            prompt_parts.append("Use simple English.")

        if include_sections:
            prompt_parts.append("Include Introduction, Main Content and Conclusion.")

        if additional_instructions and additional_instructions.strip():
            prompt_parts.append(additional_instructions.strip())

        prompt_parts.append("Do not include any emojis in the content.")

        return " ".join(prompt_parts)

    def generate_blog(
        self,
        prompt: str,
        temperature: float = 0.7,
        stream: bool = False
    ) -> Any:
        """
        Generates blog content using Ollama with the engineered prompt.
        Supports both streaming and non-streaming generation.
        """
        system_instruction = (
            "You are an expert AI blog writer. Write clear, well-structured, informative, "
            "and engaging blog content strictly following the given prompt parameters. "
            "Do not use any emojis in your response."
        )

        messages = [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": prompt}
        ]

        options = {
            "temperature": temperature
        }

        if stream:
            def stream_generator() -> Generator[str, None, None]:
                response = self.client.chat(
                    model=self.model_name,
                    messages=messages,
                    options=options,
                    stream=True
                )
                for chunk in response:
                    content = ""
                    if hasattr(chunk, "message") and hasattr(chunk.message, "content"):
                        content = chunk.message.content
                    elif isinstance(chunk, dict) and "message" in chunk:
                        content = chunk["message"].get("content", "")
                    if content:
                        yield content
            return stream_generator()
        else:
            response = self.client.chat(
                model=self.model_name,
                messages=messages,
                options=options,
                stream=False
            )
            if hasattr(response, "message") and hasattr(response.message, "content"):
                return response.message.content
            elif isinstance(response, dict) and "message" in response:
                return response["message"].get("content", "")
            return str(response)

    def summarize_text(
        self,
        text: str,
        target_word_count: int = 150,
        stream: bool = False
    ) -> Any:
        """
        Summarizes given text into a concise summary (Section 4 capability).
        """
        prompt = (
            f"Summarize the following text within approximately {target_word_count} words. "
            "Keep the key insights and factual points clear. Do not include emojis:\n\n"
            f"{text}"
        )
        return self.generate_blog(prompt=prompt, stream=stream)

    def rewrite_article(
        self,
        text: str,
        target_style: str = "Professional",
        target_tone: str = "Informative",
        stream: bool = False
    ) -> Any:
        """
        Rewrites an article with specified style and tone (Section 4 capability).
        """
        prompt = (
            f"Rewrite the following article using a {target_style.lower()} style and a {target_tone.lower()} tone. "
            "Ensure the flow is natural and points are well articulated. Do not include emojis:\n\n"
            f"{text}"
        )
        return self.generate_blog(prompt=prompt, stream=stream)
