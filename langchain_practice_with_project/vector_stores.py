# from langchain_chroma import Chroma
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores.faiss import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain_openai import OpenAI


pdf_data = PyPDFLoader("gst_certificate.pdf")
pdf_data =pdf_data.load()
text_loader = RecursiveCharacterTextSplitter(separators=[""],chunk_size =50, chunk_overlap =5)
split_data = text_loader.split_documents(pdf_data)
db = FAISS.from_documents(split_data,OpenAIEmbeddings())
data = db.similarity_search("what is firm name")
# qa =load_qa_chain(OpenAI(temperature=0.8))
# kk = qa.invoke({"input_documents":data,"question": "what is firm name"})
# print(kk)

# retriever = db.as_retriever()
# docs = retriever.invoke("what is firm name")
print(data)