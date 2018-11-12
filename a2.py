#!/usr/bin/env python3
###################################################################
#
#   CSSE1001/7030 - Assignment 2
#
#   Student Username: s4442951
#
#   Student Name: Mounir Hedna
#
###################################################################

###################################################################
#
# The following is support code. DO NOT CHANGE.

from a2_support import *

# End of support code
################################################################

# Write your code here

class GameObject(object):
    """ A game object with a name and a position on a grid.
    """
    def __init__(self, name, position):
        """Creates a game object with a name and a position on a grid.

        Constructor: GameObject(string, (float, float))
        """
        self._name = name
        self._position = position

    def __str__(self):
        """Returns a string representation of the GameObject.

        str(GameObject) -> string
        """
        return GAME_OBJECT_FORMAT.format(self._name, self._position)

    def set_position(self, position):
        """ Sets the position of a GameObject equal to position.

        GameObject.set_position((int, int)) -> None
        """
        self._position = position

    def get_position(self):
        """Returns the current position of the GameObject.

        GameObject.get_position() -> (float, float)
        """
        return self._position

    def set_name(self, name):
        """Sets the GameObject name equal to name.

        GameObject.set_name(string) -> None
        """
        self._name = name

    def get_name(self):
        """Returns the name of the GameObject.

    
        GameObject.get_name() -> string
        """
        return self._name

class Pokemon(GameObject):
    """A Pokemon object that inherits from GameObject.
    """

    def __init__(self, name, position, terrain):
        """Creates a Pokemon with a name, position on a grid and it's terrain type.

        Constructor: Pokemon(string, (int, int), string)
        """
        super().__init__(name, position)
        self._terrain = terrain

    def __str__(self):
        """Returns a string representation of a Pokemon.

        str(Pokemon) -> string
        """
        return POKEMON_FORMAT.format(self._name, self._position, self._terrain)

    def set_terrain(self, terrain):
        """Sets the terrain type of the Pokemon equal to terrain.

        Pokemon.set_terrain(string) -> None
        """
        self._terrain = terrain

    def get_terrain(self):
        """Returns the terrain type of the Pokemon

        Pokemon.get_terrain() -> string
        """
        return self._terrain
        
class Wall(GameObject):
    """A wall class that inherits from GameObject
    """
    def __init__(self, name, position):
        """Creates a wall class

        Constructor: Wall(string, (float, float))
        """
        super().__init__(name, position)

class Player(GameObject):
    """A Player object that inherits from GameObject.
    """

    def __init__(self, name=DEFAULT_PLAYER_NAME):
        """Creates a Pokemon object.

        Constrcutor: Pokemon(string)
        """
        
        super().__init__(name, position=None)
        self._dex = Dex([])
        self._pokemon = []

    def get_pokemons(self):
        """Returns a list of all Pokemon caught by the player, in the order they
           were caught.

           Player.get_pokemons() -> list<Pokemon>
           """
        return self._pokemon

    def get_dex(self):
        """Returns the players Dex.

           Player.get_dex() -> Dex
        """
        return self._dex

    def reset_pokemons(self):
        """Resets all the Poemons caught by this player, including dex

           Player.reset_pokemons() -> None
        """
        self._pokemon = []
        self._dex = Dex([])

    def register_pokemon(self, pokemon):
        """Catches a pokemon and adds to the players Dex, provided it is expected.
           If not expected will raise UnexpectedPokemonError.

           Player.register_pokemon(Pokemon) -> None
        """
        if pokemon.get_name() not in self._dex.get_expected():
            raise UnexpectedPokemonError(DexError("{} is not expected by this Dex.".
                                                  format(pokemon.get_name())))

        self._dex.register(pokemon.get_name())
        self._pokemon += [pokemon]

    def __str__(self):
        """Returns a string representation of a player.

        str(Player) -> string
        """
        return PLAYER_FORMAT.format(self._name, self._position, len(self._pokemon))

