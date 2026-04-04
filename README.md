# Smart Resource Allocator 💡

A high-fidelity modern dashboard for NGOs to manage community needs and volunteer allocation during crisis events.

## 🚀 Ethical AI Usage & Data Privacy

This project is built with a **Privacy-First** philosophy. We recognize the sensitivity of community data in crisis zones. 

### Privacy Guardrails:
*   **Automatic PII Redaction**: Our AI extraction pipeline (Gemini 1.5 Flash) is hard-coded to identify and redact Personally Identifiable Information (PII) such as names, phone numbers, and IDs, replacing them with `[REDACTED]` before they ever touch our database.
*   **Administrative Oversight**: No AI-extracted data goes live on the public-facing maps or analytics without **Manual Human Verification**. 
*   **Deduplication**: We prevent "data noise" by identifying and merging duplicate reports, ensuring that volunteers aren't dispatched to phantom or redundant incidents.
*   **Limited Data Retention**: For this prototype, all data is stored in-memory (st.session_state). In a production environment, we recommend end-to-end encryption for the backend database.

## 🛠️ Setup & Technical Configuration

### Prerequisites
*   Python 3.10+
*   Google Gemini API Key

### Configuration (.env)
Create a `.env` file in the root directory (mapped from `.env.example`) and add your key:
```env
GEMINI_API_KEY=your_api_key_here
```

### Installation
```bash
pip install -r requirements.txt
streamlit run app.py
```

## 📐 Core Architecture
*   **Dashboard**: A Bento-Grid Glassmorphism UI built with Tailwind/HTML components.
*   **Matching**: An AI-augmented engine that prioritizes Urgency > Skill > Proximity.
*   **Analytics**: Plotly-driven impact tracking for executive stakeholders.
