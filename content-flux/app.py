import time
import streamlit as st

from src.schemas import InputData, RefinementSettings, GeneratedOutput
from src.mock_engine import generate_mock_results

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Content Flux",
    page_icon="⚡",
    layout="wide",
)


# ---------------------------------------------------------------------------
# CSS Injector
# ---------------------------------------------------------------------------

def inject_custom_css() -> None:
    """Inject custom dark-mode CSS into the Streamlit app."""
    st.markdown(
        """
        <style>
        /* Main App Background & Typography */
        .stApp {
            background-color: #0B0F17 !important;
            color: #E2E8F0 !important;
            font-family: 'Inter', system-ui, -apple-system, sans-serif !important;
        }

        /* Header Stepper Styling (non-active cards) */
        div[data-testid="stMetric"] {
            background-color: #161F30 !important;
            border: 1px solid #2A3852 !important;
            border-radius: 10px !important;
            padding: 10px 16px !important;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2) !important;
        }

        /* Metric label & value colours */
        div[data-testid="stMetric"] label,
        div[data-testid="stMetricLabel"] {
            color: #64748B !important;
        }
        div[data-testid="stMetricValue"] {
            color: #CBD5E1 !important;
            font-size: 1rem !important;
        }
        div[data-testid="stMetricDelta"] svg { display: none; }
        div[data-testid="stMetricDelta"] {
            color: #22C55E !important;
            font-size: 0.72rem !important;
        }

        /* Primary Action Buttons */
        div.stButton > button {
            background: linear-gradient(135deg, #4A80F6 0%, #8DA4FF 100%) !important;
            color: #0A0F1D !important;
            font-weight: 700 !important;
            border-radius: 8px !important;
            border: none !important;
            padding: 0.65rem 1.6rem !important;
            box-shadow: 0px 4px 18px rgba(74, 128, 246, 0.35) !important;
            transition: all 0.25s ease-in-out !important;
        }

        div.stButton > button:hover {
            box-shadow: 0px 6px 24px rgba(74, 128, 246, 0.6) !important;
            transform: translateY(-2px) !important;
            color: #000000 !important;
        }

        /* Secondary / Reset Buttons */
        div.stButton > button[kind="secondary"] {
            background: #1E293B !important;
            color: #94A3B8 !important;
            border: 1px solid #334155 !important;
            box-shadow: none !important;
        }

        /* Container Cards for Generated Outputs */
        div[data-testid="stVerticalBlockBorderWrapper"] {
            background-color: #111827 !important;
            border: 1px solid #1E293B !important;
            border-radius: 12px !important;
            padding: 1.25rem !important;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3) !important;
            margin-bottom: 1rem !important;
        }

        /* Inputs, Selectboxes, and Textareas */
        .stTextArea textarea,
        .stSelectbox div[data-baseweb="select"],
        .stFileUploader {
            background-color: #111827 !important;
            border: 1px solid #243044 !important;
            border-radius: 8px !important;
            color: #F1F5F9 !important;
        }

        /* Progress bar — blue glow */
        div[data-testid="stProgressBar"] > div > div {
            background: linear-gradient(90deg, #4A80F6, #8DA4FF) !important;
            box-shadow: 0 0 10px rgba(74, 128, 246, 0.55) !important;
        }
        div[data-testid="stProgressBar"] {
            border-radius: 999px !important;
            overflow: hidden !important;
        }

        /* st.status / expander container */
        div[data-testid="stExpander"] {
            background-color: #0F1822 !important;
            border: 1px solid #1E293B !important;
            border-radius: 10px !important;
        }

        /* Dividers */
        hr { border-color: #1E293B !important; }

        /* Sidebar / left panel background */
        section[data-testid="stSidebar"] {
            background-color: #0D1321 !important;
        }

        /* Code blocks */
        .stCodeBlock { background-color: #0D1321 !important; }

        /* Hide Default Streamlit Branding Elements */
        #MainMenu, footer, header { visibility: hidden; }
        </style>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Session state initialisation
# ---------------------------------------------------------------------------
inject_custom_css()

if "step" not in st.session_state:
    st.session_state.step = 1
if "input_data" not in st.session_state:
    st.session_state.input_data = None
if "outputs" not in st.session_state:
    st.session_state.outputs = []
if "refinement_settings" not in st.session_state:
    st.session_state.refinement_settings = None


# ---------------------------------------------------------------------------
# Global stepper header
# ---------------------------------------------------------------------------

_STAGE_DEFS = [
    (1, "Stage 1", "Ingest & Select"),
    (2, "Stage 2", "Generating Drafts"),
    (3, "Stage 3", "Review & Refine"),
]

_ACTIVE_CARD_CSS = (
    "background-color:#131E35;"
    "border:1px solid #4A80F6;"
    "border-radius:10px;"
    "padding:12px 18px;"
    "box-shadow:0 0 18px rgba(74,128,246,0.35);"
    "margin-bottom:4px;"
)
_ACTIVE_LABEL_CSS = "font-size:0.72rem;color:#4A80F6;font-weight:700;letter-spacing:0.05em;"
_ACTIVE_VALUE_CSS = "font-size:1rem;font-weight:700;color:#E2E8F0;margin-top:4px;"
_ACTIVE_BADGE_CSS = (
    "display:inline-block;"
    "margin-top:6px;"
    "background:#4A80F6;"
    "color:#fff;"
    "font-size:0.62rem;"
    "font-weight:700;"
    "border-radius:4px;"
    "padding:1px 7px;"
    "letter-spacing:0.08em;"
)


def render_stepper() -> None:
    """Render a 3-step progress header indicating the active stage."""
    current = st.session_state.step
    cols = st.columns(len(_STAGE_DEFS))

    for col, (num, label, title) in zip(cols, _STAGE_DEFS):
        with col:
            if num < current:
                st.metric(
                    label=f"✅ {label}",
                    value=title,
                    delta="Complete",
                )
            elif num == current:
                st.markdown(
                    f'''<div style="{_ACTIVE_CARD_CSS}">
                      <div style="{_ACTIVE_LABEL_CSS}">▶ {label}</div>
                      <div style="{_ACTIVE_VALUE_CSS}">{title}</div>
                      <div style="{_ACTIVE_BADGE_CSS}">ACTIVE</div>
                    </div>''',
                    unsafe_allow_html=True,
                )
            else:
                st.metric(label=f"○ {label}", value=title)

    st.divider()


# ---------------------------------------------------------------------------
# Step 1 — Ingest & Select
# ---------------------------------------------------------------------------

DELIVERABLE_OPTIONS = [
    "Executive Summary",
    "LinkedIn Thought Leadership",
    "Strategic Advisory Memo",
    "Executive Video Script",
]


def render_step_1() -> None:
    """Step 1: Collect deliverable selections, uploaded files, and context."""
    left, right = st.columns([1, 2])

    with left:
        st.subheader("Required Deliverables")
        st.caption(
            "Select output formats to synthesize in parallel from your source material. "
            "Models adapt style, structure, and compression factors dynamically."
        )

        selected = []
        for option in DELIVERABLE_OPTIONS:
            if st.checkbox(option, value=True, key=f"chk_{option}"):
                selected.append(option)

        st.markdown(
            f'''<span style="background:#1E3A5F;color:#60A5FA;border-radius:5px;
            padding:3px 10px;font-size:0.75rem;font-weight:700;">
            {len(selected)} deliverable(s) selected</span>''',
            unsafe_allow_html=True,
        )

    with right:
        st.subheader("Upload Source Documents")
        uploaded_files = st.file_uploader(
            "Drag & drop source repositories or technical drafts",
            type=["pdf", "docx", "xlsx"],
            accept_multiple_files=True,
            help="Supports PDF, DOCX, and XLSX files.",
        )

        if uploaded_files:
            st.success(f"{len(uploaded_files)} file(s) staged for parsing.")

        st.subheader("Context & Strategic Guardrails")
        raw_text = st.text_area(
            "Paste supplemental qualitative notes, meeting transcripts, or strategic imperatives",
            placeholder=(
                "e.g. ‘Emphasise AI safety, target enterprise CTO persona, "
                "maintain objective tone’…"
            ),
            height=160,
        )

        st.divider()

        col_btn, _ = st.columns([1, 2])
        with col_btn:
            generate_clicked = st.button(
                "Generate Outputs →",
                type="primary",
                use_container_width=True,
            )

        if generate_clicked:
            if not selected:
                st.error("Please select at least one deliverable before generating.")
                return

            file_names = [f.name for f in uploaded_files] if uploaded_files else []

            st.session_state.input_data = InputData(
                raw_text=raw_text,
                uploaded_files=file_names,
                selected_deliverables=selected,
            )
            st.session_state.step = 2
            st.rerun()


# ---------------------------------------------------------------------------
# Step 2 — Processing / Generation
# ---------------------------------------------------------------------------

PIPELINE_STAGES = [
    ("📄", "Parsing source documents and context..."),
    ("🔍", "Extracting key metrics and narrative hooks..."),
    ("✨", "Synthesizing deliverable drafts..."),
]


def render_step_2() -> None:
    """Step 2: Animated pipeline view, calls mock engine, advances to Step 3."""
    _, center, _ = st.columns([1, 2, 1])

    with center:
        st.markdown(
            '''<h2 style="text-align:center;color:#E2E8F0;margin-bottom:4px;">
            Synthesizing Multi-Format Deliverables…</h2>
            <p style="text-align:center;color:#64748B;margin-top:0;">
            Cross-distilling strategic documents into high-resonance channel
            drafts via parallel neural passes.</p>''',
            unsafe_allow_html=True,
        )
        st.divider()

        progress_bar = st.progress(0, text="Initialising pipeline…")
        total = len(PIPELINE_STAGES)

        with st.status("🧠 Autonomous Generation  —  Pipeline Active", expanded=True) as pipeline_status:
            for i, (icon, message) in enumerate(PIPELINE_STAGES, start=1):
                st.write(f"{icon}  {message}")
                pct = int((i / total) * 90)
                progress_bar.progress(pct, text=message)
                time.sleep(0.8)

            outputs = generate_mock_results(st.session_state.input_data)
            st.session_state.outputs = outputs

            st.write("✅  All deliverables synthesized successfully.")
            pipeline_status.update(
                label="✅ Pipeline Complete — All drafts ready.",
                state="complete",
                expanded=False,
            )

        progress_bar.progress(100, text="Complete!")
        time.sleep(0.5)

    st.session_state.step = 3
    st.rerun()


# ---------------------------------------------------------------------------
# Step 3 — Review & Refine
# ---------------------------------------------------------------------------

AUDIENCE_OPTIONS = [
    "Executive Leadership (C-Suite)",
    "Technical / Engineering Leads",
    "General Audience",
    "Board & Investors",
]

TONE_OPTIONS = [
    "Authoritative & Analytical",
    "Engaging & Conversational",
    "Concise & Direct",
    "Inspirational & Forward-Looking",
]

# Badge colour map keyed by deliverable type keyword
_BADGE_COLOURS: dict[str, tuple[str, str]] = {
    "Executive Summary":         ("#1E3A5F", "#60A5FA"),
    "LinkedIn":                  ("#0A3D2E", "#34D399"),
    "Strategic Advisory":        ("#3B1F5E", "#A78BFA"),
    "Video Script":              ("#3D1F1F", "#F87171"),
}


def _badge_colour(deliverable_type: str) -> tuple[str, str]:
    """Return (bg, fg) hex colours for a deliverable type badge."""
    for key, colours in _BADGE_COLOURS.items():
        if key.lower() in deliverable_type.lower():
            return colours
    return ("#1E293B", "#94A3B8")


def _reading_stats(text: str) -> tuple[int, str]:
    """Return (word_count, formatted_reading_time_string)."""
    words = len(text.split())
    minutes = max(1, round(words / 200))
    label = f"{minutes} min read"
    return words, label


def render_step_3() -> None:
    """Step 3: Refinement sidebar + styled output cards with badges."""
    # Top action bar
    header_left, header_right = st.columns([3, 1])
    with header_left:
        st.subheader(
            f"Generated Deliverables  ·  {len(st.session_state.outputs)} Ready"
        )
    with header_right:
        if st.button("🔄 Start New Campaign", use_container_width=True):
            st.session_state.step = 1
            st.session_state.input_data = None
            st.session_state.outputs = []
            st.session_state.refinement_settings = None
            st.rerun()

    st.divider()

    left, right = st.columns([1, 2.5])

    # Left column: Refinement sidebar
    with left:
        st.subheader("Refine Parameters")

        audience = st.selectbox(
            "Target Audience",
            options=AUDIENCE_OPTIONS,
            index=0,
        )
        tone = st.selectbox(
            "Communication Tone",
            options=TONE_OPTIONS,
            index=0,
        )

        st.caption("Adjustments apply to all draft outputs on regeneration.")

        if st.button(
            "Apply Refinements to All Drafts",
            type="primary",
            use_container_width=True,
        ):
            settings = RefinementSettings(audience=audience, tone=tone)
            st.session_state.refinement_settings = settings
            st.success(
                f"Refinements queued — re-generation wired in Phase 4."
            )

        if st.session_state.refinement_settings:
            rs = st.session_state.refinement_settings
            st.markdown(
                f'''<div style="background:#0F1822;border:1px solid #1E293B;
                border-radius:8px;padding:10px 14px;margin-top:8px;">
                <div style="color:#64748B;font-size:0.7rem;font-weight:600;
                letter-spacing:0.06em;">ACTIVE REFINEMENT</div>
                <div style="color:#E2E8F0;font-size:0.85rem;margin-top:6px;">
                👥 {rs.audience}</div>
                <div style="color:#E2E8F0;font-size:0.85rem;margin-top:4px;">
                🎯 {rs.tone}</div>
                </div>''',
                unsafe_allow_html=True,
            )

    # Right column: Output cards
    with right:
        if not st.session_state.outputs:
            st.warning("No outputs found. Return to Step 1 and generate content.")
            return

        for idx, output in enumerate(st.session_state.outputs):
            bg, fg = _badge_colour(output.deliverable_type)
            words, read_time = _reading_stats(output.content)

            with st.container(border=True):
                # Card header row: type badge + stats + regen button
                badge_col, regen_col = st.columns([3, 1])

                with badge_col:
                    st.markdown(
                        f'''<span style="background:{bg};color:{fg};border-radius:5px;
                        padding:3px 10px;font-size:0.72rem;font-weight:700;">
                        {output.deliverable_type}</span>&nbsp;&nbsp;
                        <span style="color:#475569;font-size:0.72rem;">
                        {words} words · {read_time}</span>''',
                        unsafe_allow_html=True,
                    )

                with regen_col:
                    if st.button(
                        "🔁 Regenerate",
                        key=f"regen_{idx}",
                        help=f"Regenerate ‘{output.deliverable_type}’",
                    ):
                        st.toast(
                            f"Regeneration of ‘{output.deliverable_type}’ queued.",
                            icon="ℹ️",
                        )

                st.markdown(output.content)

                with st.expander("📋 Copy raw content", expanded=False):
                    st.code(output.content, language="markdown")

                st.caption(
                    f"Deliverable type: `{output.deliverable_type}`"
                )


# ---------------------------------------------------------------------------
# Step router
# ---------------------------------------------------------------------------

render_stepper()

STEP_RENDERERS = {
    1: render_step_1,
    2: render_step_2,
    3: render_step_3,
}

renderer = STEP_RENDERERS.get(st.session_state.step)
if renderer:
    renderer()
else:
    st.session_state.step = 1
    st.rerun()
