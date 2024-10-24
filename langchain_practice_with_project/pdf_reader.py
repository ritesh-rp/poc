from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores.faiss import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.chains.question_answering import load_qa_chain
from langchain_openai import OpenAI
from langchain_community.document_loaders import PyPDFLoader
# from langchain_chroma import Chroma


import os
from dotenv import load_dotenv
load_dotenv()


pdf_reader = PyPDFLoader("gst_certificate.pdf")
documents = pdf_reader.load()
# raw_text =""


# for i,page in enumerate(pdf_reader.pages):
#     text = page.extract_text()
#     if text:
#         raw_text += text
# print(raw_text)
text_splitter = RecursiveCharacterTextSplitter()
texts = text_splitter.split_documents(documents)
embeddings = OpenAIEmbeddings()
document_search =FAISS.from_documents(texts,embeddings)
chain = load_qa_chain(OpenAI(temperature=0.8),chain_type="stuff")
query = "what is the firm name"
docs = document_search.similarity_search(query)
ress = chain.invoke({"input_documents" :docs, "question":query})
print(1111111111111111,ress)