from langchain_huggingface import HuggingFaceEmbeddings,HuggingFaceEndpoint,ChatHuggingFace
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain
from dotenv import load_dotenv
from langchain.memory import ConversationBufferMemory
import os 

load_dotenv()

#document loader
class RagPipiline():
    
    def __init__(self):
    
    #Document loader

        urls=["https://huyenchip.com/2024/07/25/genai-platform.html",
            "https://lilianweng.github.io/posts/2024-07-07-hallucinatio",
            "https://jina.ai/news/what-is-colbert-and-late-interaction-and-why-they-matter-in-search/",
            "https://quoraengineering.quora.com/Building-Embedding-Search-at-Quora"]
    
        docs=[]
        for url in urls:
            loader=WebBaseLoader(url)
            docs.extend(loader.load())
            
        #text splitter
        text_splitter=RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=250
        )
        chunks=text_splitter.split_documents(docs)
        
        #embedding
        embedding=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        
        #vector_store
        vector_store=Chroma.from_documents(
            embedding=embedding,
            documents=chunks,
            collection_name="my_collection"
        )
        #memory
        memory=ConversationBufferMemory(memory_key="chat_history",return_messages=True,output_key="answer")
        
        #retriever
        retriever=vector_store.as_retriever(search_kwargs={"k":2},search_type='similarity')
        
        #model
        llm1=HuggingFaceEndpoint(repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1",task="text-generation",model_kwargs={"api_key":os.getenv("HUGGINGFACE_API_TOKEN")},temperature=0.5,max_new_tokens=512)
        model=ChatHuggingFace(llm=llm1)
        
        self.retriever_qa=ConversationalRetrievalChain.from_llm(
           llm=model,
           retriever=retriever,
           memory=memory,
           return_source_documents=True,
           output_key="answer"
        )
        
    
    def ask(self,query:str):
        result=self.retriever_qa.invoke(query)
        return result["answer"]
       
    

