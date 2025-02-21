from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import WebBaseLoader
from langchain.chains import MapReduceDocumentsChain, ReduceDocumentsChain
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import os
from docx import Document
f = open("first_open_ai_key","r")
open_ai_key = f.read()
f.close()



llm = ChatOpenAI(temperature=0, openai_api_key=open_ai_key)
chain = load_summarize_chain(llm, chain_type="stuff")

map_template = """The following is a set of documents
{docs}
Based on this list of docs, please identify the main themes in Chinese words
Helpful Answer:"""
map_prompt = PromptTemplate.from_template(map_template)
map_chain = LLMChain(llm=llm, prompt=map_prompt)

reduce_template = """The following is set of summaries:
{docs}
Take these and distill it into five points of the main themes starting with 1., 2., 3., 4., 5..
These five points should not exceed 300 English words in total:"""
reduce_prompt = PromptTemplate.from_template(reduce_template)

reduce_chain = LLMChain(llm=llm, prompt=reduce_prompt)

combine_documents_chain = StuffDocumentsChain(
    llm_chain=reduce_chain, document_variable_name="docs"
)


reduce_documents_chain = ReduceDocumentsChain(
    combine_documents_chain=combine_documents_chain,
    collapse_documents_chain=combine_documents_chain,
    token_max=4000,
)


map_reduce_chain = MapReduceDocumentsChain(
    llm_chain=map_chain,
    reduce_documents_chain=reduce_documents_chain,
    document_variable_name="docs",
    return_intermediate_steps=False,
)

text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=1000, chunk_overlap=0
)


class DocumentObject:
    def __init__(self, text, metadata=None):
        self.page_content = text
        self.metadata = metadata if metadata is not None else {}
docs = []

folder_path = 'newspaper'
for filename in os.listdir(folder_path):
    if filename.endswith('.docx'):
        file_path = os.path.join(folder_path, filename)
        doc = Document(file_path)
        full_text = '\n'.join([para.text for para in doc.paragraphs])
        docx_doc = DocumentObject(full_text)
        docs.append(docx_doc)

        split_docs = text_splitter.split_documents(docs)
        print('\n')
        print(f'Finished processing {filename}')
        print(f"Summary for {filename}:")
        print(map_reduce_chain.run(split_docs))