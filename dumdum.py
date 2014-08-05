import rg

"""My first robot. Actually no, Will 'I am a lying bastard' Greenberg's first
   robot. He told me it was a really good, really effective robot that would
   totally beat him.

   HE LIED.

   Moves to the center, attacks enemies next to it, otherwise does nothing :("""


class Robot:
    def act(self, game):
        # if we're in the center, stay put
        if self.location == rg.CENTER_POINT:
            return ['guard']

        # if there are enemies around, attack them
        for loc, bot in game.robots.iteritems():
            if bot.player_id != self.player_id:
                if rg.dist(loc, self.location) <= 1:
                    return ['attack', loc]

        # move toward the center
        return ['move', rg.toward(self.location, rg.CENTER_POINT)]
