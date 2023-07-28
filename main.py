from langchain.document_loaders import UnstructuredPDFLoader, OnlinePDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma, Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
import pinecone
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
import openai 
import os

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
PINECONE_API_ENV = os.getenv('PINECONE_API_ENV')

#initialize our pinecone index
pinecone.init(
    api_key=PINECONE_API_KEY,  # find at app.pinecone.io
    environment=PINECONE_API_ENV  # next to api key in console
)
index_name = "fast-and-slow"   

hasIndex = pinecone.list_indexes()
if not hasIndex:
    pinecone.create_index(index_name, dimension=1536, metric="cosine", pod_type="p1")
elif hasIndex[0] != index_name:
    pinecone.delete_index(hasIndex[0])
    #we use dimension 1536 because thats what openai uses
    pinecone.create_index(index_name, dimension=1536, metric="cosine", pod_type="p1")

index = pinecone.Index(index_name)
hasValues = index.describe_index_stats()
    
#initialize our embeddings and openai related things
embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
openai.api_key = OPENAI_API_KEY

#initialize our chain
llm = OpenAI(model_name='text-davinci-003', temperature=0, openai_api_key=OPENAI_API_KEY)
chain = load_qa_chain(llm, chain_type="stuff")


#read the pdf and load it into pineocne if it hasnt been loaded yet
if hasValues['total_vector_count'] < 1:   
    loader = UnstructuredPDFLoader("./assets/fast_and_slow.pdf")
    data = loader.load()
    #split up the pdf because openai has limits
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(data)

    #this one line does so many things. I should revisit to fully understand it
    docsearch = Pinecone.from_texts([t.page_content for t in texts], embeddings, index_name=index_name)
else:
    docsearch = Pinecone.from_existing_index(index_name, embeddings)

query = "What is the difference between system 1 and system 2?"
docs = docsearch.similarity_search(query, include_metadata=True)
finalResponse = chain.run(input_documents=docs, question=query)

print('\n\n\n' + finalResponse + '\n\n\n')