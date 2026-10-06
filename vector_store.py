import chromadb
from services.embeddings import create_embeddings
DATABASE_PATH = "database/chroma"
client = chromadb.PersistentClient(
    path=DATABASE_PATH
)
collection = client.get_or_create_collection(
    name="thinkvault_documents"
)
def add_document(file_name, text):
    if not text.strip():
        return 0
    chunk_size = 800
    chunk_overlap = 120
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start += chunk_size - chunk_overlap
    if not chunks:
        return 0
    embeddings = create_embeddings(chunks)
    ids = [
        f"{file_name}_{index}"
        for index in range(len(chunks))
    ]
    metadatas = [
        {
            "file_name": file_name,
            "chunk_index": index
        }
        for index in range(len(chunks))
    ]
    collection.upsert(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas
    )
    return len(chunks)
def search_documents(query, n_results=5, file_name=None):
    query_embedding = create_embeddings(
        [query]
    )[0]
    query_kwargs = {
        "query_embeddings": [query_embedding],
        "n_results": n_results
    }
    if file_name:
        query_kwargs["where"] = {
            "file_name": file_name
        }
    results = collection.query(
        **query_kwargs
    )
    documents = results.get(
        "documents",
        [[]]
    )[0]
    metadatas = results.get(
        "metadatas",
        [[]]
    )[0]
    return list(
        zip(documents, metadatas)
    )