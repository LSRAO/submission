from openai import OpenAI

import nltk

class OpenAIAgent:
    def __init__(self, api_key):
        self.client = OpenAI(
            # This is the default and can be omitted
            api_key=api_key
        )

    def ask_question(self, question, context):

        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Context: {context}"},
                {"role": "user", "content": f"Question: {question}"},
                {"role": "system", "content": "Answer: "}
            ],
            max_tokens=100,
            temperature=0.9,
            top_p=0.7

        )
        response_message = response.choices[0].message.content
        # print(response_message)
        return response_message

    # def ask_question_in_chunks(self, question, context, chunk_size=512):
    #     chunks = [context[i:i + chunk_size] for i in range(0, len(context), chunk_size)]
    #     responses = []
    #     for chunk in chunks:
    #         response = self.ask_question(question, chunk)
    #         responses.append(response)

    #     return "".join(min(responses, key=responses.count))
    def chunk_text(self, text, max_chunk_size=512, overlap=10):
        sentences = nltk.sent_tokenize(text)
        chunks = []
        current_chunk = ""
        for sentence in sentences:
            if len(current_chunk) + len(sentence) <= max_chunk_size:
                current_chunk += " " + sentence
            else:
                chunks.append(current_chunk)
                current_chunk = sentence
        if current_chunk:
            chunks.append(current_chunk)
        # Add overlap to maintain context
        
        overlapped_chunks = []
        for i in range(len(chunks)):
            start = max(0, i - overlap)
            end = min(len(chunks), i + overlap + 1)
            overlapped_chunks.append(" ".join(chunks[start:end]))
        # print(len(overlapped_chunks[-1]))
        return overlapped_chunks

    def extract_keywords(self, prompt):
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=[{"role": "system", "content":f"Extract the keywords from the following prompt\n\n{prompt}"}],
            max_tokens=100,
            temperature=0.9,
            top_p=0.7
            )
        return response.choices[0].message.content.strip().split(' ')

    def find_relevant_chunks(self, chunks, keywords):
        relevant_chunks = []
        for chunk in chunks:
            if any(keyword in chunk for keyword in keywords[0]):
                relevant_chunks.append(chunk)
        return relevant_chunks

    def query_model_for_chunks(self, prompt, chunks):
        answers = []
        for chunk in chunks:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo-0125",
                messages=[{"role": "user", "content": f"Context: {chunk}"},
                          {"role": "user", "content": f"Queston: {prompt}"},
                          {"role": "system", "content": "Answer: "}],
                max_tokens=100,
                temperature=0.9,
                top_p=0.7
            )
            answers.append(response.choices[0].message.content.strip())
        return answers
    def select_best_response(self, question, responses):
        best_response = None
        highest_relevance_score = 0

        for response in responses:
            relevance_score = self.evaluate_relevance(question, response)
            if relevance_score > highest_relevance_score:
                best_response = response
                highest_relevance_score = relevance_score

        if highest_relevance_score < 0.5:  # Set a threshold for relevance
            return "Data Not Available"
        return best_response
    
    def evaluate_relevance(self, question, response):
        relevance_prompt = f"Evaluate the relevance of the following response to the question. Score between 0 and 1.\n\nQuestion: {question}\n\nResponse: {response}\n\nRelevance score:"
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=[{"role": "user", "content": f"Context: {relevance_prompt}"}],
            max_tokens=10
        )
        try:
            relevance_score = float(response.choices[0].message.content.strip())
        except ValueError:
            relevance_score = 0
        return relevance_score

    def ask_question_in_chunks(self, question, text):
        # text = extract_text_from_pdf(pdf_path)
        chunks = self.chunk_text(text)
        keywords = self.extract_keywords(question)
        relevant_chunks = self.find_relevant_chunks(chunks, keywords)
        responses = self.query_model_for_chunks(question, relevant_chunks)
        final_answer = self.select_best_response(question, responses)
        return final_answer
