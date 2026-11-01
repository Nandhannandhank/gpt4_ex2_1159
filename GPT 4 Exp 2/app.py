"""
app.py
Enhanced Web GUI for AI-Powered Blog Content Generator using Ollama
Course: 24CS2506 - Building Applications using GPT-4
Experiment 2: AI-Powered Blog Content Generator using Ollama
"""

import sys
import streamlit as st
from generator import BlogGenerator, DEFAULT_MODEL

st.set_page_config(
    page_title="AI-Powered Blog Content Generator",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling (Strictly zero emojis, modern professional aesthetics)
st.markdown("""
<style>
    /* Main Layout and Typography */
    .main-title-container {
        padding: 1.5rem 0 0.5rem 0;
        border-bottom: 2px solid #e2e8f0;
        margin-bottom: 1.5rem;
    }
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1e293b;
        letter-spacing: -0.025em;
        margin-bottom: 0.25rem;
    }
    .main-subtitle {
        font-size: 0.95rem;
        color: #64748b;
        font-weight: 500;
    }
    
    /* Status Badge */
    .status-badge-online {
        display: inline-flex;
        align-items: center;
        background-color: #ecfdf5;
        color: #065f46;
        border: 1px solid #a7f3d0;
        padding: 4px 10px;
        border-radius: 9999px;
        font-size: 0.78rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    .status-dot {
        width: 8px;
        height: 8px;
        background-color: #10b981;
        border-radius: 50%;
        margin-right: 6px;
        display: inline-block;
    }
    
    /* Component Pill Badges */
    .pill-badge {
        display: inline-block;
        background-color: #eff6ff;
        color: #1e40af;
        border: 1px solid #bfdbfe;
        padding: 3px 9px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-right: 4px;
        margin-bottom: 4px;
    }

    /* Cards and Containers */
    .metric-card {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 12px 16px;
        text-align: center;
    }
    .metric-value {
        font-size: 1.4rem;
        font-weight: 700;
        color: #0f172a;
    }
    .metric-label {
        font-size: 0.75rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-top: 2px;
    }
    
    /* Output article container */
    .article-container {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 24px;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05);
        margin-top: 1rem;
        margin-bottom: 1rem;
    }

    /* Guide Callout */
    .guide-box {
        background-color: #f0fdf4;
        border-left: 4px solid #22c55e;
        padding: 14px 18px;
        border-radius: 0 8px 8px 0;
        margin: 12px 0;
        color: #166534;
        font-size: 0.9rem;
    }

    /* Architecture Box */
    .architecture-box {
        background-color: #f8fafc;
        border: 1px dashed #94a3b8;
        border-radius: 8px;
        padding: 16px;
        font-family: monospace;
        font-size: 0.85rem;
        line-height: 1.5;
        color: #334155;
    }
</style>
""", unsafe_allow_html=True)

# Initialize BlogGenerator instance
@st.cache_resource
def get_generator():
    return BlogGenerator()

generator = get_generator()

# Application Header
st.markdown("""
<div class="main-title-container">
    <div class="main-title">AI-Powered Blog Content Generator</div>
    <div class="main-subtitle">24CS2506 - Building Applications using GPT-4 | Experiment 2: Ollama Local LLM & Prompt Engineering</div>
</div>
""", unsafe_allow_html=True)

# Sidebar Configuration
with st.sidebar:
    st.markdown("### System & Model Status")
    
    # Check Ollama connection and models
    raw_models = generator.get_available_models()
    chat_models = [m for m in raw_models if "embed" not in m.lower()]
    
    if chat_models:
        st.markdown("""
        <div class="status-badge-online">
            <span class="status-dot"></span> Ollama Server: Connected (Localhost)
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("Ollama connection not detected or no models found. Using fallback.")
        chat_models = ["llama3.2:latest", "qwen2.5:3b"]
    
    # Default model preference for Llama 3.2
    default_index = 0
    for idx, m in enumerate(chat_models):
        if "llama3.2" in m:
            default_index = idx
            break
    
    selected_model = st.selectbox(
        "Active Ollama Model:",
        options=chat_models,
        index=default_index,
        help="Llama 3.2 is the official local model specified in the experiment manual."
    )
    generator.set_model(selected_model)
    
    st.markdown("---")
    st.markdown("### Generation Hyperparameters")
    temperature = st.slider(
        "Temperature (Creativity):",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.05,
        help="Lower values yield more focused and deterministic text; higher values increase variety and creativity."
    )
    
    st.markdown("---")
    st.markdown("### Quick Setup Reference")
    st.markdown("""
    **Core Technologies:**
    - Local LLM Runner: Ollama
    - Default Model: Meta Llama 3.2 (3.2B)
    - Technique: Modular Prompt Engineering
    
    **Ollama Advantages (PDF Section 3):**
    - Free to use
    - Runs completely offline
    - Faster local response
    - Zero API fees or rate limits
    - Data privacy (remains on machine)
    """)
    
    st.markdown("---")
    st.caption("Course: 24CS2506 | Lab Exp 2 | Student: URK23CS1140")

# Main Navigation Tabs
tab_generator, tab_tools, tab_presets, tab_theory = st.tabs([
    "Blog Generator",
    "Rewrite & Summarize",
    "Quick Presets",
    "Lab Manual & Theory"
])

# ----------------------------------------------------
# TAB 1: Blog Generator
# ----------------------------------------------------
with tab_generator:
    with st.container():
        st.markdown("#### Step 1: Configure Prompt Engineering Parameters")
        st.caption("Adheres directly to Section 6: Components of a Good Prompt (Topic, Writing Style, Tone, Word Count, Audience, Structure).")

        col_left, col_mid, col_right = st.columns(3)

        with col_left:
            pdf_topics = [
                "Artificial Intelligence",
                "Climate Change",
                "Cyber Security",
                "Electric Vehicles",
                "Healthy Living",
                "Digital Marketing",
                "Custom Topic"
            ]
            selected_topic_choice = st.selectbox(
                "Topic (PDF Section 1):",
                options=pdf_topics,
                index=0,
                key="input_topic_choice"
            )
            if selected_topic_choice == "Custom Topic":
                active_topic = st.text_input("Enter Custom Topic:", value="Quantum Computing", key="input_custom_topic")
            else:
                active_topic = selected_topic_choice

            audience_options = [
                "Engineering Students",
                "Beginners",
                "Technology Professionals",
                "College Students",
                "General Public"
            ]
            active_audience = st.selectbox(
                "Target Audience (PDF Section 6):",
                options=audience_options,
                index=0,
                key="input_audience"
            )

        with col_mid:
            style_options = [
                "Professional",
                "Casual",
                "Academic",
                "Creative",
                "Technical"
            ]
            active_style = st.selectbox(
                "Writing Style (PDF Section 6):",
                options=style_options,
                index=0,
                key="input_style"
            )

            tone_options = [
                "Friendly",
                "Formal",
                "Informative",
                "Persuasive",
                "Inspirational"
            ]
            active_tone = st.selectbox(
                "Tone (PDF Section 6):",
                options=tone_options,
                index=0,
                key="input_tone"
            )

        with col_right:
            word_count_options = [300, 500, 750, 1000]
            active_word_count = st.selectbox(
                "Word Count (PDF Section 5 & 6):",
                options=word_count_options,
                index=1,
                key="input_word_count"
            )

            active_simple_english = st.checkbox("Use simple English (PDF Section 6)", value=True, key="chk_simple")
            active_sections = st.checkbox("Include Introduction, Main Content, Conclusion", value=True, key="chk_sections")

        custom_guidance = st.text_input(
            "Optional Specific Points or Themes:",
            value="",
            placeholder="e.g. Emphasize ethical considerations and industry adoption",
            key="input_notes"
        )

    # Component Badges Overview
    st.markdown("#### Step 2: Prompt Inspection & Visual Verification")
    
    badge_html = f"""
    <div>
        <span class="pill-badge">Topic: {active_topic}</span>
        <span class="pill-badge">Style: {active_style}</span>
        <span class="pill-badge">Tone: {active_tone}</span>
        <span class="pill-badge">Target: {active_word_count} words</span>
        <span class="pill-badge">Audience: {active_audience}</span>
        <span class="pill-badge">{"Simple English" if active_simple_english else "Standard English"}</span>
        <span class="pill-badge">{"Structured Sections" if active_sections else "Freeform"}</span>
    </div>
    """
    st.markdown(badge_html, unsafe_allow_html=True)

    # Build Prompt
    formulated_prompt = generator.build_prompt(
        topic=active_topic,
        writing_style=active_style,
        tone=active_tone,
        word_count=active_word_count,
        audience=active_audience,
        use_simple_english=active_simple_english,
        include_sections=active_sections,
        additional_instructions=custom_guidance
    )

    editable_prompt = st.text_area(
        "Engineered Prompt (Directly Dispatched to Local Ollama):",
        value=formulated_prompt,
        height=95,
        help="This is the exact prompt engineered based on the PDF rules. You may adjust wording here before execution."
    )

    btn_generate = st.button("Generate Blog Article", type="primary", use_container_width=True)

    if btn_generate:
        if not editable_prompt.strip():
            st.error("Prompt cannot be empty.")
        else:
            st.markdown("---")
            st.markdown(f"### Generated Blog: {active_topic}")

            content_area = st.empty()
            accumulated_text = ""

            with st.spinner(f"Generating content locally via {selected_model}..."):
                try:
                    stream_obj = generator.generate_blog(
                        prompt=editable_prompt,
                        temperature=temperature,
                        stream=True
                    )
                    for token in stream_obj:
                        accumulated_text += token
                        content_area.markdown(accumulated_text + " ")
                    content_area.markdown(accumulated_text)
                except Exception as exc:
                    st.error(f"Generation error: {str(exc)}")

            if accumulated_text:
                word_total = len(accumulated_text.split())
                read_time_mins = max(1, round(word_total / 200, 1))

                st.success("Generation completed successfully.")

                # Interactive Metrics
                m_col1, m_col2, m_col3, m_col4 = st.columns(4)
                with m_col1:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-value">{active_word_count}</div>
                        <div class="metric-label">Target Words</div>
                    </div>
                    """, unsafe_allow_html=True)
                with m_col2:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-value">{word_total}</div>
                        <div class="metric-label">Actual Words</div>
                    </div>
                    """, unsafe_allow_html=True)
                with m_col3:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-value">~{read_time_mins} min</div>
                        <div class="metric-label">Est. Read Time</div>
                    </div>
                    """, unsafe_allow_html=True)
                with m_col4:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-value">{selected_model.split(':')[0]}</div>
                        <div class="metric-label">Ollama Engine</div>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)

                # Export Bar
                exp_col1, exp_col2 = st.columns(2)
                with exp_col1:
                    st.download_button(
                        label="Download Article as Markdown (.md)",
                        data=accumulated_text,
                        file_name=f"{active_topic.replace(' ', '_').lower()}_blog.md",
                        mime="text/markdown",
                        use_container_width=True
                    )
                with exp_col2:
                    st.download_button(
                        label="Download Article as Plain Text (.txt)",
                        data=accumulated_text,
                        file_name=f"{active_topic.replace(' ', '_').lower()}_blog.txt",
                        mime="text/plain",
                        use_container_width=True
                    )

