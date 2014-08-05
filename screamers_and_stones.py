import rg
import random
from collections import defaultdict

"""While Will 'I read Atlas Shrugged 10,000 times' Greenberg will gleefully
   break any and every rule in the world, I only bend the rules slightly, and
   only in reaction to somebody else cheating. Also occasionally preemptively.
   Also occasionally just because. But at least it's lightly bending the rules.
   Or sometimes heavily.

   Anyway! One of the most venerable rules of Robotfight is 'each robot uses
   the same code'. But I'm 99% certain that Will will bribe the judges into
   letting him run two seperate codes, so I'm hacking in that functionality.
   The code keeps a list of every bots id and role, and calls that role's act
   function to decide what it does. The only two roles here are 'screamers',
   which attack things, and 'stones', which stay put. This does terribly, as
   it's only supposed to be a prototype for multiple robot tactics that I'll
   use to make more complicated robots. So don't tell Will! It's a secret. """


class Robot:

    def assign_role(self):
        CHANCE_OF_SCREAMER = 50
        choices = [self.act_screamer, self.act_stone]
        return choices[random.randint(0, 100) < CHANCE_OF_SCREAMER]

    def __init__(self):
        self.robot_roles = defaultdict(self.assign_role)

    def act(self, game):
        return self.robot_roles[self.robot_id](game)

    def act_screamer(self, game):
        self.game = game

        adjacent_enemies = self.enemies_around(game)
        if adjacent_enemies:
            if self.hp < 15:
                return ['suicide']

            enemy_spaces = adjacent_enemies.keys()
            return ['attack', random.choice(enemy_spaces)]

        enemies = self.enemies(game)
        displacementii = [(self.location, e.location) for e in enemies]
        closest = min(displacementii, key=lambda x: (x[0][0]-x[1][0])**2 +
                                                    (x[0][1]-x[0][1])**2)
        return ['move', rg.toward(*closest)]

    def act_stone(self, game):
        return ['guard']




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
