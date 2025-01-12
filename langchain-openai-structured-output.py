from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from pydantic import BaseModel
import os
from langchain_core.messages import HumanMessage, SystemMessage

class CalendarEvent(BaseModel):
    name: str
    date: str
    participants: list[str]

if __name__ == '__main__':
    load_dotenv()
    
    chat = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    messages = [
        SystemMessage(content="""Extract the event information and return it as a JSON object with the following fields:
        - name: string (event name)
        - date: string (event date)
        - participants: array of strings (list of participants)"""),
        HumanMessage(content="Alice and Bob are going to the science fair on Friday")
    ]
    
    response = chat.invoke(messages)
    
    try:
        # Parse the response content as JSON and validate against the model
        event_data = CalendarEvent.model_validate_json(response.content)
        print(event_data)
    except Exception as e:
        print("Raw response:", response.content)
        print("Error parsing response:", e)
