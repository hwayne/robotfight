import rg
import random
from collections import defaultdict

""" Will 'I prance and dance in fancy pants' Greenberg challenged me today.
So I unleashed my secret weapon, in the form of multiple role robots.
Hunters flush towards the nearest kiter, who attacks towards the nearest
hunter.

I lied. They don't organize at all.

I also lied about it being awesome. They suck."""

class Robot:

    def assign_role(self):
        choices = [self.act_hunter, self.act_kiter]
        d = { c:0 for c in choices }
        for x in self.robot_roles.values():
            d[x] += 1
        return choices[d[self.act_hunter] > d[self.act_kiter]*2]

    def __init__(self):
        self.robot_roles = defaultdict(self.assign_role)
        self.state = defaultdict(dict)

    def act(self, game):
        self.game = game
        return self.robot_roles[self.robot_id](game)

    def act_kiter(self, game):
        if 'foe' in map(self.in_square, self.local_spaces()):
            return self.evade()
        for square in self.local_spaces():
            if self.square_is_threatened(square):
                return ['attack', rg.toward(self.location, square)]

        return ['move', rg.toward(self.location,
                                  random.choice(self.enemies(game)).location)]

    def act_hunter(self, game):
        if self.local_enemies(game):
            if self.hp < 10:
                return ['suicide']

            return ['attack', random.choice(self.local_enemies(game).keys())]

        return ['move', rg.toward(self.location,
                                  random.choice(self.enemies(game)).location)]


    def local_spaces(self):
        return rg.locs_around(self.location,
                            filter_out=('invalid', 'obstacle',
                                        'spawn'))

    def square_is_threatened(self, square):
        return any(self.in_square(l) == 'foe' for l in rg.locs_around(square))


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

    def evade(self):
        for square in self.local_spaces():
            if not self.square_is_threatened(square):
                return ['move', rg.toward(self.location, square)]
        return ['guard']