# ----------------------------------------------------
# TAB 2: Secondary Tools (Rewrite & Summarize - Section 4)
# ----------------------------------------------------
with tab_tools:
    st.markdown("#### Section 4 Capabilities: Text Summarizer & Article Rewriter")
    st.write(
        "Meta's Llama 3.2 is capable of answering questions, generating blogs, summarizing text, "
        "and rewriting articles. Test these built-in secondary capabilities below."
    )

    tool_mode = st.radio("Select Utility:", ["Summarize Text", "Rewrite Article"], horizontal=True)

    # Sample texts for quick testing
    sample_text_ai = (
        "Artificial Intelligence is the simulation of human intelligence processes by computer systems. "
        "These processes include the acquisition of information and rules for using it, reasoning to reach "
        "approximate or definite conclusions, and self-correction. Particular applications of AI include "
        "expert systems, speech recognition, machine vision, and natural language understanding. "
        "Modern engineering disciplines increasingly rely on AI models to automate quality inspections, "
        "optimize component lifespans, and manage smart grids dynamically."
    )

    if tool_mode == "Summarize Text":
        st.markdown("##### Text Summarizer")
        
        col_s_btn1, col_s_btn2 = st.columns([1, 4])
        with col_s_btn1:
            if st.button("Load Sample Text", key="btn_load_sum"):
                st.session_state["sum_input_val"] = sample_text_ai
        
        sum_input = st.text_area(
            "Input Text to Summarize:",
            value=st.session_state.get("sum_input_val", ""),
            height=160,
            placeholder="Paste text, article excerpt, or research snippet here..."
        )

        sum_word_slider = st.slider("Target Summary Length (Words):", 30, 200, 60, step=10)

        if st.button("Generate Summary", type="primary"):
            if not sum_input.strip():
                st.warning("Please provide input text to summarize.")
            else:
                with st.spinner("Generating summary using Ollama..."):
                    summary_out = generator.summarize_text(
                        text=sum_input,
                        target_word_count=sum_word_slider,
                        stream=False
                    )
                    st.markdown("##### Summary Result:")
                    st.info(summary_out)
                    st.caption(f"Word count: {len(summary_out.split())} words")

    else:
        st.markdown("##### Article Rewriter")
        
        col_r_btn1, col_r_btn2 = st.columns([1, 4])
        with col_r_btn1:
            if st.button("Load Sample Text", key="btn_load_rew"):
                st.session_state["rew_input_val"] = sample_text_ai

        rew_input = st.text_area(
            "Input Text to Rewrite:",
            value=st.session_state.get("rew_input_val", ""),
            height=160,
            placeholder="Paste draft or raw content here to reshape style and tone..."
        )

        col_rw_s, col_rw_t = st.columns(2)
        with col_rw_s:
            rewrite_target_style = st.selectbox(
                "Target Style:",
                ["Professional", "Casual", "Academic", "Creative", "Concise"]
            )
        with col_rw_t:
            rewrite_target_tone = st.selectbox(
                "Target Tone:",
                ["Friendly", "Formal", "Persuasive", "Informative", "Inspirational"]
            )

        if st.button("Rewrite Article", type="primary"):
            if not rew_input.strip():
                st.warning("Please provide input text to rewrite.")
            else:
                with st.spinner("Rewriting content using Ollama..."):
                    rewrite_out = generator.rewrite_article(
                        text=rew_input,
                        target_style=rewrite_target_style,
                        target_tone=rewrite_target_tone,
                        stream=False
                    )
                    st.markdown("##### Rewritten Result:")
                    st.info(rewrite_out)
                    st.caption(f"Word count: {len(rewrite_out.split())} words")

