# trials_data_assistant


<!-- README TOP -->
<a name="readme-top"></a>

# Trials Data Assistant

<!-- Project presentation -->
## 👨‍🏫1. Project presentation
AI agent that use clinical trials data and papers to retrieve information and compute natural language to SQL commands. 

### 1. Data
- The [ClinicalTrials.gov](https://aact.ctti-clinicaltrials.org/) registry provides information regarding characteristics of past, current, and planned clinical studies to patients, clinicians, and researchers; in addition, registry data are available for bulk download. The databse includes 605,592 clinical trials as of 2026 studying conditions like ovarian cancer, Aortic Aneurysm,HIV',Rheumatoid Arthritis, Chronic Periodontitis', etc.
- Collection of 15 scientific papers about ovarian cancer (to complete)


### 2. Method and results
Using models GPT-5 from OpenAI, is built an agent capable of categorizing the user question into "SQL Query" and "Paper search". Then, regarding the predicted task, the agent either query the database or search for the medical answer to the user's question in the stored articles.

### 🧰3. Built with
Python 3.13.13

### 📈4. Improvements
Points of improvement:
- Evaluate and improve agents (benchmark, compare to fine-tuned LLM ) 
- Add more papers to the data and add an hybrid option to user's question (SQL+Paper search)

<!-- User's guide -->
## 📄II. User's guide

- Clone the repository in python environment and go to dir "/trials_data_assistant"
```
cd /trials_data_assistant
```
- In terminal:
    - Create vitual envrionment
    ```
    python -m venv name_of_environment
    ```
    ```
    source  name_of_environment/bin/activate
    ```
     or
    ```
    .\name_of_environment\Scripts\Activate.ps1
    ```
    ```
    pip install -r requirements.txt

    ```
    - To run the API use the command :
    ```
    uvicorn app.api:app --reload --host "0.0.0.0" --port 8000
    ```
    

