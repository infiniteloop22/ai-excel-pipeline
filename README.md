# AI Excel File Sorter

An intelligent Python script that utilizes a local LLM via **Ollama** and **Pydantic** structured outputs to analyze spreadsheet schemas and automatically sort multiple Excel (`.xlsx`) files based on a natural language request.

## Features
- **Intelligent Sorting:** Dynamically analyzes columns, data types, and sample rows via `llama3.2:1b`.
- **Structured Data Extraction:** Uses Pydantic validation to extract precise, case-normalized sorting columns and generation reasoning.
- **Data Logging:** Logs raw model outputs into a local text file (`model_output.txt`) for reference.

## Technologies Used
- **Language:** Python 3.x
- **Local AI Orchestration:** `ollama` (Running `llama3.2:1b`)
- **Data Libraries:** `pandas`, `pydantic`

## Getting Started

### Prerequisites
- Python 3.8 or higher.
- [Ollama](https://ollama.com) installed on your machine.
- The local Llama model pulled via terminal:
  ```bash
  ollama pull llama3.2:1b
  ```

### Installation & Run
1. Clone the repository:
   ```bash
   git clone https://github.com/infiniteloop22/ai-excel-pipeline
   cd ai-excel-pipeline
   ```
2. Activate your virtual environment (`venv`) through your terminal:
   - **Windows (PowerShell):** `.\.venv\Scripts\Activate.ps1`
   - **macOS / Linux:** `source .venv/bin/activate`
3. Install the required libraries using the requirements file:
   ```bash
   pip install -r requirements.txt
   ```
4. Verify `files.txt` and `prompt.txt` exist in your working directory. Add the relative paths of the Excel spreadsheets you want to sort into `files.txt` (one per line):
   ```text
   example:
   data/inventory.xlsx
   data/sales.xlsx
   ```
5. Run the application from your project root folder:
   ```bash
   python src/script.py
   ```

## Usage
1. Populate your target spreadsheet paths inside `files.txt`.
2. Configure your strategic analyst prompt rules inside `prompt.txt`.
3. Launch the script using the root entry execution command `python src/script.py`. 
4. The backend pipeline compiles your data context, extracts the ideal sorting configuration using the local model, validates parameters against your spreadsheet headers, and writes the sorted outputs back to input file.