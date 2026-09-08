from pathlib import Path

from langchain_aws import ChatBedrock
from langchain_core.messages import HumanMessage, SystemMessage

from bmw_rag.settings import settings
from bmw_rag.tools.retriever import retrieve


SYSTEM_PROMPT = """
You are a document question-answering assistant.

Answer only from the supplied context.
If the answer is absent, say:
'I could not find that information in the indexed documents.'

Do not invent facts.
"""


def answer_question(question: str) -> dict:
    documents = retrieve(question)

    if not documents:
        return {
            "answer": "No indexed content was found.",
            "sources": []
        }

    context = "\n\n".join(
        document.page_content
        for document in documents
    )

    model = ChatBedrock(
        model_id=settings.chat_model,
        region_name=settings.aws_region,
        temperature=settings.temperature,
    )

    response = model.invoke([
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(
            content=f"Context:\n{context}\n\nQuestion: {question}"
        ),
    ])

    sources = []

    for document in documents:
        page = document.metadata.get("page")

        sources.append({
            "file": Path(
                document.metadata.get("source", "unknown")
            ).name,
            "page": page + 1 if page is not None else None,
        })

    return {
        "answer": response.content,
        "sources": sources,
    }