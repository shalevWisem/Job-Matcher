# Job Matcher

AI-powered tool that analyzes job descriptions and matches them to the top 5 relevant job codes from your organization's job classification system using Claude AI.

## Overview

Job Matcher helps HR teams and recruiters quickly classify job descriptions by matching them against your organization's standardized job codes. Simply paste a job description, and the tool returns the 5 best matching job titles and codes with AI-generated reasoning.

## Prerequisites

- Python 3.11 or higher
- Pipenv
- Anthropic API key ([get one here](https://console.anthropic.com/))

## Quick Start

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd job-matcher
   ```

2. **Install dependencies**
   ```bash
   pipenv install
   ```

3. **Set up your API key**
   ```bash
   cp .env.example .env
   ```
   Then edit `.env` and add your Anthropic API key:
   ```
   ANTHROPIC_API_KEY=your_actual_api_key_here
   ```

4. **Prepare your job data**
   - Place your job classification Excel file in the `data/` folder
   - Use the same format as `data/sample_data.xlsx`
   - See [Data Format](#data-format) below for details

5. **Run the application**
   ```bash
   pipenv run python main.py
   ```

6. **Open your browser**
   
   Navigate to: http://127.0.0.1:5050

## Usage

1. Open the web interface at http://127.0.0.1:5050
2. Paste a job description into the text area
3. Click "Classify"
4. View the top 5 matching job codes with:
   - Job Title
   - Job Code
   - AI reasoning for each match

## Data Format

Your Excel file should be placed in the `data/` folder and must include these columns:

- `Job Module`
- `Job Code`
- `Job Title`
- `Job Function`
- `Job Area`
- `Job Focus`
- `Job Level`
- `Module Code`
- `Function Code`
- `Area Code`
- `Focus Code`
- `Level Code`
- `Module Definition`
- `Function Definition`
- `Area Definition`
- `Focus Definition`
- `Detailed Definition`

**Note:** The Excel file should use the first sheet. An index column (like "Unnamed: 0") will be automatically handled.

Refer to `data/sample_data.xlsx` for the correct format.

## Project Structure

```
job-matcher/
├── main.py                 # Flask application entry point
├── handlers/               # Internal processing logic
├── llm_calls/             # AI/LLM integration
├── static/                # Web UI (HTML/CSS/JS)
├── data/                  # Your job classification data
│   └── sample_data.xlsx   # Example data format
├── .env                   # Your API keys (create from .env.example)
├── Pipfile                # Python dependencies
└── README.md
```

## Configuration

The application runs on `127.0.0.1:5050` by default. To change this, edit the `app.run()` parameters in `main.py`.

## Troubleshooting

**"ANTHROPIC_API_KEY not found"**
- Make sure you created `.env` from `.env.example`
- Verify your API key is correct

**"No data file found"**
- Ensure your Excel file is in the `data/` folder
- Check that it matches the format in `sample_data.xlsx`

**Dependencies issues**
- Make sure you're using Python 3.11+: `python --version`
- Try removing and reinstalling: `pipenv --rm && pipenv install`

## License

[Add your license here - e.g., MIT, Apache 2.0]

## Support

For issues or questions, please open an issue on GitHub.
