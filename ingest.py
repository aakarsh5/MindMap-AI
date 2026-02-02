from sentence_transformers import SentenceTransformer
from pypdf import PdfReader
import requests, uuid, time

model = SentenceTransformer('all-MiniLM-L6-v2')

def chunk(text, size=500):
    return [text[i:i+size] for i in range(0, len(text), size)]

def ingest(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""

    for p in reader.pages:
        page_text = p.extract_text()
        if page_text:
            text += page_text

    chunks = chunk(text)
    print(f"Total chunks: {len(chunks)}")

    vectors = []

    for c in chunks:
        vec = model.encode(c).tolist()

        vectors.append({
            "id": str(uuid.uuid4()),
            "dense_vector": vec,
            "metadata": {"text": c}
        })

    BATCH_SIZE = 5

    for i in range(0, len(vectors), BATCH_SIZE):
        batch = vectors[i:i+BATCH_SIZE]

        payload = {"vectors": batch}

        print(f"Inserting batch {i//BATCH_SIZE + 1} ...")

        res = requests.post(
            "http://127.0.0.1:8080/api/v1/index/mindmap/vector/insert",
            json=payload,
            timeout=120
        )

        print(res.text)

        time.sleep(1)

ingest("data/Interactive_Concept_Bottleneck_Models.pdf")
