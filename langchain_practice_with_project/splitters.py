from langchain_text_splitters import HTMLHeaderTextSplitter ,CharacterTextSplitter, RecursiveCharacterTextSplitter

# url = "demo.html"
# html_split = HTMLHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
# splitted_text =html_split.split_text_from_file("demo.html")
# print(splitted_text)


############################# CharacterTextSplitter #######################

text = """<div class="w3-col m6 w3-padding-large">
      <h1 class="w3-center">About Catering</h1><br>
      <h5 class="w3-center">Tradition since 1889</h5>
      <p class="w3-large">The Catering was founded in blabla by Mr. Smith in lorem ipsum dolor sit amet, consectetur adipiscing elit consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute iruredolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.We only use <span class="w3-tag w3-light-grey">seasonal</span> ingredients.</p>
      <p class="w3-large w3-text-grey w3-hide-medium">Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum consectetur adipiscing elit, sed do eiusmod temporincididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</p>
    </div>"""

splitter = RecursiveCharacterTextSplitter(separators=[""],
                                chunk_size=10,
                                chunk_overlap=0,
                                length_function=len,
                                is_separator_regex=False,)
# print(text)
splitted_text =splitter.split_text(text)
print(11111111111111111111111111111111111111,splitted_text[0])