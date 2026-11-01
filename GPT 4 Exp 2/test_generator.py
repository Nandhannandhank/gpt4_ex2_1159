"""
test_generator.py
Unit tests for BlogGenerator and prompt engineering logic.
"""

import unittest
from generator import BlogGenerator

class TestBlogGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = BlogGenerator(model_name="llama3.2")

    def test_build_prompt_components(self):
        """
        Test prompt engineering construction based on Section 6 of lab manual.
        """
        prompt = self.generator.build_prompt(
            topic="Artificial Intelligence",
            writing_style="Professional",
            tone="Friendly",
            word_count=500,
            audience="Engineering Students",
            use_simple_english=True,
            include_sections=True
        )

        self.assertIn("500-word", prompt)
        self.assertIn("professional", prompt)
        self.assertIn("Artificial Intelligence", prompt)
        self.assertIn("engineering students", prompt)
        self.assertIn("friendly tone", prompt)
        self.assertIn("Use simple English.", prompt)
        self.assertIn("Include Introduction, Main Content and Conclusion.", prompt)
        self.assertIn("Do not include any emojis", prompt)

    def test_build_prompt_custom_topic(self):
        prompt = self.generator.build_prompt(
            topic="Cyber Security",
            writing_style="Technical",
            tone="Formal",
            word_count=300,
            audience="Beginners",
            use_simple_english=True,
            include_sections=False
        )

        self.assertIn("300-word", prompt)
        self.assertIn("technical", prompt)
        self.assertIn("Cyber Security", prompt)
        self.assertIn("beginners", prompt)
        self.assertIn("formal tone", prompt)

    def test_model_listing(self):
        models = self.generator.get_available_models()
        self.assertIsInstance(models, list)

if __name__ == "__main__":
    unittest.main()
