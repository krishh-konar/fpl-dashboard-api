import asyncio
import aiohttp
from fpl import FPL
from dotenv import dotenv_values
import requests
import mongo_helper
import pymongo
import urllib 
import json


ENV_VARS = dotenv_values(".env")
MONGO_URL = "mongodb://" + ENV_VARS["MONGO_FPL_DB_USERNAME"] + ":" + \
    urllib.parse.quote(ENV_VARS["MONGO_FPL_DB_PASSWORD"]) + "@localhost:27017/"

MONGO_CLIENT = pymongo.MongoClient(MONGO_URL)

async def get_user_gw_history(user_id):
    mongo_user_gw_history =  mongo_helper.isDocInCollection(
        MONGO_CLIENT, "user_id", user_id, "user_gw_history"
    )

    if mongo_user_gw_history[0]:
        print("cache_hit for get_user_gw_history")
        return mongo_user_gw_history[1]["data"]
    
    else:
        async with aiohttp.ClientSession() as session:
            fpl = FPL(session)
            # await fpl.login(ENV_VARS["FPL_ACCOUNT_EMAIL"], ENV_VARS["FPL_ACCOUNT_PASSWD"])
            user = await fpl.get_user(user_id)
            gw_history = await user.get_user_history()
        
        mongo_helper.insertIntoCollection(MONGO_CLIENT, \
            "user_gw_history", {"user_id": user_id, "data": gw_history})

        return gw_history

async def get_user_summary(user_id):
    mongo_user_summary =  mongo_helper.isDocInCollection(
        MONGO_CLIENT, "user_id", user_id, "user_summary"
    )

    if mongo_user_summary[0]:
        print("cache_hit for get_user_summary")
        return json.dumps(mongo_user_summary[1], default=str)

    else:
        async with aiohttp.ClientSession() as session:
            fpl = FPL(session)
            # await fpl.login(ENV_VARS["FPL_ACCOUNT_EMAIL"], ENV_VARS["FPL_ACCOUNT_PASSWD"])
            user = await fpl.get_user(user_id)
            user_summary = {
                "user_id": user_id,
                "player_first_name": user.player_first_name,
                "player_last_name": user.player_last_name,
                "player_region_name": user.player_region_name,
                "player_region_iso_code_long": user.player_region_iso_code_long,
                "summary_overall_points": user.summary_overall_points,
                "summary_overall_rank": user.summary_overall_rank,
                "summary_event_points": user.summary_event_points,
                "summary_event_rank": user.summary_event_rank,
                "current_event": user.current_event,
                "name": user.name,
                "last_deadline_total_transfers": user.last_deadline_total_transfers,
                "last_deadline_bank": user.last_deadline_bank,
                "last_deadline_value": user.last_deadline_value,
                "favourite_team": user.favourite_team
            }

        mongo_helper.insertIntoCollection(MONGO_CLIENT, "user_summary", user_summary)

        return json.dumps(user_summary, default=str)

async def get_season_history(user_id):
    mongo_user_season_history =  mongo_helper.isDocInCollection(
        MONGO_CLIENT, "user_id", user_id, "user_season_history"
    )

    if mongo_user_season_history[0]:
        print("cache_hit for get_season_history")
        return mongo_user_season_history[1]["data"]

    else:
        async with aiohttp.ClientSession() as session:
            fpl = FPL(session)
            # await fpl.login(ENV_VARS["FPL_ACCOUNT_EMAIL"], ENV_VARS["FPL_ACCOUNT_PASSWD"])
            user = await fpl.get_user(user_id)
            season_history = await user.get_season_history() 
        
        mongo_helper.insertIntoCollection(MONGO_CLIENT, \
            "user_season_history", {"user_id": user_id, "data": season_history})
        
        return season_history

def check_user_exists(user_id):
    resp = requests.get("https://fantasy.premierleague.com/api/entry/%s/" % user_id)
    
    if resp.status_code == 200:
        return {
            "status": "success", 
            "status_code": 200,
            "user_id": user_id,
            "player_first_name": resp.json()["player_first_name"],
            "player_last_name": resp.json()["player_last_name"]
        }
    else:
        return {
            "status": "failure",
            "status_code": 404
        }
    
