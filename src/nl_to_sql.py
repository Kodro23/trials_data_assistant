#Load packages
from openai import OpenAI
import os
import sys
from pathlib import Path
from src.database import query_db
from dotenv import load_dotenv



#seting directory
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))
load_dotenv()
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
    Args:
        instructions (str): Natural language instructions for the SQL query.
        schema (str): Database schema to guide the translation.
        model (str): LLM model to use for translation.
    """
    try:
        response=client.responses.create(
            model=model,
            reasoning= {"effort": "high" },
            input=[
              {"role": "developer", "content": "Translate user intructions into SQL queries."},
              {"role": "developer", "content":"Use only the data you are fed and you retrieved. If it's not in the data, you are allowed to say it's not in the data so you cannot answer"},
              {"role": "developer", "content": f"Here is the database schema: {schema}"},
              {"role":"user", "content": instructions},
             {"role":"user", "content": "Return only the executable PostgreSQL query. Do not use Markdown, code fences, backticks, explanations, or introductory text."}
         ] 

    )
    except Exception as e:
        print(f"Error translating instructions to SQL: {e}")
        return None

    return response.output_text

def retrive_db_from_query(instructions):
    """
    Use generated SQL query to interrogate the database
    Args:
        instructions (str): Natural language instructions for the SQL query.
    """
    try:
        query=translate_nl_to_sql(instructions=instructions)
        print(f"Generated SQL query: {query}")
        results=query_db(query)
        return results

    except Exception as e:
        print(f"Error retrieving data from database: {e}")
        return None



