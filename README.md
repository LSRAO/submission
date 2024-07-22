# Zania AI Challenge

## Overview
This project aims to create an AI agent that leverages the capabilities of a large language model. The agent can extract answers based on the content of a large PDF document and post the results on Slack using OpenAI's GPT-3.5-turbo model.

## Features
- Extracts text from a PDF document.
- Splits the document text into manageable chunks.
- Uses OpenAI's GPT-3.5-turbo to answer questions based on the document content.
- Posts answers to a specified Slack channel.
- Returns structured JSON output with questions and corresponding answers.

## Technologies Used
- Python
- OpenAI GPT-3.5-turbo
- PyPDF2
- Slack SDK
- Python-dotenv

## Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)
- Git

### Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/LSRAO/submission.git
   cd submission
   ```
2. Create a Virtual Environment and activate it:
   ```sh
   python -m venv .venv
   source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
   ```
3. Install the required packages:
   ```sh
   pip install -r requirements.txt
   ```
4. Set up environment variables.
   Create a .env file in the root directory of the project and add the following:
   ```sh
   OPENAI_API_KEY=your-open-api-key
   SLACK_API_TOKEN=your-slack-api-key
   SLACK_CHANNEL=slack-channel-the-app-is-integrated-with
   ```
   
### Usage

1. Ensure your virtual environment is activated:
   ```sh
   source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
   ```
2. Run the main script:
   ```sh
   python src/main.py
   ```

### Example

To answer the question "What is the name of the company?" based on the content of handbook.pdf, run:

```sh
python main.py
```

Enter the File Path for the PDF, followed by the question that needs to be answered.
Output will be An updated JSON file with 

### Project Structure
```plaintext
submission/
│
├── data/
│   └── handbook.pdf
│
├── src/
│   ├── __init__.py
│   ├── pdf_extractor.py
│   ├── openai_agent.py
│   └── slack_client.py
│
├── .env
├── .gitignore
├── requirements.txt
├── README.md
└── main.py
```

## Enhancements

### Accuracy Improvements

* Fine-tune the OpenAI model with domain-specific data.
* Implement advanced text preprocessing techniques.
* Use a more sophisticated chunking strategy that considers context boundaries.
  
###Code Quality Improvements

* Modularize the code further by separating concerns into different modules.
* Implement logging for better debugging and monitoring.
* Add more extensive error handling and input validation.

### Contact

If you have any questions/suggestions, feel free to reach out to me at lsr22299@gmail.com.
