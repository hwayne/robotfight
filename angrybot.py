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


        local_enemies = self.local_enemies(game)
        empty_spaces = [e for e in self.local_spaces()
                        if e not in local_enemies.keys()]

        if local_enemies:
            if self.hp < 10 and len(local_enemies) > 1:
                return ['suicide']

            if is_angry:
                return ['attack', random.choice(local_enemies.keys())]
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
                                  random.choice(self.enemies(game)).location)]

    def local_spaces(self):
        return rg.locs_around(self.location,
                              filter_out=('invalid', 'obstacle',
                                          'spawn'))

    def in_square(self, location):
        bot = self.game.robots.get(location)
        if bot is None:
            return bot
        return ["friend", "foe"][bot.player_id != self.player_id]

    def enemies(self, game):
        return [e for e in game.robots.itervalues() if
                e.player_id != self.player_id]

    def local_enemies(self, game):
        locs = rg.locs_around(self.location)
        bots = {}
        for loc, bot in game.robots.iteritems():
            if bot.player_id != self.player_id and loc in self.local_spaces():
                bots[loc] = bot
        return bots
