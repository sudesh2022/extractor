import pandas as pd
import csv

from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
from langchain.document_loaders import TextLoader
from langchain.document_loaders import DirectoryLoader
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.document_loaders import OnlinePDFLoader, UnstructuredPDFLoader, PyPDFLoader
from langchain.text_splitter import TokenTextSplitter
from langchain.memory import ConversationBufferMemory
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.llms import OpenAI
from langchain.chains import ConversationalRetrievalChain
from pypdf import PdfReader
import os
import chromadb
from dotenv import load_dotenv
from ibm_watson_machine_learning.metanames import GenTextParamsMetaNames as GenParams
from ibm_watson_machine_learning.foundation_models.utils.enums import DecodingMethods
from ibm_watson_machine_learning.foundation_models import Model
from ibm_watson_machine_learning.foundation_models.utils.enums import ModelTypes
from ibm_watson_machine_learning.foundation_models.extensions.langchain import WatsonxLLM
from langchain.chains import RetrievalQA
#from genai.extensions.langchain import LangChainInterface
#from genai.schemas import GenerateParams
# from genai.credentials import Credentials
import pandas as pd
import csv


# Replace 'example.csv' with the actual path to your CSF file
file_path = './outputfiles/sentence_split.csv'

# Initialize empty lists to store data from each column
audit_areas = []
keywords = []
sentences = []

def addtoDataframe(questions,answers,source_documents,keywords):
# Create a DataFrame (for example)
    data = {'questions': questions,'answers': answers,'keywords': keywords,'source_of_truth':source_documents}
    df = pd.DataFrame(data)
    df.to_csv('./answers/data.csv', index=False)



def readData():
# Open the CSV file and read its content
    with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
    # Create a CSV reader object
        csv_reader = csv.reader(csvfile)
    # Skip the header row if it contains column names
        next(csv_reader)
    # Iterate over each row in the CSV file
        for row in csv_reader:
        # Assuming the columns are in the order: Audit Areas, Keywords, Sentences
            audit_areas.append(row[0])
            keywords.append(row[1])
            sentences.append(row[2])

question_array = []
def getQuestions():
    csv_file_path = 'questions.csv'
    question_array = []
    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
         question_array.append(row)
    #print(question_array)
    return question_array

def init_llm():
    global llm_hub, embedding,model
    load_dotenv()
    params = {
        GenParams.DECODING_METHOD: DecodingMethods.GREEDY,
        GenParams.MIN_NEW_TOKENS: 1,
        GenParams.MAX_NEW_TOKENS: 500
    }
    project_id = os.getenv('IBM_PROJECT_ID')
    model_id = os.getenv('GRANITE_2')
    credentials = {"url": os.getenv('IBM_CLOUD_URL'),
                   "apikey": os.getenv('IBM_CLOUD_API')}
    
    model = Model(
        model_id= model_id,
        credentials=credentials,
        params=params,
        project_id=os.getenv("IBM_PROJECT_ID"))
    
    llm_hub = WatsonxLLM(model=model)
    embedding = HuggingFaceEmbeddings()


def predictAnswers():
    i=0
    outputResults=[]
    for question in audit_areas:
        prompt_input="Please answer the question based on provided information. Answer in full sentences  " + sentences[i]
        prompt = prompt_input+question
        generated_response = model.generate_text(prompt)
        outputResults.append(generated_response)
        i=i+1
    data = list(zip(audit_areas,keywords, outputResults, sentences))
    
    csv_file_name = './answers/data.csv'
    with open(csv_file_name, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Question','keywords', 'Answer', 'Proof'])
        csv_writer.writerows(data)
    print(f"CSV file '{csv_file_name}' has been created.")



def main():
    readData()
    init_llm()
    predictAnswers()

if __name__ == "__main__":
    main()
