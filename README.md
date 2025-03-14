# AI-Driven Earnings Analyzer

## Overview
This project builds an AI-driven “earnings analyzer” that automates the process of:
1. Retrieving and parsing press releases & earnings call presentations (via manual upload **or** web search).
2. Comparing the reported numbers to Street estimates (EPS and revenue).
3. Generating a post-earnings stock price prediction using advanced Generative AI capabilities.

We leverage **OpenAI’s newly released agent tools (March 2025)** that support PDF uploads, retrieval-augmented generation (RAG), and web search to create a streamlined pipeline from data retrieval to automated analysis.

---

## Features

1. **PDF Parsing**  
   - Utilizes the new `pdf_extractor` agent tool to read earnings call presentations in PDF format.  
   - Optionally fetches the same documents from each company’s investor relations website using web search.  

2. **Web Search for Market Data**  
   - Automatically retrieves Street estimates (expected EPS, expected revenue) and the company’s stock price at close, if the user opts in.  
   - Allows manual entry if the user prefers or if no data is found.  

3. **Retrieval-Augmented Generation (RAG)**  
   - Embeds the PDF or web-fetched text into a vector store (optional) for contextual retrieval.  
   - Feeds relevant chunks to GPT-4o for accurate comparisons of reported vs. expected data.  

4. **Two Markdown Tables**  
   - **Table 1: Earnings Calls** (Expected vs. Reported EPS/Revenue + Surprise%).  
   - **Table 2: Quarterly Financials** (Revenue, Net Income, Diluted EPS, etc., plus Y/Y changes).  

5. **Post-Earnings Price Prediction**  
   - GPT-4o provides a forecast for the stock, referencing newly reported guidance.  
   - Formulas are rendered in LaTeX using inline `$...$` or `$$...$$` syntax.  

---

## Project Structure
```
.
├── .env                  # Contains your OPENAI_API_KEY and any secrets
├── README.md             # This file
├── requirements.txt      # Python dependencies
├── main_app.py           # The main Streamlit app
└── utils/
    ├── data_fetchers.py  # Web search & data fetch logic
    ├── pdf_parser.py     # PDF extraction with new OpenAI agent tools
    └── ...
```

---

## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/YourUsername/ai-earnings-analyzer.git
   cd ai-earnings-analyzer
   ```

2. **Create & Activate a Virtual Environment (Optional)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # macOS/Linux
   # Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure `.env`**
   - Create a file named `.env` at the project root.
   - Add your API key (and other secrets) as:
     ```
     OPENAI_API_KEY=sk-...
     ```
   
5. **Run the Streamlit App**
   ```bash
   streamlit run main_app.py
   ```
   - Open the displayed local URL in your browser.

---

## Usage

1. **Select Data Source**  
   - On the sidebar, choose whether to **fetch** or **upload** the press release & earnings call presentation.  
   - Also select whether to **fetch** or **manually enter** Street estimates & stock price.

2. **Fetch & Parse**  
   - If fetching, the app uses OpenAI’s new agent-based web search to gather the files and data.  
   - If uploading, the app uses the `pdf_extractor` agent tool to parse PDFs.

3. **Generate Comparison & Prediction**  
   - Click **“Generate Earnings Analysis”**.  
   - You’ll see two Markdown tables plus a short explanation in the main area.  
   - The price prediction formula will be rendered in LaTeX.

4. **Refine & Adjust**  
   - If the output seems off, adjust inputs or check the logs to ensure correct data retrieval.  
   - The agentic prompts can be tweaked in `main_app.py` or under `utils/` to refine the final text.

---

## Key Technologies

- **OpenAI GPT-4o**  
  Large language model for generating financial summaries and stock predictions.

- **OpenAI’s New Agent Tools**  
  - **pdf_extractor**: Parse PDFs, e.g. earnings call presentations.  
  - **web_search**: Dynamically retrieve press releases, investor slides, and market data from the web.  
  - **Retrieval-Augmented Generation**: GPT can look up relevant text chunks before composing its final answer.

- **Streamlit**  
  A simple framework for building interactive web apps in Python.

---

## Future Improvements

- **Additional Financial Ratios**  
  P/E, PEG, or free cash flow calculations.

- **Charting**  
  Graph quarterly data over time using a library like Plotly or Altair.

- **Fine-Tuning**  
  Explore domain-specific finetuning of GPT-4o for specialized financial tasks.

- **User Management**  
  Implement authentication to let multiple users save their analyses or limit internal data.

---

## License
This project is released under the [MIT License](LICENSE.md)

---

## Acknowledgments

- **OpenAI** for GPT-4o and the newly released agent tools (March 2025).  
- **CS7180 Teaching Staff** for guidelines and project structure.  
- Open-source maintainers of Streamlit, python-dotenv, and other libraries.

