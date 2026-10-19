from report_generator.predict_file import predict_delay
from LLM.llm import llm
from LLM.system_prompt import SYSTEM_PROMPT
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from rich import print

prompt = ChatPromptTemplate.from_template(SYSTEM_PROMPT)

structure_output = StrOutputParser()

def main(csv_path):

    try:

        # print("Reading CSV...")
        context = predict_delay(csv_path)

        # print("Creating Chain...")
        chain = prompt | llm | structure_output

        # print("Calling LLM...")
        response = chain.invoke({"context":context})

        # print("Generate Response...")
        # if response:
        #     print(response)
        # else:
        #     print("Response is Null.")

        return response

    except Exception as e:
        raise f"Error : {e}"