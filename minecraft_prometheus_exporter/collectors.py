from collections import defaultdict
import json
from typing import Dict, List
import os

from prometheus_client.core import CounterMetricFamily, REGISTRY
from prometheus_client.registry import Collector


path = "/opt/minecraft"


def get_player_uuids(server_path: str) -> Dict[str, str]:
    """Returns a dict where the key is the player uuid and value is the player name"""
    users_path = server_path + "/usercache.json"
    with open(users_path, "r") as f:
        players: List = json.load(f)
    
    return {player["uuid"]: player["name"] for player in players}


def get_player_stat_files(server_path: str) -> Dict[str, defaultdict]:
    """Returns the world/stats/*.json files for all players"""
    world_stats_path = server_path + "/world/stats/"
    stat_files = [file for file in os.listdir(world_stats_path) if file.endswith(".json")]
    
    player_stats_map = {}
    for file in stat_files:
        uuid = file.removesuffix(".json")
        with open(world_stats_path + file, "r") as f:
            stats: Dict = (json.load(f)["stats"])
        player_stats_map[uuid] = stats
    
    return player_stats_map


class Deaths(Collector):
    def collect(self):
        player_stats_map: Dict = get_player_stat_files(path)
        player_map = get_player_uuids(path)
        deaths_counter = CounterMetricFamily("deaths", "Number of deaths for each player", labels=["player_uuid", "player_name"])
        for uuid, data in player_stats_map.items():
            deaths = data.get("minecraft:custom", 0).get("minecraft:deaths", 0)
            deaths_counter.add_metric([uuid, player_map[uuid]], deaths)

        yield deaths_counter


class DiamondsMined(Collector):
    def collect(self):
        player_stats_map: Dict = get_player_stat_files(path)
        player_map = get_player_uuids(path)
        diamonds_mined_counter = CounterMetricFamily("diamonds_mined", "Number of diamonds mined by each player", labels=["player_uuid", "player_name"])
        for uuid, data in player_stats_map.items():
            deepslate = data.get("minecraft:mined", 0).get("minecraft:deepslate_diamond_ore", 0)
            normal = data.get("minecraft:mined", 0).get("minecraft:diamond_ore", 0)

            diamonds_mined_counter.add_metric([uuid, player_map[uuid]], deepslate+normal)

        yield diamonds_mined_counter


REGISTRY.register(Deaths())
REGISTRY.register(DiamondsMined())
