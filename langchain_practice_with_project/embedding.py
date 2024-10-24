from langchain_openai import OpenAIEmbeddings

embedding = OpenAIEmbeddings()

embedded_data = embedding.embed_documents(
    [
        "Hi there!",
        "Oh, hello!",
        "What's your name?",
        "My friends call me World",
        "Hello World!"
    ]
)
print(len(embedded_data),embedded_data)