#Load packages
import os
import sys
from pathlib import Path
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, END
from src.nl_to_sql import retrive_db_from_query
from src.scientific_paper_rag import read_papers

#seting directory
project_root = Path.cwd().parent
sys.path.append(str(project_root))

#Set the api key in the os
API_KEY=os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"]=API_KEY

# Set the model
MODEL = "gpt-5-nano"


# Define the TypedDict to store the agent's state
class AgentState(TypedDict):
  start: bool
  conversation: int #conversation turns
  question: str # customer's questions
  query: str # True if SQL query, False if paper search
  sql_query: str # sql query to be executed
  sql_answer: str # answer to the question from the database
  rag_answer: str # answer to the question from the papers
  recursion_limit: int # limits endless loops
  memory: list # conversation history
  continue_chat: bool


# Define the greeting node
def greetings(state):
  # greet the customer
  print("Hello! How can I help you?")
  # capture the user input
  user_input = input()
  # Update the state
  state['question'] = user_input
  state['conversation'] = 1
  state['memory'] = [user_input]
  return state


# Define function to check if the question needs a SQL query
def check_if_query(state):
  # Get the customer's question from state
  question = state['question']
  memory = state['memory']
  # Define the system prompt
  system_prompt = """
    You are a grader evaluating the category of the user's question.
    Assess if the question should be answered using the clinical trials
    database or using the stored scientific papers.
    Respond with "True" if the question needs information from the clinical
    trials database. This includes questions about clinical trials, number of
    trials, trial phases, recruitment status, interventions, enrollment,
    sponsors or study dates.
    Respond with "False" if the question asks about scientific evidence,
    research findings, interpretation, mechanisms, conclusions or information
    that should be retrieved from scientific papers.
    Provide only "True" or "False" in your response.
    """
  # Create the prompt template
  TEMPLATE = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "Customer question: {question},\nConversation History:{memory}"),
  ])
  # format the prompt
  prompt = TEMPLATE.format(memory=memory,question=question)
  # Initialize the LLM
  model = ChatOpenAI(api_key=API_KEY,model=MODEL)
  # Invoke the answer
  response_text = model.invoke(prompt)
  # Update the state
  state['query'] = response_text.content.strip()
  return state


# Function to route the question
def topic_router(state):
  query = state['query']
  if query == "True":
    return "SQL_query"
  else:
    return "paper_search"


# Define the SQL node
def SQL_query(state):
  # Get the customer's question
  question = state['question']
  # Retrieve the answer from the database
  answer = retrive_db_from_query(question)
  # Update the state
  state['sql_answer'] = answer
  # Print the answer
  print(answer)
  return state


# Define the paper search node
def paper_search(state):
  # Get the customer's question
  question = state['question']
  # Retrieve the answer from the scientific papers
  answer = read_papers(question)
  # Update the state
  state['rag_answer'] = answer
  # Print the answer
  print(answer)
  return state


# Define function to figure out if we need another conversation round
def further_question(state):
  print("Ask another question or type 'exit' to stop:")
  user_input = input()
  # simple exit condition
  if user_input.lower() in ["exit", "no", "thanks", "that's all", "thank you"]:
    state['continue_chat'] = False
  else:
    # update the conversation memory
    state['memory'].append(user_input)
    state['conversation'] += 1
    state['question'] = user_input
    state['continue_chat'] = True
  return state


# define a conditional router
def continue_router(state):
  if state['continue_chat']:
    return "continue"
  return "end"


def build_agent():
  # Initialize the agent's state
  initial_state = AgentState(
    start=True,
    conversation=0,
    question="",
    query="",
    sql_query="",
    sql_answer="",
    rag_answer="",
    recursion_limit=5,
    memory=[],
    continue_chat=True
  )
  # Initialize a StateGraph
  workflow = StateGraph(AgentState)
  # Add the functions as nodes
  workflow.add_node("greetings", greetings)
  workflow.add_node("check_if_query", check_if_query)
  workflow.add_node("SQL_query", SQL_query)
  workflow.add_node("paper_search", paper_search)
  workflow.add_node("further_question", further_question)
  # Add an entry point
  workflow.set_entry_point("greetings")
  # Connecting the nodes (edges)
  workflow.add_edge("greetings", "check_if_query")
  workflow.add_edge("SQL_query", "further_question")
  workflow.add_edge("paper_search", "further_question")
  # Conditional edges
  workflow.add_conditional_edges(
    "check_if_query",
    topic_router,
    {
      "SQL_query": "SQL_query",
      "paper_search": "paper_search"
    }
  )
  workflow.add_conditional_edges(
    "further_question",
    continue_router,
    {
      "continue": "check_if_query",
      "end": END
    }
  )
  # Compile the workflow
  app = workflow.compile()
  return app