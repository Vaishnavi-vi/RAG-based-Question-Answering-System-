from fastapi import FastAPI,Depends
from pydantic import BaseModel,Field
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from  web import RagPipiline
from typing import Annotated

#--------API key---------
API_key="mysecretkey123"
def get_api_key(api_key:str):
    if api_key!=API_key:
        raise HTTPException(status_code=401,detail="Invalid api_key")
    return api_key

app=FastAPI()
rag=RagPipiline()

class user_input(BaseModel):
    Question:Annotated[str,Field(...,description="Enter your Query")]
    
@app.get("/")
def view():
    return {"message":"This is about Rag Application"}

@app.post("/ask")
def query(query:user_input,api_key:str=Depends(get_api_key)):
    response=rag.ask(query.Question)
    return JSONResponse(status_code=201,content={"message":response})