# ----------------------------------------------------
# TAB 3: Quick Presets (One-click lab configurations)
# ----------------------------------------------------
with tab_presets:
    st.markdown("#### One-Click Lab Presets")
    st.write("Quickly populate the Blog Generator with canonical scenarios taken directly from the lab manual.")

    col_p1, col_p2 = st.columns(2)

    with col_p1:
        st.markdown("""
        **Preset 1: Section 6 Example Prompt**  
        - Topic: Artificial Intelligence  
        - Style: Professional  
        - Tone: Friendly  
        - Length: 500 words  
        - Audience: Engineering Students  
        - Structure: Introduction, Main Content, Conclusion  
        """)
        if st.button("Apply Section 6 Example Preset", use_container_width=True):
            st.session_state["input_topic_choice"] = "Artificial Intelligence"
            st.session_state["input_style"] = "Professional"
            st.session_state["input_tone"] = "Friendly"
            st.session_state["input_word_count"] = 500
            st.session_state["input_audience"] = "Engineering Students"
            st.session_state["chk_simple"] = True
            st.session_state["chk_sections"] = True
            st.success("Preset applied. Switch to the 'Blog Generator' tab to generate.")

    with col_p2:
        st.markdown("""
        **Preset 2: Section 5 Example Prompt**  
        - Topic: Artificial Intelligence  
        - Style: Professional  
        - Tone: Informative  
        - Length: 300 words  
        - Audience: Beginners  
        - Structure: Simple English  
        """)
        if st.button("Apply Section 5 Example Preset", use_container_width=True):
            st.session_state["input_topic_choice"] = "Artificial Intelligence"
            st.session_state["input_style"] = "Professional"
            st.session_state["input_tone"] = "Informative"
            st.session_state["input_word_count"] = 300
            st.session_state["input_audience"] = "Beginners"
            st.session_state["chk_simple"] = True
            st.session_state["chk_sections"] = False
            st.success("Preset applied. Switch to the 'Blog Generator' tab to generate.")

    st.markdown("---")

    col_p3, col_p4 = st.columns(2)
    with col_p3:
        st.markdown("""
        **Preset 3: Cyber Security Technical Blog**  
        - Topic: Cyber Security  
        - Style: Technical  
        - Tone: Formal  
        - Length: 500 words  
        - Audience: Technology Professionals  
        """)
        if st.button("Apply Cyber Security Preset", use_container_width=True):
            st.session_state["input_topic_choice"] = "Cyber Security"
            st.session_state["input_style"] = "Technical"
            st.session_state["input_tone"] = "Formal"
            st.session_state["input_word_count"] = 500
            st.session_state["input_audience"] = "Technology Professionals"
            st.session_state["chk_simple"] = True
            st.session_state["chk_sections"] = True
            st.success("Preset applied. Switch to the 'Blog Generator' tab to generate.")

    with col_p4:
        st.markdown("""
        **Preset 4: Climate Change Awareness**  
        - Topic: Climate Change  
        - Style: Casual  
        - Tone: Inspirational  
        - Length: 300 words  
        - Audience: General Public  
        """)
        if st.button("Apply Climate Change Preset", use_container_width=True):
            st.session_state["input_topic_choice"] = "Climate Change"
            st.session_state["input_style"] = "Casual"
            st.session_state["input_tone"] = "Inspirational"
            st.session_state["input_word_count"] = 300
            st.session_state["input_audience"] = "General Public"
            st.session_state["chk_simple"] = True
            st.session_state["chk_sections"] = True
            st.success("Preset applied. Switch to the 'Blog Generator' tab to generate.")