class Dex(object):
    """A Dex class that contains a list of Pokemon
    """

    def __init__(self, pokemon_names):
        """Creates a Dex class.

        Constructor: Dex(list<string>)
        """

        self._pokemon_names = pokemon_names
        self._expected = {}
        for p in pokemon_names:
            self._expected[p] = False        

    def expect_pokemons(self, pokemon_names):
        """Instructs Dex to expect all pokemon in pokemon_names if they are not already
           expected.

           Dex.expect_pokemons(list<string>) -> None
        """

        for p in pokemon_names:
            if p not in self._expected:
                self._expected[p] = False

    def get_expected(self):
        """Returns the dictionary of expected pokemon.

        Dex.get_expected() -> dict<string : boolean>
        """

        return self._expected

    def expect_pokemons_from_dex(self, other_dex):
        """Adds a list of expected pokemon from other_dex to this dex

        Dex.expect_pokemons_from_dex(Dex) -> None
        """
        self._expected.update(other_dex.get_expected())

    def register(self, pokemon_name):
        """Registers the pokemon in the Dex. Returns True if the pokemon was already
        registered, else False. Raises anUnexpectedPokemonError if the pokemon is
        not expected by the Dex.

        Dex.register(string) -> boolean
        """
        if pokemon_name not in self._expected:
            raise UnexpectedPokemonError(DexError("{} is not expected by this Dex.".
                                                  format(pokemon.get_name())))

        if self._expected[pokemon_name]:
            return True
        else:
            self._expected[pokemon_name] = True
            return False

    def register_from_dex(self, other_dex):
        """Registers all pokemon from another Dex provided it is expected by this dex
        and registered on the other Dex.

        Dex.register_from_dex(Dex) -> None
        """
        for p in other_dex.get_expected(): 
            if p in self._expected and other_dex.get_expected()[p] == True:
                self._expected[p] = True

    def get_pokemons(self):
        """Returns an alphabetically list of (name, registered) pairs for each pokemon
        expected by this Dex.

        Dex.get_pokemons() -> list<(string, boolean)>
        """
        pokemons = []
        for p in Dex.get_expected(self):
            pokemons += [(p, Dex.get_expected(self)[p])]

        pokemons.sort()
        return pokemons

    def get_registered_pokemons(self):
        """Returns alphabetically sorted list of names of pokemons registered and expected
        in the Dex.

        Dex.get_registered_pokemons() -> list<string>
        """
        pokemons = []
        for p in self._expected:
            if self._expected[p] == True:
                pokemons += [p]

        pokemons.sort()

        return pokemons

    def get_unregistered_pokemons(self):
        """Returns an alphabetically sorted list of names of pokemons unregistered
        but expected by the Dex.

        Dex.get_unregistered_pokemons() -> list<string>
        """
        pokemons = []
        for p in self._expected:
            if self._expected[p] == False:
                pokemons += [p]

        pokemons.sort()

        return pokemons
    
    def __len__(self):
        """Returns the total number of pokemons expected by this Dex.

        len(Dex) -> int
        """
        return len(self._expected)

    def __contains__(self, name):
        """Returns True iff pokemon with name is registered in this Dex, else False.

        Dex.contains(string) -> boolean
        """
        if name in self._expected and self._expected[name] == True:
            return True
        else:
            return False

    def __str__(self):
        """Return a string representation of a Dex.

        str(Dex) -> string
        """
        return DEX_FORMAT.format(len(Dex.get_registered_pokemons(self)),
                                 ", ".join(Dex.get_registered_pokemons(self)),
                                 len(Dex.get_unregistered_pokemons(self)),
                                 ", ".join(Dex.get_unregistered_pokemons(self)))


