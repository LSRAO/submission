from src.pdf_extractor import extract_text_from_pdf
from src.openai_agent import OpenAIAgent
from dotenv import load_dotenv
from src.slack_client import SlackClient
import json

import nltk
nltk.download("punkt")

import os
load_dotenv()

# Load environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
print(OPENAI_API_KEY)
SLACK_API_TOKEN = os.getenv("SLACK_API_TOKEN")
SLACK_CHANNEL = os.getenv("SLACK_CHANNEL")
PDF_PATH = input("Path to input file:")#os.getenv("PDF_PATH")
# QUESTION = os.getenv("QUESTION")

def main(questions):
    # Extract text from PDF
    
    pdf_text = extract_text_from_pdf(PDF_PATH)
    
    # Create OpenAI agent
    openai_agent = OpenAIAgent(api_key=OPENAI_API_KEY)
    
    # Create Slack client
    slack_client = SlackClient(token=SLACK_API_TOKEN, channel=SLACK_CHANNEL)

    for QUESTION in questions:
        # Ask the question
        answer = openai_agent.ask_question_in_chunks(QUESTION, pdf_text)

        
        # Write in JSON
        with open("res.json", "r+") as f:
            data = json.load(f)
        data.append({"Question": QUESTION, "Answer": answer})

        with open("res.json", "w") as f:
            json.dump(data, f, indent=4)
 
        # Send answer to Slack
        slack_client.send_message(f"Quesion:{QUESTION} \n Answer:{answer}")

if __name__ == "__main__":
    questions = []
    print("Enter your questions. Type 'done' when you are finished.\n")
    
    while True:
        question = input("Enter a question: ")
        if question.lower() == 'done':
            break
        questions.append(question)
    
    main(questions)