# ----------------------------------------------------
# TAB 4: Lab Manual & Theory
# ----------------------------------------------------
with tab_theory:
    st.markdown("#### Experiment 2 Theory and Conceptual Reference")
    st.caption("Content directly transcribed from pages 1 and 2 of the lab PDF.")

    col_t1, col_t2 = st.columns(2)

    with col_t1:
        with st.expander("1. What is a Blog?", expanded=True):
            st.markdown("""
            A blog is an article written to share information, opinions, tutorials, or news on a specific topic.
            
            **Example Topics listed in the PDF:**
            - Artificial Intelligence
            - Climate Change
            - Cyber Security
            - Electric Vehicles
            - Healthy Living
            - Digital Marketing
            """)

        with st.expander("2. What is AI Content Generation?", expanded=True):
            st.markdown("""
            AI Content Generation is the process of automatically creating human-like text using Artificial Intelligence. 
            Instead of writing manually, users provide a prompt, and the AI generates content.
            
            **Example:**
            - **Input:** Write a blog about Artificial Intelligence.
            - **AI Response:** Artificial Intelligence (AI) is transforming industries by enabling machines to perform tasks that normally require human intelligence...
            """)

        with st.expander("3. What is Ollama?", expanded=True):
            st.markdown("""
            Ollama is software that allows users to run Large Language Models (LLMs) locally on their own computer without using cloud APIs.
            
            **Advantages:**
            - Free to use
            - Runs offline
            - Faster response
            - No API cost
            - Data remains on your computer
            """)

    with col_t2:
        with st.expander("4. What is Llama 3.2?", expanded=True):
            st.markdown("""
            Llama 3.2 is a Large Language Model developed by Meta.
            
            **Key Capabilities:**
            - Answer questions
            - Generate blogs
            - Summarize text
            - Translate languages
            - Write code
            - Rewrite articles
            """)

        with st.expander("5. Understanding Prompt Engineering", expanded=True):
            st.markdown("""
            A Prompt is the instruction given to the AI.
            
            **Example:**
            > "Write a professional blog on Artificial Intelligence using simple English within 300 words."
            
            *The better the prompt, the better the output.*
            """)

        with st.expander("6. Components of a Good Prompt", expanded=True):
            st.markdown("""
            A good prompt contains:
            - **Topic:** e.g., Artificial Intelligence
            - **Writing Style:** e.g., Professional
            - **Tone:** e.g., Friendly
            - **Word Count:** e.g., 500 words
            - **Audience:** e.g., Engineering Students
            
            **Canonical Example Prompt from PDF:**
            > "Write a 500-word professional blog on Artificial Intelligence for engineering students. Use simple English. Include Introduction, Main Content and Conclusion."
            """)

    st.markdown("---")
    st.markdown("#### System Architecture Flowchart")
    st.markdown("""
    <div class="architecture-box">
    [User Input Configuration] -> [Topic, Style, Tone, Length, Audience]
                  |
                  v
    [Prompt Engineering Engine] -> Formulates structured instruction with simple English constraints
                  |
                  v
    [Local Ollama Runtime]     -> meta/llama3.2 running offline on port 11434
                  |
                  v
    [Streaming Response]       -> Real-time token streaming to Streamlit UI
                  |
                  v
    [Metrics & Export]         -> Target vs. Actual Word Count, .txt/.md downloads
    </div>
    """, unsafe_allow_html=True)

# CLI Fallback Launcher
if __name__ == "__main__" and not (hasattr(st, "runtime") and st.runtime.exists()):
    from streamlit.web import cli as stcli
    sys.argv = ["streamlit", "run", sys.argv[0]]
    sys.exit(stcli.main())
