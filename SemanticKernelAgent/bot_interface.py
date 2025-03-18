import json
import requests
import gradio as gr
from config import CONSTS
import random, string

def sk_agent_response(user_message, chat_history, session_id):
    
    global session_
    
    if not chat_history:        
        session_ = session_id+''.join(random.choices(string.ascii_letters + string.digits, k=16))        
        
    headers = {"accept": "application/json", "Content-Type": "application/x-www-form-urlencoded","X-Session-Id":session_}
    params_={"user_input":user_message}
    
    try:
        response = requests.post(f"http://localhost:{int(CONSTS.default_port)}/invokeAgentWorkflow", params=params_, headers=headers) 
        output_ = json.loads(response.text)
        
        if output_.get("download_flag",False):
            file_name = output_.get("file_name")
            chat_response = output_.get("chat_response")
            
            file_path = f"{CONSTS.local_repo}/{file_name}"
            final_output = f"{chat_response}, [{file_name}]({file_path})"
              
            
        else:
            final_output = output_.get('chat_response')
        
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        final_output = 'Server down, please try later!!!'
              
    return final_output


id_component = gr.State(value = 'sk_agent_ui')
sk_demo = gr.ChatInterface(sk_agent_response,
                        additional_inputs = [id_component],
                        chatbot=gr.Chatbot(label='Play around with GitHub!!!',
                                           avatar_images=('./images/user.png','./images/bot.png'),
                                           scale=1,
                                           height=400,
                                           type="messages",
                                           ),
                        title='Semantic Kernel Agent Demo',
                        textbox=gr.Textbox(placeholder="Type your queries here", container=False, scale=7,submit_btn=True),
                        type="messages"
                                             
                        )

sk_demo.launch(share=True,server_port=int(CONSTS.gradio_port))