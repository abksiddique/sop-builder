\# SOP Builder



An AI-powered Standard Operating Procedure generator built as a capstone project for the \*\*AI for SOPs and Process Documentation\*\* course at the University of Cincinnati.



\## Authors

\- \*\*Siddique Abubakr Muntaka\*\*

\- \*\*Dogbe, Abigail\*\*



\*\*Course:\*\* AI for SOPs and Process Documentation

\*\*School:\*\* School of Information Technology, University of Cincinnati

\*\*Professor:\*\* Dr. Michael Zidar



\---



\## What It Does



SOP Builder takes a process description as input and generates:



\- A complete, structured SOP document (Purpose, Scope, Roles, Procedure, Exceptions, Governance, Improvement Recommendation)

\- An interactive process flow diagram rendered in the browser

\- Downloadable outputs: PDF, Markdown, BPMN XML, PNG diagram



\## AI Stack



\- \*\*Primary:\*\* Google Gemini 1.5 Flash (free tier)

\- \*\*Fallback:\*\* Groq Llama 3.3 70B (free tier)

\- Both APIs are called directly over HTTP — no SDK dependencies



\## Tech Stack



\- \*\*Backend:\*\* Python 3 + Flask

\- \*\*Database:\*\* SQLite via Flask-SQLAlchemy

\- \*\*Diagrams:\*\* Mermaid.js (browser rendering)

\- \*\*Frontend:\*\* HTML5 + CSS3 + Vanilla JavaScript

\- \*\*Deployment:\*\* Gunicorn + Nginx



\---



\## Local Setup



\### 1. Clone the repository



```bash

git clone https://github.com/abksiddique/sop-builder.git

cd sop-builder

```



\### 2. Create virtual environment



```bash

python -m venv venv

source venv/Scripts/activate  # Windows

source venv/bin/activate       # Linux/Mac

```



\### 3. Install dependencies



```bash

pip install -r requirements.txt

```



\### 4. Configure environment variables



```bash

cp .env.example .env

```



Edit `.env` and add your API keys:



Get free API keys:

\- Gemini: https://aistudio.google.com

\- Groq: https://console.groq.com



\### 5. Run the application



```bash

python run.py

```



Visit `http://127.0.0.1:5000`



\---



\## How to Use



1\. Enter a process name and description

2\. Optionally add roles and known exceptions

3\. Click \*\*Generate SOP + BPMN Diagram\*\*

4\. View the generated SOP document

5\. Click \*\*Process Diagram\*\* tab to see the flowchart

6\. Export as PDF, Markdown, PNG, or BPMN XML

7\. All generated SOPs are saved in History



\---



\## Project Structure



\---



\## Deployment



The live application is hosted at:

\*\*https://sopbuilder.muntworld.com\*\*



Deployed on VPS using Gunicorn + Nginx.





