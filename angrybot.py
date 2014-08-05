import rg
import random

"""Fresh off my crushing defeat with 'dumdum', I was unimagineably angry at
   Will 'Allergic to Sunshine and Smiles' Greenberg. So angry the angriness
   leaked into my robot. It tries to kite enemies but just gets so angry
   at times it charges instead. It's also too angry to live a crippled life, so
   it explodes instead.

   Also has swanking 'Will'/'Not Will' targetting software!"""


class Robot:

    def act(self, game):
        self.game = game
        max_angry = 10
        angry = 8
        is_angry = random.choice([True]*angry+[False]*(max_angry-angry))

        adjacent_enemies = self.enemies_around(game)
        local_spaces = rg.locs_around(self.location,
                                      filter_out=('invalid', 'obstacle',
                                                  'spawn'))

        enemy_spaces = adjacent_enemies.keys()
        empty_spaces = [e for e in local_spaces
                        if e not in enemy_spaces]

        if adjacent_enemies:
            if self.hp < 10 and len(adjacent_enemies) > 1:
                return ['suicide']

            if enemy_spaces and is_angry:
                return ['attack', random.choice(enemy_spaces)]
            if empty_spaces:
                return ['move', random.choice(empty_spaces)]

            return['guard']

        enemies = self.enemies(game)

        for enemy in enemies:
            displacement = (self.location, enemy.location)
            if rg.wdist(*displacement) == 2:
                attack_loc = rg.toward(*displacement)
                if is_angry:
                    return ['move', attack_loc]
                if self.in_square(attack_loc) != 'friend':
                    return ['attack', attack_loc]

        return ['move', rg.toward(self.location,
                                  random.choice(enemies).location)]

    def in_square(self, location):
        bot = self.game.robots.get(location)
        if bot is None:
            return bot
        return ["friend", "foe"][bot.player_id != self.player_id]

    def enemies(self, game):
        return [e for e in game.robots.itervalues() if
                e.player_id != self.player_id]

    def enemies_around(self, game):
        locs = rg.locs_around(self.location)
        bots = {}
        for loc, bot in game.robots.iteritems():
            if bot.player_id != self.player_id and loc in locs:
                bots[loc] = bot
        return bots
