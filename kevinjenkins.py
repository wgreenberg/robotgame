import random
import rg

SQUAD_DIST = 3
JESUS_TAKE_THE_WHEEL = 10
CENTER = {'x': 9, 'y': 9}
SQUAD_POSITIONS = [
    (CENTER['x'] - SQUAD_DIST, CENTER['y'] - SQUAD_DIST),
    (CENTER['x'] + SQUAD_DIST, CENTER['y'] - SQUAD_DIST),
    (CENTER['x'] - SQUAD_DIST, CENTER['y'] + SQUAD_DIST),
    (CENTER['x'] + SQUAD_DIST, CENTER['y'] + SQUAD_DIST),
]

class Robot:
    def get_squad(self):
        closest = (None, 100000)
        for squad_pos in SQUAD_POSITIONS:
            squad_dist = rg.dist(self.location, squad_pos)
            if squad_dist < closest[1]:
                closest = (squad_pos, squad_dist)
        return closest[0]

    def is_near(self, pos):
        near = 3
        return rg.dist(self.location, pos) < near

    def squad_act(self, game):
        return ['move', rg.toward(self.location, self.squad_pos)]

    def closest_enemy(self, game):
        closest = (None, 1000000)
        enemies = [r for r in game.robots.values() if r.player_id != self.player_id]
        for enemy in enemies:
            enemy_dist = rg.wdist(self.location, enemy.location)
            if enemy_dist < closest[1]:
                closest = (enemy, enemy_dist)
        return closest[0]

    def seek_enemies(self, game):
        closest_enemy = self.closest_enemy(game)
        if closest_enemy is not None:
            if rg.wdist(self.location, closest_enemy.location) == 1:
                return ['attack', closest_enemy.location]
            else:
                return ['move', rg.toward(self.location, closest_enemy.location)]
        else:
            return ['guard']

    def enemies_abound(self, game):
        return self.is_near(self.closest_enemy(game).location)

    def act(self, game):
        self.squad_pos = self.get_squad()

        if self.hp < JESUS_TAKE_THE_WHEEL:
            return ['suicide']

        if self.is_near(self.squad_pos) or self.enemies_abound(game):
            return self.seek_enemies(game)
        else:
            return self.squad_act(game)

