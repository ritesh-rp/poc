from langchain.output_parsers import PydanticOutputParser, CommaSeparatedListOutputParser
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.prompts import PromptTemplate
from langchain.chains.llm import LLMChain
from langchain_openai import OpenAI


class Player(BaseModel):
    age : int = Field()
    total_matches_played :int =  Field()
    place_of_birth :str =  Field()
    description :str =  Field()


# parser = PydanticOutputParser(pydantic_object=Player)

# parser = JsonOutputParser()

parser = CommaSeparatedListOutputParser()

query ="give the details of the {format_instruction} of {player}"

prompt = PromptTemplate(template = query, input_variables=["player"],partial_variables={"format_instruction":parser.get_format_instructions})
model = OpenAI()
chain = LLMChain(llm=model,prompt=prompt)
res = chain.invoke({"player" : "ms dhoni"})
print(111111111111111111111111111,res)