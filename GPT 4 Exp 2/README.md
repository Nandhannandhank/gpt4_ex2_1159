# 24CS2506 - Building Applications using GPT-4
## Experiment 2: AI-Powered Blog Content Generator using Ollama

An end-to-end AI-powered blog content generation application built using Python, Streamlit, and local LLMs via Ollama (Meta Llama 3.2).

---

## 1. Overview and Core Concepts

### What is a Blog?
A blog is an article written to share information, opinions, tutorials, or news on a specific topic. Common topics include:
- Artificial Intelligence
- Climate Change
- Cyber Security
- Electric Vehicles
- Healthy Living
- Digital Marketing

### What is AI Content Generation?
AI Content Generation is the process of automatically creating human-like text using Artificial Intelligence. Instead of writing manually, users provide a structured prompt, and the AI generates tailored content.

### What is Ollama?
Ollama is open-source software that allows users to run Large Language Models (LLMs) locally on their own machines without relying on cloud APIs.
**Key Advantages:**
- Free to use
- Runs offline
- Faster response
- No API cost
- Data remains private and secure on your local computer

### What is Llama 3.2?
Llama 3.2 is an advanced lightweight Large Language Model developed by Meta. Its capabilities include:
- Answering questions
- Generating blog posts
- Summarizing long text
- Translating languages
- Writing code
- Rewriting and refining articles

---

## 2. Prompt Engineering Framework

As highlighted in Experiment 2, prompt engineering is the key to obtaining high-quality outputs: *The better the prompt, the better the output.*

### Components of a Good Prompt
A structured prompt consists of:
1. **Topic:** The subject matter (e.g., Artificial Intelligence, Climate Change).
2. **Writing Style:** The writing approach (e.g., Professional, Casual, Technical, Academic).
3. **Tone:** The emotional attitude (e.g., Friendly, Formal, Informative, Persuasive).
4. **Word Count:** The target length (e.g., 300 words, 500 words).
5. **Audience:** The intended reader (e.g., Engineering Students, Beginners, Professionals).
6. **Structure & Language:** Clear guidelines such as simple English and sections (Introduction, Main Content, Conclusion).

**Example Prompt:**
> "Write a 500-word professional blog on Artificial Intelligence for engineering students. Maintain a friendly tone throughout the blog. Use simple English. Include Introduction, Main Content and Conclusion."

---

## 3. Project Structure

```text
GPT 4 Exp 2/
├── app.py              # Streamlit Web Application Interface
├── generator.py        # Core BlogGenerator class & Ollama integration
├── requirements.txt    # Python dependencies
├── test_generator.py   # Unit tests for prompt engineering and generator
└── README.md           # Experiment documentation
```

---

## 4. Setup and Installation

### Prerequisites
- Python 3.9+
- Ollama installed and running locally (`http://localhost:11434`)
- Llama 3.2 model pulled in Ollama:
  ```bash
  ollama pull llama3.2
  ```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run the Application
```bash
streamlit run app.py
```

### Run Unit Tests
```bash
python3 -m unittest test_generator.py
```
