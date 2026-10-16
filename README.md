# Trials Data Assistant
<!-- README TOP -->
<a name="readme-top"></a>

<!-- Project presentation -->
## 👨‍🏫1. Project presentation
AI agent that use clinical trials data and papers to retrieve information and compute natural language to SQL commands.
For storage reason, the [assistant](https://trialsdataassistant-4hha9jjtevoas93subvnnq.streamlit.app/)'s database is limited to ovarian cancer.


### 1. Data
- The [ClinicalTrials.gov](https://aact.ctti-clinicaltrials.org/) registry provides information regarding characteristics of past, current, and planned clinical studies to patients, clinicians, and researchers; in addition, registry data are available for bulk download. The databse includes 605,592 clinical trials as of 2026 studying conditions like ovarian cancer, Aortic Aneurysm,HIV',Rheumatoid Arthritis, Chronic Periodontitis', etc.
- Collection of 15 scientific papers about ovarian cancer (to complete)


### 2. Method and results
Using models GPT-5 from OpenAI, is built an agent capable of categorizing the user question into "SQL Query" (ex: Give me 5 trials names about ovarian cancer) or "Paper search" (ex: What are 3 biomarkers used to evaluate treatment effect in ovarian cancer?). Then, regarding the predicted task, the agent either query the database or search for the medical answer to the user's question in the stored articles.

### 🧰3. Built with
Python 3.13.13

### 📈4. Improvements
Points of improvement:
- Evaluate and improve agents (benchmark, compare to fine-tuned LLM ) 
- Add more papers to the data and add an hybrid option to user's question (SQL+Paper search)
- Improve displaying of answers in the app


  <img width="460" height="337" alt="image" src="https://github.com/user-attachments/assets/6d564ab1-7505-4eae-b256-ed63966dc578" />
  <img width="500" height="602" alt="02" src="https://github.com/user-attachments/assets/1b3b5989-249c-4aca-a944-6db7067aa307" />

    

