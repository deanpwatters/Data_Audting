# ============================================================
# STEP 2 - IMPORT REQUIRED LIBRARIES
# ============================================================

import json
from openai import OpenAI
from dotenv import load_dotenv

# ============================================================
# STEP 3 - LOAD ENVIRONMENT VARIABLES
# ============================================================
# Loads the API key from the .env file.
#
# Example .env file:
#
# OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# ============================================================

load_dotenv()

# ============================================================
# STEP 4 - INITIALISE THE OPENAI CLIENT
# ============================================================
# The API key is automatically loaded from the environment.
# ============================================================

client = OpenAI()

# ============================================================
# STEP 5 - CONVERT AUDIT RESULTS TO JSON
# ============================================================
# The LLM receives a structured JSON summary rather than the
# entire dataset. This keeps token usage low and ensures the
# model only interprets validated audit findings.
# ============================================================

audit_json = json.dumps(
    audit_results,
    indent=4,
    default=str
)

# ============================================================
# STEP 6 - CREATE THE LLM PROMPT
# ============================================================
# Provide clear instructions to the model.
# The model should only discuss findings present in the audit.
# ============================================================

prompt = f"""
You are a Senior Data Quality Consultant.

Below is the output from an automated data quality audit.

{audit_json}

Produce a professional report with the following sections.

1. Executive Summary

2. Key Data Quality Findings

3. Business Risks

4. Recommendations

5. Suggested Next Steps

Instructions

- Do NOT invent statistics.
- Only discuss findings contained within the audit.
- Write for business stakeholders.
- Explain technical findings in simple language.
- Use UK English.
"""

# ============================================================
# STEP 7 - SEND THE AUDIT TO GPT-5.5
# ============================================================
# The Responses API is used to generate a business report.
# ============================================================

response = client.responses.create(
    model="gpt-5.5",
    input=prompt
)

# Store the generated report

llm_report = response.output_text

# ============================================================
# STEP 8 - SAVE THE EXECUTIVE REPORT
# ============================================================
# Saves the generated report to a text file.
# This can later be upgraded to Word or PDF.
# ============================================================

REPORT_FILE = "Executive_Report.txt"

with open(
    REPORT_FILE,
    "w",
    encoding="utf-8"
) as file:

    file.write(llm_report)

# ============================================================
# STEP 9 - DISPLAY THE REPORT
# ============================================================
# Prints the report to the console and confirms completion.
# ============================================================

print("\n" + "=" * 60)
print("AI EXECUTIVE DATA AUDIT REPORT")
print("=" * 60)

print(llm_report)

print("\n" + "=" * 60)
print(f"Executive report successfully saved to: {REPORT_FILE}")
print("=" * 60)