class Level(object):
    """A Level that contains pokemon
    """

    def __init__(self, player, data):
        """Initialises a level with a player and data about which pokemon are in
           the level and their positions as well as the location of all walls.

        Constructor: Level(Player, dict<object>)
        """
        self._player = player
        self._data = data
        if not is_cell_position_valid(self.get_starting_position(), self.get_size()):
            raise InvalidPositionError("Invalid Start Position")
        self._dex = Dex([])
        self._poke_positions = {}
        for p in self._data["pokemons"]:
            if not is_cell_position_valid(p["position"], self.get_size()):
                raise InvalidPositionError("Invalid Pokemon Position")
            #Creates an instance of a Pokemon
            pokemon = Pokemon(p["name"], p["position"], Level.get_terrain(self))
            #Adds the Pokemon to the dictionary of Pokemon and their positions
            self._poke_positions[p["position"]] = pokemon
            #Level and Players Dex set to expect the Pokemon in this level
            self._dex.expect_pokemons([p["name"]])
            self._player.get_dex().expect_pokemons([p["name"]])

        #Wall positions from data
        self._wall_positions = {}
        for p in self._data["walls"]:
            if not is_wall_position_valid(p, self.get_size()):
                raise InvalidPositionError("Invalid Wall Position")
            self._wall_positions[p] = "wall"

        #Vertical boundary walls
        for y in range(0, Level.get_size(self)[0]):
            self._wall_positions[(y, -0.5)] = "wall"
            self._wall_positions[(y,Level.get_size(self)[1]-0.5)] = "wall"

        #Horizontal boundary walls
        for x in range(0, Level.get_size(self)[1]):
            self._wall_positions[(-0.5, x)] = "wall"
            self._wall_positions[(Level.get_size(self)[0]-0.5, x)] = "wall"

    def get_player(self):
        """Returns the player in the level

        Level.get_player() -> Player
        """
        return self._player

    def get_data(self):
        """Returns the data for the level

        Level.get_data() -> dict<object>
        """
        return self._data

    def get_size(self):
        """Returns the size of the level grid

        Level.get_size() -> (int, int)
        """
        return (self._data["rows"], self._data["columns"])

    
    def get_terrain(self):
        """Returns the terrain type of the level.

        Level.get_terrain() -> string
        """
        return self._data["terrain"]

    def get_dex(self):
        """Returns the Dex for this level.

        Level.get_dex() -> Dex
        """
        return self._dex

    def get_starting_position(self):
        """Returns the players starting position for this level.

        Level.get_starting_position() -> (int, int)
        """
        return self._data["player"]

    def is_obstacle_at(self, position):
        """Returns True iff an obstacle exists at position, else False.

        Level.is_obstacle_at((float, float)) -> boolean
        """
        if position in self._wall_positions:
            return True
        else:
            return False

    def get_obstacles(self):
        """Returns a list of all wall positions in the level.

        Level.get_obstacles() -> list<(float, float)>
        """
        walls = []
        for p in self._wall_positions:
            walls += [p]

        return walls

    def get_pokemons(self):
        """Returns a list of all Pokemon in this level.

        Level.get_pokemons() -> list<Pokemon>
        """
        pokemons = []
        for p in self._poke_positions:
            pokemon = self._poke_positions[p]
            pokemons += [pokemon]

        return pokemons

    def get_pokemon_at(self, position):
        """Return the pokemon that exists at the given position, else None.

        Level.get_pokemon_at((int, int)) -> Pokemon
        """
        if position in self._poke_positions:
            return self._poke_positions[position]
        else:
            return None

    def catch_pokemon_at(self, position):
        """Catches and returns the Pokemon that exists at the given position.
           If no pokemon exists at the position raises InvalidPositionError.

           Level.catch_pokemon_at((int, int)) -> Pokemon
        """
        if Level.get_pokemon_at(self, position) == None:
            raise InvalidPositionError("Invalid Pokemon Position")

        pokemon = Level.get_pokemon_at(self, position)
        self._dex.register(pokemon.get_name())
        self._player.register_pokemon(pokemon)

        del self._poke_positions[position]
        
        return pokemon

    def is_complete(self):
        """Returns True if all expected pokemon have been registered in the dex,
           else False.

           Level.is_complete() -> boolean
        """
        if len(self._dex.get_unregistered_pokemons()) == 0:
            return True
        else:
            return False

