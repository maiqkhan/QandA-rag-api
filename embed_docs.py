import chromadb 
from pathlib import Path

client = chromadb.PersistentClient(path="./db")
collection = client.get_or_create_collection("docs")

# Clear existing documents 
existing_ids = collection.get()['ids']
if existing_ids:
    collection.delete(ids=existing_ids)

for filename in Path("./docs").glob("*.txt"):
    if filename.suffix == ".txt":
        with open(filename, "r") as f:
            text = f.read()
            collection.add(documents=[text], ids=[filename.stem])


print("Embedding stored in Chroma!")