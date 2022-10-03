
from fastapi import FastAPI
from fastapi_versioning import VersionedFastAPI, version
from pydantic import BaseModel
import fpl_stats
import asyncio
import aiohttp
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse



#########################
### Fast API Settings ###
#########################

app = FastAPI(title="FPL Dashboard API")

origins = [
    "http://fpl-dashboard.local:3000",
    "http://localhost:3000"
]

headers = {"Access-Control-Allow-Origin": "*"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    # allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

###############################

##################
### App Routes ###
##################


@app.get("/healthcheck")
@version(1)
def read_root():
    return {"status": "ok"}

@app.get("/check_user/{user_id}")
@version(1)
def check_user(user_id):
    if not user_id:
        return JSONResponse(content={"status": "user not defined"}, headers=headers, status_code=404)
    resp = fpl_stats.check_user_exists(user_id)
    return JSONResponse(content=resp, headers=headers)

@app.get("/team_history/{user_id}")
@version(1)
def get_team_history(user_id):
    data = asyncio.run(fpl_stats.get_user_gw_history(user_id))

    return JSONResponse(content={"data": data}, headers=headers)

@app.get("/user_info/{user_id}")
@version(1)
def get_user_info(user_id):
    data = asyncio.run(fpl_stats.get_user_summary(user_id))
    
    return JSONResponse(content={"details": data}, headers=headers)

@app.get("/season_history/{user_id}")
@version(1)
def get_season_history(user_id):
    data = asyncio.run(fpl_stats.get_season_history(user_id))
    
    return JSONResponse(content={"details": data}, headers=headers)

#Version the API
app = VersionedFastAPI(app,
    version_format='{major}',
    prefix_format='/v{major}')