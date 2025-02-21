import os
from docx import Document
import openai

f = open("first_open_ai_key","r")
open_ai_key = f.read()
f.close()

openai.api_key = open_ai_key

def split_text(text):
    max_chunk_size = 2048
    chunks = []
    current_chunk = ""
    for sentence in text.split("."):
        if len(current_chunk) + len(sentence) < max_chunk_size:
            current_chunk += sentence + "."
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + "."
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

def summarize_text(text):
    input_chunks = split_text(text)
    output_chunks = []
    for chunk in input_chunks:
        response = openai.completions.create(
            model="gpt-3.5-turbo-instruct",  
            prompt=(f"You are a professional journalist. Please summarize the following text to five points in Chinese words. Then translate these points to English and these five points should not exceed 300 English words in total:\n{chunk}\n\nSummary:"),
            max_tokens=300  
        )
        summary = response.choices[0].text.strip()
        output_chunks.append(summary)
        response = openai.completions.create(
            model="gpt-3.5-turbo-instruct", 
            prompt=(f"You are a professional journalist. Please summarize the following points to five major points starting with 1., 2., 3., 4., 5., these five points should not exceed 300 English words in total:\n{output_chunks}\n\nSummary:"),
            max_tokens=300  
        )
        final_summary = response.choices[0].text.strip()
    return final_summary


folder_path = 'newspaper'

for filename in os.listdir(folder_path):
    if filename.endswith('.docx'):
        file_path = os.path.join(folder_path, filename)
        doc = Document(file_path)
        full_text = []
        for para in doc.paragraphs:
            full_text.append(para.text)
        text = '\n'.join(full_text)
        
        summary = summarize_text(text)
        print(f'Finished processing {filename}')
        print(f"Summary for {filename}:\n{summary}\n\n")