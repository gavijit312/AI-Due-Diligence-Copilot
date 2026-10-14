from typing import Optional
from fastapi import APIRouter
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from rag.retriever import retriever
from rag.citations import build_cited_context, format_citations
from config.settings import settings

router = APIRouter(prefix="/chat", tags=["Document Chat"])


class ChatRequest(BaseModel):
    query: str
    category: Optional[str] = None


CHAT_PROMPT = """You are a senior due diligence analyst. Answer the user's question accurately using ONLY the provided verified document excerpts. 
Every material statement MUST reference its numbered citation anchor (e.g. [1], [2]).

Context:
{context}

Question: {query}
"""


@router.post("/query")
def chat_with_documents(payload: ChatRequest):
    docs = retriever.retrieve(query=payload.query, category=payload.category, top_k=5)
    context = build_cited_context(docs)

    llm = ChatOpenAI(model=settings.DEFAULT_LLM_MODEL, temperature=0.1, api_key=settings.OPENAI_API_KEY)
    chain = ChatPromptTemplate.from_template(CHAT_PROMPT) | llm
    response = chain.invoke({"context": context, "query": payload.query})

    return {
        "answer": response.content,
        "citations": format_citations(docs)
    }