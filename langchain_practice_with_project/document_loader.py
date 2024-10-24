from langchain_community.document_loaders.html import UnstructuredHTMLLoader
from langchain_community.document_loaders.html_bs import BSHTMLLoader
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.document_loaders.pdf import PyPDFLoader 
from langchain_community.document_loaders.web_base import WebBaseLoader

# loader = UnstructuredHTMLLoader("demo.html")

# loader = BSHTMLLoader("demo.html")

# loader = CSVLoader("/home/user/Downloads/AUG- 2023 purchase (1).csv")

# loader = PyPDFLoader("gst_certificate.pdf")

loader = WebBaseLoader("https://python.langchain.com/docs/integrations/document_loaders/web_base/")

data = loader.load()

print(111111111111111111111,data)