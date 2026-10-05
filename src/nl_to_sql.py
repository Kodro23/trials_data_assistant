#setting environment
from openai import OpenAI
import os
import sys
from pathlib import Path
from src.database import query_db

#seting directory
project_root = Path.cwd().parent
sys.path.append(str(project_root))

#Set the api key in the os
API_KEY=os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"]=API_KEY
client=OpenAI()

#Database schema
with open(str(project_root)+"\\config\\schema.txt", "r") as f:
    schema=str(f.read())

def translate_nl_to_sql(instructions,schema=schema,model="gpt-5.2"):
    """
    LLM translating natural language to SQL queries.
    """
    response=client.responses.create(
        model=model,
        reasoning= {"effort": "low" },
        input=[
          {"role": "developer", "content": "Translate user intructions into SQL queries."},
          {"role": "developer", "content":"Use only the data you are fed and you retrieved. If it's not in the data, you are allowed to say it's not in the data so you cannot answer"},
          {"role": "developer", "content": f"Here is the database schema: {schema}"},
          {"role":"user", "content": instructions},
          {"role":"user", "content": "Return only the executable PostgreSQL query. Do not use Markdown, code fences, backticks, explanations, or introductory text."}
       ] 

    )

    return response.output_text

def retrive_db_from_query(instructions):
    query=translate_nl_to_sql(instructions=instructions)
    results=query_db(query)
    return results


