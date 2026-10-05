##Load packages
from openai import OpenAI
import os
import sys
from pathlib import Path
from dotenv import load_dotenv



#seting directory
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))
load_dotenv()
#set_up
docs_directory=str(project_root)+"\\data\\scientific_papers"
supported_extensions=[".txt",".py",".pdf"]
API_KEY=os.getenv("OPENAI_API_KEY")
VECTOR_STORE_ID=os.getenv("VECTOR_STORE_ID")
os.environ["OPENAI_API_KEY"]=API_KEY
os.environ["VECTOR_STORE_ID"]=VECTOR_STORE_ID
client=OpenAI()

# # File paths
# files_path=[]
# for file in os.listdir(docs_directory):
#   file_path=os.path.join(docs_directory, file)
#   if os.path.isfile(file_path):
#     file_extension=os.path.splitext(file_path)[1].lower()
#     if file_extension in supported_extensions:
#       files_path.append(file_path)

# #upload files to openai
# file_ids=[]
# for file_path in files_path:
#   with open(file_path, "rb") as file:
#     response=client.files.create(
#         file=file,
#         purpose="assistants"
#     )
#     file_ids.append(response.id)

# #creating a vector store
# vector_store=client.vector_stores.create(name="read_papers")

# #add files to the vector store
# for file_id in file_ids:    
#   results=client.vector_stores.files.create(
#     vector_store_id=vector_store.id,
#     file_id=file_id
#   )

# #save vector store id
# vector_store_id=vector_store.id


def read_papers(question,model="gpt-5.2"):
  """
  Read a question by the user and answer based on stored scientific articles
    Args:
        question (str): The question to be answered based on the scientific articles.
        model (str): LLM model to use for answering the question.
  """
  try:
    # Call the API
    response=client.responses.create(
      model=model,
      input=question,
      tools=[{"type":"file_search","vector_store_ids":[VECTOR_STORE_ID],"max_num_results":20} ],
      include=["file_search_call.results"],
      instructions="Only answer based on the information retrieved. Say you don't know if you don't know")   
    return response.output_text
  except Exception as e:
    print(f"An error occurred: {e}")
    return None