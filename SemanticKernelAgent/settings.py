import uvicorn
from config import CONSTS
from fastapi import FastAPI
from router import invoke_agent_workflow
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title=CONSTS.app_name,
              description=CONSTS.app_desc,
              )

app.include_router(invoke_agent_workflow.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
    

if __name__ == "__main__":
    uvicorn.run("settings:app", host="0.0.0.0", port=int(CONSTS.default_port))


   


