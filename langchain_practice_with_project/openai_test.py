from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate,ChatPromptTemplate
from langchain.chains.sequential import  SimpleSequentialChain
from langchain.chains.llm import LLMChain
from langchain_community.llms import ollama, huggingface_endpoint
import streamlit as st
import os
from dotenv import load_dotenv
load_dotenv()



st.title("Langchain Openai")
llm =OpenAI(temperature=0.8, api_key=os.environ.get("KEY"))
text_input = st.text_input("search the topic you want")


# prompt_search =  PromptTemplate(input_variables=["name"],template="Tell me about celebrity {name}")
# chain = LLMChain(llm=llm,prompt=prompt_search,verbose=True,output_key = "title")

# prompt_search2 =PromptTemplate(input_variables=["title"],template="when does {title} born")
# chain2 = LLMChain(llm=llm,prompt=prompt_search2,verbose=True,output_key="dob")

# parent_chain = SimpleSequentialChain(chains=[chain,chain2],verbose=True)


# if text_input:
#     res = parent_chain.run(text_input)
#     # res = llm(text_input)
#     st.write(res)


chat_template = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful doctor. Your name is {name}."),
        ("human", "Hello, how are you doing?"),
        ("ai", "I'm doing well, thanks!"),
        ("human", "{user_input}"),
    ]
)

chat_template_chain = LLMChain(llm=llm,prompt=chat_template,verbose=True)

if text_input:
    res = chat_template_chain.run({"name":"boby","user_input":text_input})
    st.write(res)















# prom = PromptTemplate.from_template("Tell me a {adjective} flirting line about {content}.")
# search_text = prom.format(adjective ="funny",content ="chicken")
# llm =OpenAI(api_key=os.environ.get("KEY"), temperature=0.5)
# print(11111111111111111111111111111111111,search_text)
# print(llm.invoke(search_text))






# repo_id = "google/gemma-7b"
# llm = huggingface_endpoint.HuggingFaceEndpoint(repo_id=repo_id, max_length=128, temperature=0.5, token=os.environ["HUGGINGFACEHUB_API_TOKEN"])
# print(llm.invoke("who is first pm of india"))

