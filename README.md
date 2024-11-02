# A Prometheus Exporter for Random Minecraft Metrics

Exposes metrics about player stats available in the world/stats/*.json files which can be exported to prometheus to be tracked over time.

Just a bit of fun.

# TODO

- Metrics:
    - [ ] minecraft:mined.* pie chart
        - [ ] minecraft:mined.minecraft:ancient_debris counter
        - [ ] minecraft:minecraft.minecraft:diamonds counter
    - [ ] minecraft:killed.* pie chart
    - [ ] minecraft:custom.minecraft:playtime stat
    - [ ] minecraft:custom.minecraft:animals_bred stat
    - [ ] minecraft:custom.minecraft:player_kills stat
- [ ] Integrate with Prometheus server
- [ ] Dockerise
- [ ] Create Grafana dashboard
