# AI Lab Report Assistant

An AI-powered web app that converts raw experimental data and observations into a complete, structured academic lab report — built with Flask and Claude API.

---

## Features

- Generates a full 12-section IEEE-style lab report from raw input
- Real-time streaming output (report appears as it's being written)
- Dynamic data table with add/remove rows and columns
- Automatic error analysis and percentage error calculation
- Methodology improvement suggestions
- Export report as `.md` file
- Copy to clipboard

---

## Tech Stack

- **Backend:** Python, Flask
- **Frontend:** HTML, CSS, JavaScript
- **AI:** Anthropic Claude API (claude-sonnet-4-20250514)

---

## Project Structure

```
lab-report-assistant/
├── app.py
├── templates/
│   └── index.html
├── requirements.txt
├── .env.example
├── .env
└── .gitignore
```

---

## Setup & Installation

**1. Clone the repository**
```bash
git clone https://github.com/your-username/lab-report-assistant.git
cd lab-report-assistant
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Set up environment variables**
```bash
copy .env.example .env
```
Open `.env` and paste your Anthropic API key:
```
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxxxxx
```
Get your key from [console.anthropic.com](https://console.anthropic.com)

**4. Run the app**
```bash
python app.py
```

**5. Open in browser**
```
http://localhost:5000
```

---

## How to Use

1. Enter your experiment title and objective
2. Fill in apparatus, procedure, and observations
3. Enter your experimental data in the table
4. Add theoretical values for error analysis (optional)
5. Click **Generate Lab Report**
6. Copy or export the generated report

---

## Report Sections Generated

1. Abstract
2. Introduction
3. Theory & Governing Equations
4. Apparatus & Materials
5. Experimental Procedure
6. Observations & Raw Data
7. Data Analysis & Calculations
8. Results
9. Discussion
10. Conclusion
11. Methodology Improvements
12. Safety & Precautions
13. References

---

## Author

**Mehul Pramanik**

---

## License

MIT
