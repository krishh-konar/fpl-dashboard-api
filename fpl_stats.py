import asyncio
import aiohttp
from fpl import FPL
from dotenv import dotenv_values
import requests

ENV_VARS = dotenv_values(".env")


async def get_user_gw_history(user_id):
    async with aiohttp.ClientSession() as session:
        fpl = FPL(session)
        # await fpl.login(ENV_VARS["FPL_ACCOUNT_EMAIL"], ENV_VARS["FPL_ACCOUNT_PASSWD"])
        user = await fpl.get_user(user_id)
        team = await user.get_user_history()
    return team

async def get_user_summary(user_id):
    async with aiohttp.ClientSession() as session:
        fpl = FPL(session)
        # await fpl.login(ENV_VARS["FPL_ACCOUNT_EMAIL"], ENV_VARS["FPL_ACCOUNT_PASSWD"])
        user = await fpl.get_user(user_id)
        user_summary = {
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
    return user_summary

async def get_season_history(user_id):
    async with aiohttp.ClientSession() as session:
        fpl = FPL(session)
        # await fpl.login(ENV_VARS["FPL_ACCOUNT_EMAIL"], ENV_VARS["FPL_ACCOUNT_PASSWD"])
        user = await fpl.get_user(user_id)
        season_history = await user.get_season_history() 
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
    


# a = asyncio.run(get_season_history(1495979))
# print(a)
