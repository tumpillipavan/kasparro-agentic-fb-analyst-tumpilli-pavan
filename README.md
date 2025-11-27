# Kasparro — Agentic Facebook Performance Analyst (Runnable)

Project created at: C:\Users\HP\OneDrive\Desktop\fb_project\kasparro-agentic-fb-analyst-tumpilli-pavan

Quick start:

1. Create & activate a venv:
   ```bash
   python -m venv .venv
   source .venv/bin/activate   
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. (Optional) Enable LLM calls:
   - Set OPENAI_API_KEY in your environment or a .env file
   - In config/config.yaml change model.use_llm to true

4. Run analysis:
   ```bash
   python src/run.py "Analyze ROAS drop in last 7 days"
   ```

Outputs: `reports/insights.json`, `reports/creatives.json`, `reports/report.md`