class Game(object):
    """The game class manages data pertaining to the entire game.
    """
    def __init__(self):
        """Initialises a game, contains an instance of the Player class which
           will be used when instantiating each Level. Also contains a list of
           Levels that will be loaded from a file or URL.
        """
        self._player = Player()
        self._levels = []
        self._current_level = 0
        
    def load_file(self, game_file):
        """Loads a game from a file.

        Game.load_file(string) -> None
        """
        game_data = load_game_file(game_file)
        #Resets the Player and Levels
        self._player = Player()
        self._levels = []
        self._current_level = 0
        #Creates a level with a new player in each level
        for x in range(0, len(game_data["levels"])):
            level_data = {}
            level_data = game_data["levels"][x]
            player = Player()
            level = Level(player, level_data)
            self._levels += [level]

    def load_url(self, game_url):
        """Loads a game from a URL.

        Game.load_game_url(string) -> None
        """
        game_data = load_game_url(game_file)
        self._player = Player()
        self._levels = []
        self._current_level = 0
        for x in range(0, len(game_data["levels"])):
            level_data = {}
            level_data = game_data["levels"][x]
            level = Level(self._player, level_data)
            self._levels += [level]

    def start_next_level(self):
        #Checks if last level is complete
        if(self._levels[len(self._levels)-1].is_complete()):
           return True
        else:
            self._current_level += 1
            level = self._levels[self._current_level - 1]
            
            if not is_cell_position_valid(level.get_starting_position(),
                                          level.get_size()):
                raise InvalidPositionError("Invalid Start Position")

            for p in level.get_data()["pokemons"]:
                if not is_cell_position_valid(p["position"], level.get_size()):
                    raise InvalidPositionError("Invalid Pokemon Position")

            for p in level.get_data()["walls"]:
                if not is_wall_position_valid(p, level.get_size()):
                    raise InvalidPositionError("Invalid Wall Position")
            #Checks if there is more than 1 level
            if self._current_level > 1:
                #Inherits all registered Pokemon from previous level
                prev_level = self._levels[self._current_level - 2]
                prev_dex = prev_level.get_dex()
                level_dex = level.get_dex()
                level_dex.expect_pokemons_from_dex(prev_dex)
                level_dex.register_from_dex(prev_dex)

            #Sets player to new levels starting position and updates dex with
            #expected pokemon
            y,x = level.get_starting_position()
            self._player.set_position((y,x))
            self._player.get_dex().expect_pokemons_from_dex(level.get_dex())
            
            return False

    def get_player(self):
        """Returns the player of the game.

        Game.get_player() -> Player
        """
        return self._player

    def get_level(self):
        """Returns the current level else None if game hasn't started.

        Game.get_level() -> Level
        """
        if len(self._levels) == 0:
            return None
        elif self._current_level == 0:
            return None
        else:
             return self._levels[self._current_level-1]

    def __len__(self):
        """Returns the total number of levels in the game.

        len(Game) -> int
        """
        return len(self._levels)

    def is_complete(self):
        """Returns True iff no levels remain incomplete, else False.

        Game.is_complete() -> boolean
        """
        for level in self._levels:
           if not level.is_complete():
               return False

        return True

    def move_player(self, direction):
        """Attempts to move the player in the given direction. Returns the
           object that player would have hit, else None.
           Raises DirectionError if direction is not NORTH, EAST, SOUTH or WEST.

           Game.move_player(string) -> GameObject
        """
        y,x = self._player.get_position()
        level = Game.get_level(self)
           
        if direction not in DIRECTIONS:
           raise DirectionError("Invalid Direction")

        elif direction == NORTH:
           y -= 1
           if level.is_obstacle_at((y+0.5, x)):
               return Wall("#", (y+0.5, x))
           elif level.get_pokemon_at((y,x)) == None:
               self._player.set_position((y,x))
               return None
           else:
               pokemon = level.get_pokemon_at((y,x))
               level.catch_pokemon_at((y,x))
               self._player.set_position((y,x))
               self._player.register_pokemon(pokemon)
               return pokemon

        elif direction == EAST:
           x += 1
           if level.is_obstacle_at((y, x-0.5)):
               return Wall("#", (y, x-0.5))
           elif level.get_pokemon_at((y,x)) == None:
               self._player.set_position((y,x))
               return None
           else:
               pokemon = level.get_pokemon_at((y,x))
               level.catch_pokemon_at((y,x))
               self._player.set_position((y,x))
               self._player.register_pokemon(pokemon)
               return pokemon

        elif direction == SOUTH:
           y += 1
           if level.is_obstacle_at((y-0.5, x)):
               return Wall("#", (y-0.5, x))
           elif level.get_pokemon_at((y,x)) == None:
               self._player.set_position((y,x))
               return None
           else:
               pokemon = level.get_pokemon_at((y,x))
               level.catch_pokemon_at((y,x))
               self._player.set_position((y,x))
               self._player.register_pokemon(pokemon)
               return pokemon

        elif direction == WEST:
           x -= 1
           if level.is_obstacle_at((y, x+0.5)):
               return Wall("#", (y, x+0.5))
           elif level.get_pokemon_at((y,x)) == None:
               self._player.set_position((y,x))
               return None
           else:
               pokemon = level.get_pokemon_at((y,x))
               level.catch_pokemon_at((y,x))
               self._player.set_position((y,x))
               self._player.register_pokemon(pokemon)
               return pokemon
           
    

# Uncomment the following to autorun GUI
if __name__ == "__main__":
     import gui
     gui.main()
