from sentence_transformers import SentenceTransformer
import json

# Load the document
def load_document(filename):
    with open(filename, "r", encoding="utf-8") as file:
        content = file.read()
    return content

# Split document into smaller chunks (~200 words each)
def split_into_chunks(text, chunk_size=200):
    words = text.split()  # Split into words
    chunks = []
    
    for i in range(0, len(words), chunk_size):  # Process every 200 words
        chunk = " ".join(words[i:i + chunk_size])  # Create a chunk of 200 words
        chunks.append(chunk)

    return chunks

# Generate embeddings using SentenceTransformers
def generate_embeddings(chunks):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(chunks, convert_to_tensor=True)
    
    # Store embeddings in a dictionary
    embedding_dict = {chunks[i]: embeddings[i].tolist() for i in range(len(chunks))}
    return embedding_dict

# Save embeddings to a JSON file
def save_embeddings(embedding_dict, output_file="embeddings.json"):
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(embedding_dict, file, indent=4)

# Main execution
if __name__ == "__main__":
    document_text = load_document("Selected_Document.txt")
    text_chunks = split_into_chunks(document_text)  # Now correctly chunked
    embeddings = generate_embeddings(text_chunks)
    
    save_embeddings(embeddings)
    print("Embeddings successfully generated and saved to embeddings.json.")