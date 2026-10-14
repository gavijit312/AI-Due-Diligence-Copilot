import requests

API_BASE = "http://localhost:8000/api/v1"


def upload_document_api(file_bytes, filename: str, category: str):
    files = {"file": (filename, file_bytes)}
    data = {"category": category}
    return requests.post(f"{API_BASE}/documents/upload", files=files, data=data)


def fetch_documents_api():
    return requests.get(f"{API_BASE}/documents/")


def start_audit_api(target_company: str):
    return requests.post(f"{API_BASE}/audit/start", json={"target_company": target_company})


def get_audit_status_api(audit_id: str):
    return requests.get(f"{API_BASE}/audit/status/{audit_id}")


def ask_chat_api(query: str, category: str = None):
    payload = {"query": query}
    if category and category != "All":
        payload["category"] = category.lower()
    return requests.post(f"{API_BASE}/chat/query", json=payload)