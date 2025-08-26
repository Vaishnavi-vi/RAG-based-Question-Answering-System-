import streamlit as st
import json
import requests
from PIL import Image

url_link="http://127.0.0.1:8000/ask"
api_key="mysecretkey123"

st.set_page_config("Rag Question-Answer System with Memory",layout="centered")

page=st.sidebar.radio("Select one between the two:",["Intro","RAG"])
if page=="Intro":
    st.header("Rag Based Chatbot with ConversationalBuffermemory")
    image=Image.open("C:\\Users\\Dell\\Downloads\\Rag.png")
    st.image(image,use_container_width=True)
elif page=="RAG":
    st.header("Rag Based Chatbot with ConversationalBuffermemory, Integrating 4 websites which includes colbert, RAG description,Building embedding search")
    

    user_input=st.text_area("Enter your input:")
    
    input={"Question":user_input}
    if st.button("Answer:"):
        if user_input=="":
            st.warning("Please add an input")
        
    try:
        response=requests.post(url_link,json=input,params={"api_key":api_key})
        if response.status_code in [200,201,202]:
            result=response.json()
            st.write(f"Output:{result['message']}")
        else:
            st.write(f"{response.status_code}--{response.text}")
    except requests.exceptions.ConnectionError as e:
        st.write("Failed to connect with fast Api",e)
            

        

    