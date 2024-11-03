import json
from typing import Any, Dict, Iterable, List, Generator

from prometheus_client.core import CounterMetricFamily, GaugeMetricFamily, REGISTRY
from prometheus_client.metrics_core import Metric
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


def get_player_stats(server_path: str) -> Generator[PlayerMetadata, Any, Any]:
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


class PlayTime(Collector):
    def collect(self):
        play_time = CounterMetricFamily("play_time", "Number of seconds since first joined server", labels=["player_uuid", "player_name"])
        for player in get_player_stats(path):
            ticks = player.data.get("minecraft:custom", 0).get("minecraft:play_time", 0)
            time = ticks / 20 # time in seconds
            play_time.add_metric([player.uuid, player.name], time)

        yield play_time


class PlayerKills(Collector):
    def collect(self):
        player_kills = CounterMetricFamily("player_kills", "Number of animals bred", labels=["player_uuid", "player_name"])
        for player in get_player_stats(path):
            kills = player.data.get("minecraft:custom", 0).get("minecraft:player_kills", 0)
            player_kills.add_metric([player.uuid, player.name], kills)

        yield player_kills


class DiamondsMined(Collector):
    def collect(self):
        diamonds_mined_counter = CounterMetricFamily("diamonds_mined", "Number of diamonds mined by each player", labels=["player_uuid", "player_name"])
        for player in get_player_stats(path):
            deepslate = player.data.get("minecraft:mined", 0).get("minecraft:deepslate_diamond_ore", 0)
            normal = player.data.get("minecraft:mined", 0).get("minecraft:diamond_ore", 0)

            diamonds_mined_counter.add_metric([player.uuid, player.name], deepslate+normal)

        yield diamonds_mined_counter


class MobsKilled(Collector):
    def collect(self):
        mobs_killed = GaugeMetricFamily("mobs_killed", "", labels=["player_uuid", "player_name", "mob_killed"])
        for player in get_player_stats(path):
            if player.data.get("minecraft:killed"):
                for mob, num in player.data.get("minecraft:killed").items():
                    mobs_killed.add_metric([player.uuid, player.name, mob.removeprefix("minecraft:")], num)

        yield mobs_killed


class OresMined(Collector):
    def collect(self):
        ores = [
            "diamond_ore",
            "deepslate_diamond_ore",
            "gold_ore",
            "deepslate_gold_ore",
            "iron_ore",
            "deepslate_iron_ore",
            "ancient_debris"
        ]
        ores_mined = GaugeMetricFamily("ores_mined", "", labels=["player_uuid", "player_name", "ore"])
        for player in get_player_stats(path):
            if not player.data.get("minecraft:mined"):
                continue
            for mined, num in player.data.get("minecraft:mined").items():
                if mined.removeprefix("minecraft:") in ores:
                    ores_mined.add_metric([player.uuid, player.name, mined.removeprefix("minecraft:")], num)

        yield ores_mined

REGISTRY.register(Deaths())
REGISTRY.register(PlayTime())
REGISTRY.register(PlayerKills())
REGISTRY.register(DiamondsMined())
REGISTRY.register(MobsKilled())
REGISTRY.register(OresMined())
