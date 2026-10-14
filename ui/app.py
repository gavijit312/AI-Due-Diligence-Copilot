import sys
from pathlib import Path

# Add project root directory to Python path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

import time
import streamlit as st
from ui.utils import (
    upload_document_api,
    fetch_documents_api,
    start_audit_api,
    get_audit_status_api,
    ask_chat_api
)

# Page configuration
st.set_page_config(
    page_title="DueSense AI – Due Diligence Copilot",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Header
st.title("🚀 DueSense AI – Multi-Agent Due Diligence Copilot")
st.markdown("Automated Legal, Financial, and Compliance Due Diligence using LangGraph & RAG.")
st.divider()

# Create tabs
tabs = st.tabs(["📁 Document Room", "🤖 Multi-Agent Audit", "💬 Diligence Q&A"])

# ----------------- TAB 1: Document Upload -----------------
with tabs[0]:
    st.subheader("Data Room Document Ingestion")
    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown("#### Upload Corporate Records")
        uploaded_file = st.file_uploader(
            "Select corporate file (.pdf, .docx, .xlsx)",
            type=["pdf", "docx", "xlsx"]
        )
        category = st.selectbox(
            "Target Domain Category",
            ["legal", "financial", "compliance", "general"]
        )
        if st.button("🚀 Ingest Document", type="primary") and uploaded_file:
            with st.spinner("Extracting, parsing, and chunking into ChromaDB..."):
                try:
                    res = upload_document_api(uploaded_file.getvalue(), uploaded_file.name, category)
                    if res.status_code == 200:
                        st.success(f"Successfully indexed '{uploaded_file.name}' into {category} store!")
                        st.rerun()
                    else:
                        st.error(f"Error ({res.status_code}): {res.text}")
                except Exception as e:
                    st.error(f"Connection failure to FastAPI: {e}")

    with col2:
        st.markdown("#### Ingested Documents Repository")
        try:
            res = fetch_documents_api()
            if res.status_code == 200:
                docs = res.json()
                if docs:
                    st.dataframe(docs, use_container_width=True)
                else:
                    st.info("No documents uploaded yet. Upload a file on the left to begin.")
            else:
                st.warning(f"Could not retrieve documents from backend (Status {res.status_code}).")
        except Exception as e:
            st.error(f"Cannot connect to FastAPI backend at http://localhost:8000: {e}")

# ----------------- TAB 2: Multi-Agent Audit -----------------
with tabs[1]:
    st.subheader("Autonomous Multi-Agent Audit Run")
    target_company = st.text_input("Target Entity / Acquisition Candidate", value="Acme Technologies Inc.")

    if st.button("⚡ Trigger Multi-Agent Analysis", type="primary"):
        try:
            res = start_audit_api(target_company)
            if res.status_code == 200:
                audit_id = res.json()["audit_id"]
                st.session_state["current_audit_id"] = audit_id
                st.info(f"Audit Queued! Session ID: `{audit_id}`")
            else:
                st.error(f"Failed to start audit: {res.text}")
        except Exception as e:
            st.error(f"API Connection error: {e}")

    if "current_audit_id" in st.session_state:
        audit_id = st.session_state["current_audit_id"]
        status_box = st.empty()

        with st.spinner("Agents analyzing legal, financial, and compliance streams in parallel..."):
            for _ in range(60):
                try:
                    status_res = get_audit_status_api(audit_id)
                    if status_res.status_code == 200:
                        data = status_res.json()
                        curr_status = data["status"]
                        status_box.markdown(f"**Current Status:** `{curr_status}`")

                        if curr_status == "COMPLETED":
                            report = data.get("report") or {}
                            st.success(f"Audit Complete! Overall Risk Score: **{data.get('risk_score', 'N/A')}**")

                            st.markdown("### 📋 Executive Summary")
                            st.markdown(report.get("executive_summary") or "No summary generated.")

                            st.markdown("### 🔍 Specialized Domain Findings")
                            c1, c2, c3 = st.columns(3)
                            with c1:
                                st.markdown("#### ⚖️ Legal")
                                st.json(report.get("legal") or {})
                            with c2:
                                st.markdown("#### 💰 Financial")
                                st.json(report.get("financial") or {})
                            with c3:
                                st.markdown("#### ✅ Compliance")
                                st.json(report.get("compliance") or {})
                            break

                        elif curr_status == "FAILED":
                            st.error("Audit workflow execution encountered an error.")
                            st.json(data.get("report") or {})
                            break
                    time.sleep(2)
                except Exception as e:
                    st.error(f"Polling failed: {e}")
                    break

# ----------------- TAB 3: Diligence Chat -----------------
with tabs[2]:
    st.subheader("Cited Grounding Q&A")
    chat_filter = st.selectbox("Filter Domain Focus", ["All", "legal", "financial", "compliance"])
    user_query = st.text_input("Ask a due diligence query (e.g., 'What are the uncapped indemnification clauses?'):")

    if st.button("Ask Copilot") and user_query:
        with st.spinner("Retrieving document chunks and synthesizing answer with citations..."):
            try:
                res = ask_chat_api(user_query, chat_filter)
                if res.status_code == 200:
                    answer_data = res.json()
                    st.markdown("### Answer")
                    st.write(answer_data.get("answer", ""))

                    citations = answer_data.get("citations", [])
                    if citations:
                        st.markdown("### Source Citations")
                        for cit in citations:
                            with st.expander(f"📄 {cit.get('source')} (Page {cit.get('page')}) — {cit.get('category').upper()}"):
                                st.write(cit.get("excerpt"))
                else:
                    st.error(f"Error ({res.status_code}): {res.text}")
            except Exception as e:
                st.error(f"Chat request failed: {e}")