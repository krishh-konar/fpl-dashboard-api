
from fastapi import FastAPI
from fastapi_versioning import VersionedFastAPI, version
from pydantic import BaseModel
import fpl_stats
import asyncio
import aiohttp
from fastapi.middleware.cors import CORSMiddleware



#########################
### Fast API Settings ###
#########################

app = FastAPI(title="FPL Dashboard API")

origins = [
    "http://fpl-api.local:8000"
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    # allow_origins=origins,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

###############################

##################
### App Routes ###
##################


@app.get("/v1/healthcheck")
@version(1)
def read_root():
    return {"status": "ok"}

@app.get("/team_history")
@version(1)
def get_team_history():
    data = asyncio.run(fpl_stats.get_user_gw_history(1495979))
    
    return {
        "data": data
    }

@app.get("/user_info")
@version(1)
def get_user_info():
    data = asyncio.run(fpl_stats.get_user_summary(1495979))
    
    return {
        "details": data
    }


#Version the API
app = VersionedFastAPI(app,
    version_format='{major}',
    prefix_format='/api/v{major}')