1. System Architecture & State
The application is a single-page Streamlit app (app.py) driven by st.session_state. The pipeline operates in three distinct phases:

st.session_state.step = 1: Ingest & Select (Data entry)

st.session_state.step = 2: Processing (Simulated loading/spinner)

st.session_state.step = 3: Review & Refine (Post-generation customization)

2. File Tree Structure
Generate the skeleton for this exact directory structure. Use placeholder logic for the backend engines.

Plaintext
content-flux/
├── app.py                   # Main Streamlit UI and state router
├── requirements.txt         # streamlit, pydantic
└── src/
    ├── __init__.py
    ├── schemas.py           # Pydantic data contracts
    └── mock_engine.py       # Dummy generator to simulate backend work
3. Data Contracts (src/schemas.py)
Implement these exact Pydantic models to ensure all 6 team members share the same data structures.

Python
from pydantic import BaseModel
from typing import List, Optional, Dict

class InputData(BaseModel):
    raw_text: str
    uploaded_files: List[str]
    selected_deliverables: List[str]

class RefinementSettings(BaseModel):
    audience: str
    tone: str

class GeneratedOutput(BaseModel):
    deliverable_type: str
    content: str
4. UI Component Instructions (app.py)

Step 1 View: Render a main column with st.file_uploader and st.text_area for context. Render checkboxes for deliverable types (Executive Summary, LinkedIn, Video Script). Add a st.button to trigger Step 2.

Step 2 View: Render st.spinner or st.progress to simulate processing for 3 seconds, then automatically advance to Step 3.

Step 3 View: Use st.columns([1, 3]). The left column acts as the Refinement Sidebar (dropdowns for Target Audience and Tone, plus a 'Regenerate' button). The right column renders the GeneratedOutput data inside styled st.container or st.expander cards.
5. Custom Styling Contract (CSS Injection)
Inject the following CSS at the top of app.py using st.markdown('<style>...</style>', unsafe_allow_html=True):

/* Primary Action Buttons (Generate Outputs) */
div.stButton > button {
    background: linear-gradient(135deg, #4A80F6 0%, #A3B8FF 100%) !important;
    color: #0F172A !important;
    font-weight: 600 !important;
    border-radius: 8px !important;
    border: none !important;
    padding: 0.6rem 1.5rem !important;
    box-shadow: 0px 4px 15px rgba(74, 128, 246, 0.3) !important;
    transition: all 0.3s ease-in-out !important;
}

/* Button Hover State */
div.stButton > button:hover {
    box-shadow: 0px 6px 22px rgba(74, 128, 246, 0.55) !important;
    transform: translateY(-2px) !important;
}