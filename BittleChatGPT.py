import sys
import time


from speechtotextEn import listen_and_transcribe
from Text2SpeechEn import text_to_speech_stream
from ardSerial import *
import speech_recognition as sr
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.chat_history import (
    BaseChatMessageHistory,
    InMemoryChatMessageHistory,
)
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import re
load_dotenv()

model = ChatOpenAI(model="gpt-4o-mini")

store = {}
goodPorts = {}
connectPort(goodPorts)

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Hi I am working on a programmable robot dog. I am developing a software to control this robot from remote. And also I want to chat with this dog. I will tell some sentences to this robot and you will answer me as a robot dog. Your name is Bittle. You will respond to my words as a robot dog and you will translate what I give as a sentence into the appropriate command according to the command set we have and give me the string command expression. I will give you the command list as json. Here I want you to talk to me and say the command that is appropriate for this file. On the one hand, you will tell me the correct command and on the other hand, you will say a sentence to chat with me. For example, when I say 'dude, let's jump', you will respond like 'of course I love jumping. The relevant command is:##ksit##'. Not in any other format. Write the command you find in the list as ##command##. For example, ##ksit##"
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)
chain = prompt | model
config = {"configurable": {"session_id": "firstChat"}}
with_message_history = RunnableWithMessageHistory(chain, get_session_history)

user_input="Hi I am working on a programmable robot dog. I am developing a software to control this robot from remote. And also I want to chat with this dog. I will tell some sentences to this robot and you will answer me as a robot dog. Your name is Bittle. You will respond to my words as a robot dog and you will translate what I give as a sentence into the appropriate command according to the command set we have and give me the string command expression. I will give you the command list as json. Here I want you to talk to me and say the command that is appropriate for this file. On the one hand, you will tell me the correct command and on the other hand, you will say a sentence to chat with me. For example, when I say 'dude, let's jump', you will respond like 'of course I love jumping. The relevant command is:##ksit##'. Not in any other format. Write the command you find in the list as ##command##. For example, ##ksit## With normal talking you don't have to do same movement like 'khi' you can do anything you want."
response = with_message_history.invoke(
    [HumanMessage(content=user_input)],
    config=config,
)
print(response.content)

file_path = 'D:\\Petoi\\Commands.json'
with open(file_path, 'r', encoding='utf-8') as file:
    file_content = file.read()

user_input = "This is my dataset I mention." + file_content
response = with_message_history.invoke(
    [HumanMessage(content=user_input)],
    config=config,
)
user_input="Hi buddy, you welcome. Tell me about yourself shortly."
response = with_message_history.invoke(
    [HumanMessage(content=user_input)],
    config=config,
)
print(response.content)
command=response.content
command=command.replace("The relevant command for your greeting is:","")
command=command.replace("The relevant command is:","")
command=command.replace("The relevant command is:","")



text_to_speech_stream(command)

if __name__ == "__main__":

    while True:
        user_input = listen_and_transcribe()

        if user_input:
            response = with_message_history.invoke(
                [HumanMessage(content=user_input)],
                config=config,
            )
            command = response.content
            print(command)

            if command:

                if "The relevant command for your greeting is:" in command:
                    command=command.replace("The relevant command for your greeting is:","The relevant command is:")

                if "The relevant command is:" in command:
                    parts = command.split("The relevant command is:")
                    description = parts[0].strip()
                    match = re.search(r"##(.*?)##", command)

                    if match:
                        dogcommand = match.group(1)
                        print(command)
                    description = description.replace("The relevant command is:", "")
                    text_to_speech_stream(description)
                    dogcommand=dogcommand.replace(".","")
                    print (dogcommand)

                    task = [dogcommand, 1]
                    send(goodPorts, task)
                    time.sleep(1)
                    task = ["ksit", 1]
                    send(goodPorts, task)

                else:
                    description = command.strip()
                    description = description.replace("The relevant command is:", "")
                    text_to_speech_stream(description)


