# 🧠 Multi-Agent Intelligent Recruitment System

A multi-agent recruitment platform that simulates candidate profiling, adaptive assessment design, behavioral & cultural fit analysis, and market intelligence.  
Built with **Streamlit**, **SQLite3**, and **Python agents** for a fully automated experience.

---

## 🚀 Features

### 1. Candidate Profiler Agent
- Parses and analyzes candidate profiles (synthetic LinkedIn/GitHub-like data).  
- Extracts skills, career progression, and assigns confidence scores.  
- Generates a structured **Talent Intelligence Report**.  

### 2. Adaptive Technical Assessment Designer Agent
- Creates personalized assessments based on candidate profile and target role.  
- Includes:
  - Role-specific coding/system design tasks.  
  - Scoring rubric with weighted criteria.  
  - Bias mitigation protocol for fair evaluation.  

### 3. Behavioral & Cultural Fit Analyzer Agent
- Analyzes candidate responses (simulated interviews / text data).  
- Detects traits: **Teamwork, Problem-Solving, Communication**.  
- Provides sentiment analysis, insights, and evidence.  
- Ensures strict bias avoidance.  

### 4. Market Intelligence & Sourcing Agent
- Fetches real market data (salary benchmarks, hot skills, sourcing channels).  
- Falls back to a static dataset if APIs are unavailable.  
- Helps recruiters target the right roles & sourcing channels.  

---

## 🏗️ System Architecture

```
app/
 ├── streamlit_app.py     # Main app navigation
 └── pages/               # Each feature as a page
       ├── Admin.py
       ├── Profiler.py
       ├── Assessment.py
       ├── Behavioral.py
       └── Market.py

agents/
 ├── profiler.py
 ├── assessment.py
 ├── behavioral.py
 └── market.py

utils/
 ├── db.py                # SQLite3-backed candidate store
 └── generator.py         # Bulk synthetic candidate generator

candidates.db             # Auto-created SQLite database
requirements.txt          # Dependencies
README.md                 # Documentation
```

---

## ⚙️ Setup & Installation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/<your-username>/multiagent-recruitment.git
cd multiagent-recruitment
```

### 2️⃣ Create & Activate Virtual Environment

**Windows**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Run the Application
```bash
streamlit run app/streamlit_app.py
```

---

## 📊 Usage Flow
1. **Admin Panel** → Bulk-generate synthetic candidates or upload data.  
2. **Candidate Profiler** → Generate a Talent Intelligence Report.  
3. **Assessment Designer** → Create adaptive role-based assessments.  
4. **Behavioral Analyzer** → Paste interview responses for analysis.  
5. **Market Intelligence** → Fetch role-based salary, skills, and sourcing insights.  

---

## ⚖️ Bias Mitigation Approach
- Candidate **names, gender, ethnicity, and age are ignored** in profiling and assessments.  
- Evaluation is **output-based only** (code, answers, artifacts).  
- Rubrics enforce **structured scoring with clear weights**.  
- Assessors must provide **justification for scores** → ensures auditability.  
- **Normalization** reduces subjectivity across evaluators.  

---

## 🌟 Future Enhancements (Planned)
- Integration with **real candidate APIs** (LinkedIn, GitHub).  
- Advanced **AI explainability dashboards** for fairness & transparency.  
- **Multi-language support** for international candidate data.  
- Integration with **ATS platforms** for end-to-end recruitment workflows.  

---
