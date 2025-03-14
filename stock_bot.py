import os
import streamlit as st
import openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set your OpenAI API key from the .env file
openai.api_key = os.getenv("OPENAI_API_KEY")

st.title("Earnings Analysis & Post-Earnings Stock Price Predictor")

st.markdown("""
This app lets you:
- Either upload or fetch (via web search) the press release and earnings call presentation files from a company's investor relations website.
- Either manually enter or fetch from the web the street estimates (expected EPS and Revenue) and the stock price at close on earnings day.
- Receive **two separate tables** comparing the company’s reported earnings with Street expectations and the quarterly financials.
- Get a prediction for the appropriate post-earnings stock price based on guidance in the slides.
""")

# =======================
# Sidebar: Document Options
# =======================
st.sidebar.header("Document Options")
fetch_pr_from_web = st.sidebar.checkbox("Fetch Press Release from Web", value=True)
fetch_ec_from_web = st.sidebar.checkbox("Fetch Earnings Call Presentation from Web", value=True)
company_name = st.sidebar.text_input("Company Name for Web Search", "NVIDIA")

# If not fetching from the web, allow file uploads.
if not fetch_pr_from_web:
    press_release_file = st.sidebar.file_uploader("Upload Press Release (PDF/TXT)", type=["pdf", "txt"])
else:
    press_release_file = None

if not fetch_ec_from_web:
    presentation_file = st.sidebar.file_uploader("Upload Earnings Call Presentation (PDF/TXT)", type=["pdf", "txt"])
else:
    presentation_file = None

# =======================
# Sidebar: Market Data Options
# =======================
st.sidebar.header("Market Data Options")
use_web_search = st.sidebar.checkbox("Fetch Street Estimates & Stock Price from Web", value=True)

if use_web_search:
    def fetch_market_data(company):
        """
        Uses the new OpenAI agent tool for web search to fetch market data.
        (Placeholder implementation. Replace with the actual API call per OpenAI's new tools.)
        """
        try:
            result = openai.Agent.run_tool("web_search", query=f"Latest street estimates and stock price at close on earnings day for {company} earnings")
            # Assume the result returns a dict with keys: 'expected_eps', 'expected_rev', 'close_price'
            expected_eps = result.get("expected_eps", "0.85")
            expected_rev = result.get("expected_rev", "38.14")
            close_price = result.get("close_price", "131.28")
            return expected_eps, expected_rev, close_price
        except Exception as e:
            return "0.85", "38.14", "131.28"
    
    with st.spinner("Fetching market data from the web..."):
        fetched_expected_eps, fetched_expected_rev, fetched_close_price = fetch_market_data(company_name)
    st.sidebar.markdown("**Fetched Market Data:**")
    st.sidebar.write(f"Expected EPS: {fetched_expected_eps}")
    st.sidebar.write(f"Expected Revenue (B USD): {fetched_expected_rev}")
    st.sidebar.write(f"Stock Price at Close: ${fetched_close_price}")
else:
    fetched_expected_eps = st.sidebar.text_input("Expected EPS", "0.85")
    fetched_expected_rev = st.sidebar.text_input("Expected Revenue (in Billion USD)", "38.14")
    fetched_close_price = st.sidebar.text_input("Stock Price at Close on Earnings Day (USD)", "131.28")

# =======================
# Functions to Fetch Documents via Web Search
# =======================
def fetch_press_release(company):
    """
    Uses the new agent tool for web search to fetch the latest press release text from the company's investor relations website.
    (Placeholder implementation—replace with actual API calls per OpenAI's new tools.)
    """
    try:
        result = openai.Agent.run_tool("web_search", query=f"Latest press release from {company} investor relations website")
        return result.get("text", "No press release text found.")
    except Exception as e:
        return f"Error fetching press release: {str(e)}"

def fetch_earnings_call(company):
    """
    Uses the new agent tool for web search to fetch the latest earnings call presentation text from the company's investor relations website.
    (Placeholder implementation—replace with actual API calls per OpenAI's new tools.)
    """
    try:
        result = openai.Agent.run_tool("web_search", query=f"Latest earnings call presentation slides from {company} investor relations website")
        return result.get("text", "No earnings call presentation text found.")
    except Exception as e:
        return f"Error fetching earnings call presentation: {str(e)}"

# =======================
# Utility: PDF Extraction using New Agent Tool
# =======================
def extract_pdf_text(uploaded_file):
    """
    Uses the new OpenAI agent tool to extract text from a PDF.
    (Placeholder implementation. Replace with the actual API call as documented in OpenAI's new tools.)
    """
    try:
        result = openai.Agent.run_tool("pdf_extractor", file=uploaded_file)
        extracted_text = result.get("extracted_text", "")
        if not extracted_text:
            return "No text could be extracted from this PDF."
        return extracted_text
    except Exception as e:
        return f"Error extracting PDF: {str(e)}"

# =======================
# Utility: Read File Content
# =======================
def read_file(uploaded_file):
    if uploaded_file is not None:
        if uploaded_file.type == "text/plain":
            return uploaded_file.getvalue().decode("utf-8")
        elif "pdf" in uploaded_file.type:
            return extract_pdf_text(uploaded_file)
    return ""

# =======================
# Obtain Document Texts
# =======================
if fetch_pr_from_web:
    press_release_text = fetch_press_release(company_name)
else:
    press_release_text = read_file(press_release_file)

if fetch_ec_from_web:
    presentation_text = fetch_earnings_call(company_name)
else:
    presentation_text = read_file(presentation_file)

# =======================
# Main Analysis
# =======================
st.header("Run Analysis")
if st.button("Generate Earnings Analysis"):
    with st.spinner("Processing your input..."):
        prompt = f"""
You are an expert financial analyst. Using the following inputs, please produce:

1. **Two separate tables** in Markdown:
   - **Table 1: Earnings Calls** which compares:
      - Reported EPS vs. Expected EPS,
      - Reported Revenue vs. Expected Revenue,
      - and calculates the Surprise percentage.
   - **Table 2: Quarterly Financials** showing the quarterly financial metrics such as revenue, net income, diluted EPS, operating income, etc., with Year-over-Year (Y/Y) changes.

2. A brief explanation or summary below the tables.

3. A prediction for the appropriate post-earnings stock price based on guidance in the slides.
   - **Important**: Use **only LaTeX math with dollar signs** for any formulas. For example:
     
     $\\text{{Price Prediction}} = 131.28 \\times (1 + 0.04) = 136.53$
     
   - Do **not** use square brackets for LaTeX. Only use inline `$...$` or display `$$...$$` syntax.

-- Press Release --
{press_release_text}

-- Earnings Call Presentation --
{presentation_text}

-- Street Estimates --
Expected EPS: {fetched_expected_eps}
Expected Revenue: {fetched_expected_rev} Billion USD

-- Market Data --
Stock Price at Close on Earnings Day: ${fetched_close_price}

In your final answer, please:
- Format the two tables exactly as **Earnings Calls** and **Financials**.
- Include columns for Expected vs. Reported vs. Surprise in the first table.
- In the second table, show each financial metric with Y/Y changes.
- Then provide the post-earnings price prediction in a short paragraph or bullet, using **only** the dollar-sign LaTeX notation for any formulas.
"""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=2500,
            )
            answer = response.choices[0].message.content
            st.markdown("### Analysis Output")
            st.markdown(answer)
        except Exception as e:
            st.error(f"Error generating answer: {e}")
