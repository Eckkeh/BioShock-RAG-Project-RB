import json
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from transformers import T5Tokenizer, T5ForConditionalGeneration

# Load embeddings from file
def load_embeddings(filename="embeddings.json"):
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)

# Convert dictionary embeddings back to NumPy arrays
def prepare_embeddings(embedding_dict):
    texts = list(embedding_dict.keys())
    embeddings = np.array([embedding_dict[text] for text in texts])
    return texts, embeddings

# Get the most relevant chunks based on the query and cosine similarity
def get_relevant_chunks(query, embedding_dict, model, top_n=3):
    query_embedding = model.encode([query], convert_to_tensor=True).cpu().numpy()
    similarities = {}

    query_embedding = query_embedding.reshape(1, -1)  # Ensure query embedding is 2D
    
    for text, embedding in embedding_dict.items():
        embedding = np.array(embedding).reshape(1, -1)
        similarity = cosine_similarity(query_embedding, embedding)[0][0]
        similarities[text] = similarity

    sorted_chunks = sorted(similarities.items(), key=lambda item: item[1], reverse=True)
    top_chunks = sorted_chunks[:top_n]

    relevant_chunks = [chunk[0][:250] + "..." if len(chunk[0]) > 250 else chunk[0] for chunk in top_chunks]  # Trim to 250 chars max

    return relevant_chunks

# Generate response using FLAN-T5 model
def generate_response(query, retrieved_chunks):
    model_name = "google/flan-t5-small"
    tokenizer = T5Tokenizer.from_pretrained(model_name)
    model = T5ForConditionalGeneration.from_pretrained(model_name)
    
    # Combine retrieved chunks into a single prompt
    input_text = f"Context: {' '.join(retrieved_chunks)} Query: {query}"
    
    # Tokenize and generate response
    inputs = tokenizer(input_text, return_tensors="pt", max_length=512, truncation=True)
    outputs = model.generate(**inputs, max_length=150)
    
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# Main function to handle user queries
def main():
    print("Type your query (or 'exit' to quit):")
    
    # Load stored embeddings
    embedding_dict = load_embeddings()
    texts, embeddings = prepare_embeddings(embedding_dict)
    
    # Load SentenceTransformer model
    model = SentenceTransformer("all-MiniLM-L6-v2")
    
    while True:
        query = input("\nEnter your query: ")
        if query.lower() == "exit":
            break
        
        # Retrieve relevant content
        retrieved_chunks = get_relevant_chunks(query, embedding_dict, model)
        print("\nRetrieved Text Chunks:")
        for chunk in retrieved_chunks:
            print(f"- {chunk[:200]}...") 

        # Generate response
        response = generate_response(query, retrieved_chunks)
        print("\nGenerated Response:", response)

if __name__ == "__main__":
    main()