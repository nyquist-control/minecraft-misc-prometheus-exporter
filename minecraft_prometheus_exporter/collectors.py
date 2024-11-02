import json
from typing import Dict, List, Generator

from prometheus_client.core import CounterMetricFamily, REGISTRY
from prometheus_client.registry import Collector
from pydantic import BaseModel


path = "/opt/minecraft"


class PlayerMetadata(BaseModel):
    name: str
    uuid: str
    data: Dict


def get_stat_file(server_path: str, uuid: str) -> Dict[str, Dict]:
    """Returns the world/stats/*.json files for all players"""
    path = server_path + "/world/stats/" + f"{uuid}.json"
    with open(path, "r") as f:
        return (json.load(f)["stats"])


def get_player_stats(server_path: str) -> Generator[PlayerMetadata]:
    """Returns a dict where the key is the player uuid and value is the player name"""
    users_path = server_path + "/usercache.json"
    with open(users_path, "r") as f:
        players: List = json.load(f)

    for player in players:
        yield PlayerMetadata(
            uuid=player["uuid"],
            name=player["name"],
            data=get_stat_file(path, player["uuid"])
        )


class Deaths(Collector):
    def collect(self):
        deaths_counter = CounterMetricFamily("deaths", "Number of deaths for each player", labels=["player_uuid", "player_name"])
        for player in get_player_stats(path):
            deaths = player.data.get("minecraft:custom", 0).get("minecraft:deaths", 0)
            deaths_counter.add_metric([player.uuid, player.name], deaths)

        yield deaths_counter


class DiamondsMined(Collector):
    def collect(self):
        diamonds_mined_counter = CounterMetricFamily("diamonds_mined", "Number of diamonds mined by each player", labels=["player_uuid", "player_name"])
        for player in get_player_stats(path):
            deepslate = player.data.get("minecraft:mined", 0).get("minecraft:deepslate_diamond_ore", 0)
            normal = player.data.get("minecraft:mined", 0).get("minecraft:diamond_ore", 0)

            diamonds_mined_counter.add_metric([player.uuid, player.name], deepslate+normal)

        yield diamonds_mined_counter


REGISTRY.register(Deaths())
REGISTRY.register(DiamondsMined())
