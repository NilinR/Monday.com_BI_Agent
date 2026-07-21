# Monday.com BI Agent – Architecture & Decision Log

**Live Application:** [monday-bi-agent-beta.vercel.app](https://monday-bi-agent-beta.vercel.app/)  
**GitHub Repository:** [NilinR/Monday.com_BI_Agent](https://github.com/NilinR/Monday.com_BI_Agent)

### 1. System Architecture & Assumptions
* **REST Model:** Built a decoupled architecture using a Python (FastAPI) backend and a React (Vite + `remark-gfm`- for displaying tables and md output properly) frontend. This guarantees clear separation, quicker response rendering, and easy cloud serverless deployment.
* **Data Completeness Assumption:** Assumed CRM data from monday.com is inherently imperfect (after preprocessing the data of course). Sanitization must occur programmatically *before* LLM ingestion to avoid hallucinations and token waste.
* **Founder Intent:** Assumed business leaders prioritize actionable risk warnings (like stale high-value deals, missing product metrics) over raw, unvalidated financial sums.

### 2. Technical Trade-offs & Rationale
* **Deterministic Python Cleaning vs. Pure LLM Processing:** 
  * *Choice:* Programmatically transformed and sanitized monday.com GraphQL payloads using Python prior to feeding them to Gemini.
  * *Trade-off:* Requires explicit data-handling logic in Python, but dramatically reduces token consumption, cuts latency under Vercel serverless constraints, and eliminates mathematical hallucination risks.
* **Direct API Execution vs. Agent Framework Overheads (LangChain/MCP):**
  * *Choice:* Used direct HTTP calls to monday.com and standard OpenAI-compatible client libraries.
  * *Trade-off:* Bypasses heavy frameworks, ensuring lightweight serverless execution, fast starts on Vercel, and total control over prompt engineering.
* **Gemini 3.1 Flash-Lite Model:**
  * *Choice:* Selected `gemini-3.1-flash-lite` for inference.
  * *Trade-off:* Delivers frontier-level analytical performance across large token windows while maintaining high throughput under strict rate limits.

### 3. Creative Executions & Strengths
* **Hybrid Data Processing Pipeline:** Rather than relying entirely on the LLM to parse messy JSON, the system enforces a strict Python sanitization layer. Missing fields, trailing whitespaces, and inconsistent date formats are normalized programmatically, ensuring high data resilience and preventing the AI from hallucinating math on null values.
* **Zero-Friction User Experience:** Designed the UI with a product-first mindset. Instead of an empty chat interface, the frontend includes quick-test Prompt Chips and a dedicated "Leadership Brief" trigger, anticipating executive needs.
* **Production-Grade Visuals:** Implemented GitHub-flavored markdown parsing (`remark-gfm`) on the React frontend. This transforms standard text responses into executive ready reports complete with data tables, bolded metrics, and clean formatting, significantly elevating the readability of the AI's output.

### 4. Leadership Updates Implementation
* Interpreted the optional "Leadership Updates" requirement as an **on-demand executive briefing engine**. Exposed a dedicated `/api/leadership-update` REST endpoint triggered by a one-click UI button, delivering concise executive summaries highlighting revenue totals, pipeline data flaws, and operational risks across both Deals and Work Orders boards simultaneously.

### 5. Future Improvements (Given More Time)
* Implement vector embeddings or local SQLite caching to handle multi-year historical board data exceeding standard LLM context windows.
* Add interactive data visualization components (e.g., Recharts) alongside Markdown reports.