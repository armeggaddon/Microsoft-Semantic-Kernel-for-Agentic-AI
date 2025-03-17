import json
import logging
import tempfile
import traceback
from fastapi import APIRouter, Request
from utils.agent_util import get_tc_manager
from semantic_kernel.contents import ChatHistory

temp_dir = tempfile.gettempdir() 
logger = logging.getLogger(__name__)

router = APIRouter()   
chat_history = ChatHistory()


@router.post("/invokeAgentWorkflow", tags=["agent"], summary='Demonstrating Agent workflow', description='This demonstrates the Agentic AI workflow')
async def agent_workflow(request:Request, user_input:str): 

    try:

        chat_history.add_user_message(user_input)
        output_ = await test_case_agent(chat_history)
                  
        return output_    

    except Exception as e: 
        print(traceback.format_exc())
        logger.exception("######################### Error Processing the request in GPT model ############################")        
        output_ = {"chat_response":"error"} 

    
async def test_case_agent(chat_history):
    
    organiser = get_tc_manager()
    
    async for content in organiser.invoke(chat_history):
        # Add the response to the chat history
        chat_history.add_message(content)
        
    try:
        download_ = chat_history.messages[-3].inner_content.choices[0].message.tool_calls[0].function.arguments
        json_download_ = json.loads(download_)
        output_ = {"chat_response":content.content}
        output_.update({"download_flag":True, "download_data":json_download_['all_test_cases'],
                       "file_name":json_download_['file_name']})
        return output_
    
    except Exception as e:
        print("Just for fun")
    ############################################################################################
    output_ = {"chat_response":content.content}        
    return output_


