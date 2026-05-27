from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()


prompt_template = """
Answer the question as detailed as possible from the provided context.
If the answer is not in the context, say:
'Answer is not available in the context.'

Context:\n {context}\n
Question:\n {question}\n
Answer:
"""

def get_conversational_chain():

    model = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0.3
    )

    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "question"]
    )

    chain = load_qa_chain(
        model,
        chain_type="stuff",
        prompt=prompt
    )

    return chain