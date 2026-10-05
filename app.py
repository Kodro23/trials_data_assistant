#Load packages
import streamlit as st
from src.app_agent import ask_agent

#Set page configuration
st.set_page_config(
  page_title="Trials Data Assistant",
  page_icon="🔬"
)

#Set title
st.title("Trials Data Assistant")

#Set description
st.write(
  "Ask questions about clinical trials "
  "or information from scientific papers."
)

#Get the user's question
question=st.chat_input("Ask a question")

#Check if the user asked a question
if question:
  #Display the user's question
  with st.chat_message("user"):
    st.write(question)

  #Call the agent
  with st.spinner("Searching..."):
    result=ask_agent(question)

  #Get the final answer
  answer=result["final_answer"]

  #Get the source used by the agent
  if result["query"] == "True":
    source="Clinical Trials Database"
  else:
    source="Scientific Papers"

  #Display the agent's answer
  with st.chat_message("assistant"):
    st.write(answer)
    st.caption("Source: "+source)