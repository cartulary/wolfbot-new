PING_WAIT = 300  # Seconds
MINIMUM_WAIT = 0 # debug, change to 60 for normal
EXTRA_WAIT = 0
MAXIMUM_WAITED = 2  # limit for amount of !wait's
MAX_SHOTS = 2
DRUNK_SHOTS_MULTIPLIER = 3
NIGHT_TIME_LIMIT = 0
DAY_TIME_LIMIT = 0
START_WITH_DAY = False

                    #       HIT    MISS    SUICIDE
GUN_CHANCES         =   (   5/7  ,  1/7  ,   1/7   )
DRUNK_GUN_CHANCES   =   (   4/7  ,  2/7  ,   1/7   )
MANSLAUGHTER_CHANCE =       1/5

GAME_MODES = {}

################################################################################################
# ROLE INDEX:   PLAYERS     SEER    WOLF   CURSED   DRUNK   HARLOT  TRAITOR  GUNNER   CROW     #
ROLES_GUIDE = {    4    : (   1   ,   1   ,   0   ,   0   ,   0   ,    0   ,   0   ,   0    ), #
                   6    : (   1   ,   1   ,   1   ,   1   ,   0   ,    0   ,   0   ,   0    ), #
                   8    : (   1   ,   2   ,   1   ,   1   ,   1   ,    0   ,   0   ,   0    ), #
                   10   : (   1   ,   2   ,   1   ,   1   ,   1   ,    1   ,   1   ,   0    ), #
                   None : (   0   ,   0   ,   0   ,   0   ,   0   ,    0   ,   0   ,   0    )} #
################################################################################################

ROLE_INDICES = {0 : "seer",
                1 : "wolf",
                2 : "cursed",
                3 : "village drunk",
                4 : "harlot",
                5 : "traitor",
                6 : "gunner",
                7 : "werecrow"}
INDEX_OF_ROLE = dict((v,k) for k,v in ROLE_INDICES.items())


NO_VICTIMS_MESSAGES = ("The body of a young penguin pet is found.",
                       "A pool of blood and wolf paw prints are found.",
                       "Traces of wolf fur are found.")
LYNCH_MESSAGES = ("The villagers, after much debate, finally decide on lynching \u0002{0}\u0002, who turned out to be... a \u0002{1}\u0002.",
                  "Under a lot of noise, the pitchfork-bearing villagers lynch \u0002{0}\u0002, who turned out to be... a \u0002{1}\u0002.",
                  "The mob drags a protesting \u0002{0}\u0002 to the hanging tree. S/He succumbs to the will of the horde, and is hanged. It is discovered (s)he was a \u0002{1}\u0002.",
                  "Resigned to his/her fate, \u0002{0}\u0002 is led to the gallows. After death, it is discovered (s)he was a \u0002{1}\u0002.")
                                              

is_role = lambda plyr, rol: rol in ROLES and plyr in ROLES[rol]

def plural(role):
    if role == "wolf": return "wolves"
    elif role == "person": return "people"
    else: return role + "s"
    
def list_players():
    pl = []
    for x in ROLES.values():
        pl.extend(x)
    return pl
    
def list_players_and_roles():
    plr = {}
    for x in ROLES.keys():
        for p in ROLES[x]:
            plr[p] = x
    return plr
    
get_role = lambda plyr: list_players_and_roles()[plyr]


def del_player(pname):
    prole = get_role(pname)
    ROLES[prole].remove(pname)


    
class InvalidModeException(Exception): pass
def game_mode(name):
    def decor(c):
        GAME_MODES[name] = c
        return c
    return decor

    
CHANGEABLE_ROLES = { "seers"  : INDEX_OF_ROLE["seer"],
                     "wolves" : INDEX_OF_ROLE["wolf"],
                     "cursed" : INDEX_OF_ROLE["cursed"],
                    "drunks"  : INDEX_OF_ROLE["village drunk"],
                   "harlots"  : INDEX_OF_ROLE["harlot"],
                  "traitors"  : INDEX_OF_ROLE["traitor"],
                   "gunners"  : INDEX_OF_ROLE["gunner"],
                 "werecrows"  : INDEX_OF_ROLE["werecrow"]}
    
#  !game roles=wolves:1 seers:0, x=1

# TODO: implement game modes
@game_mode("roles")
class ChangedRolesMode(object):
    def __init__(self, arg):
        self.ROLES_GUIDE = ROLES_GUIDE.copy()
        lx = list(ROLES_GUIDE[None])
        pairs = arg.split(",")
        pl = list_players()
        if not pairs:
            raise InvalidModeException("Invalid syntax for mode roles.")
        for pair in pairs:
            change = pair.split(":")
            if len(change) != 2:
                raise InvalidModeException("Invalid syntax for mode roles.")
            role, num = change
            try:
                num = int(num)
                try:
                    lx[CHANGEABLE_ROLES[role.lower()]] = num
                except KeyError:
                    raise InvalidModeException(("The role \u0002{0}\u0002 "+
                                                "is not valid.").format(role))
            except ValueError:
                raise InvalidModeException("A bad value was used in mode roles.")
        for k in ROLES_GUIDE.keys():
            self.ROLES_GUIDE[k] = tuple(lx)