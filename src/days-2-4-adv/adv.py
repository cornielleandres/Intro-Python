import textwrap
from item import Item, Treasure, LightSource
from room import Room
from player import Player
from monster import Monster

# Declare all items

item = {
    'nothing': Item(
                'nothing',
                'no items'
            ),
    'sword': Item(
                'sword',
                'a wooden SWORD'
            ),

    'shield': Item(
                'shield',
                'an iron SHIELD'
            ),

    'ruby': Treasure(
                'ruby',
                'a large RUBY',
                5
            ),

    'gold': Treasure(
                'gold',
                'GOLD nuggets',
                15
            ),

    'sapphire': Treasure(
                'sapphire',
                'a SAPPHIRE pendant',
                10
            ),

    'lamp': LightSource(
                'lamp',
                'a bright LAMP'
            )
}

# Declare all the rooms

room = {
    'outside':  Room(
                    'Outside Cave Entrance',
                    'North of you, the cave mount beckons.',
                    item['nothing'],
                    True
                ),

    'entrance':  Room(
                    'Cave Entrance',
                    'The cave entrance is eerily silent.',
                    item['lamp'],
                    False
                ),

    'foyer':    Room(
                    'Foyer',
                    'Dim light filters in from the south. Dusty passages run north and east.',
                    item['shield'],
                    False
                ),

    'overlook': Room(
                    'Grand Overlook',
                    'A steep cliff appears before you, falling into the darkness. Ahead to the north, a light flickers in the distance, but there is no way across the chasm.',
                    item['sword'],
                    False
                ),

    'narrow':   Room(
                    'Narrow Passage',
                    'The narrow passage bends here from west to north. The smell of gold permeates the air.',
                    item['ruby'],
                    False
                ),

    'treasure': Room(
                    'Treasure Chamber',
                    'You\'ve found the long-lost treasure chamber! Sadly, it has already been completely emptied by earlier adventurers. The only exit is to the south.',
                    item['gold'],
                    False
                ),

    'hall': Room(
                    'Dark Hall',
                    'The smell of fire and brimstone emanates from the south. Better make sure you are prepared for whatever may await.',
                    item['sapphire'],
                    False
                ),

    'chamber': Room(
                    'Large Chamber',
                    'You\'ve stumbled upon a large chamber. A hideous beast awakens and swifly blocks your retreat!',
                    item['nothing'],
                    True
                )
}


# Link rooms together

room['outside'].n_to    = room['entrance']
room['entrance'].s_to   = room['outside']
room['entrance'].n_to   = room['foyer']
room['foyer'].s_to      = room['entrance']
room['foyer'].n_to      = room['overlook']
room['foyer'].e_to      = room['narrow']
room['overlook'].s_to   = room['foyer']
room['narrow'].w_to     = room['foyer']
room['narrow'].n_to     = room['treasure']
room['narrow'].e_to     = room['hall']
room['treasure'].s_to   = room['narrow']
room['hall'].w_to       = room['narrow']
room['hall'].s_to       = room['chamber']


#
#                                             Map
#
#
#                       Overlook(3)        Treasure(5)
#                          |                   |
#                          |                   |
#                       Foyer(2) ---------- Narrow(4) ---------- Hall(6)
#                          |                                       |
#                          |                                       |
#                       Entrance(1)                            Chamber(7)
#                          |
#                          |
#                       Outside
#
#
# (1): Lamp   (2): Shield   (3): Sword   (4): Ruby   (5): Gold   (6): Sapphire   (7): Beast
#

#
# Main
#

# Make a new player object that is currently in the 'outside' room.

# Write a loop that:
#
# * Prints the current room name
# * Prints the current description (the textwrap module might be useful here).
# * Waits for user input and decides what to do.
#
# If the user enters a cardinal direction, attempt to move to the room there.
# Print an error message if the movement isn't allowed.
#
# If the user enters "q", quit the game.

p = Player(room['outside'], [], 0, 100)
m = Monster(100)

def print_wrapped_lines(value = ''):
    wrapper = textwrap.TextWrapper(width = 50)
    word_list = wrapper.wrap(text = value)

    for element in word_list:
        print(element)

def start_game():
    valid_moves = {'n': 'north', 's': 'south', 'e': 'east', 'w': 'west'}
    currRoom = p.room
    inventory = p.items
    get_item = p.get_item
    view_inventory = p.view_inventory
    text_divider = '\n====================\n'

    def try_get_item(item_name):
        if item_name == currRoom.item.name:
            get_item(currRoom.item)
            print(text_divider)
            print_wrapped_lines(f'You have picked up {currRoom.item.description}.')
            currRoom.item.on_take(p, print_wrapped_lines)
            print('\n')
            setattr(currRoom, 'item', item['nothing'])
        else:
            print(text_divider)
            print_wrapped_lines(f'This room does not have a(n) {item_name}.')
            print('\n')

    def try_drop_item(item_name):
        for index, item in enumerate(inventory):
            if item.name == item_name:
                del inventory[index]
                setattr(currRoom, 'item', item)
                print(text_divider)
                print_wrapped_lines(f'You have dropped the {item_name}.')
                currRoom.item.on_drop(print_wrapped_lines)
                print('\n')
                return view_inventory()
        print(text_divider)
        print(f'Your inventory does not contain: {item_name}.')
        return print('\n')

    print(text_divider)

    while True:
        if currRoom.name == 'Large Chamber':
            print_wrapped_lines(currRoom.description)
            print('\n')
            inventory_list = [item.name for item in inventory]
            if 'sword' not in inventory_list:
                print_wrapped_lines('You are unarmed! The beast easily overpowers you and eats you alive. If only you had found a weapon...')
                print('\n')
                return print_wrapped_lines('Game over.')
            else:
                while True:
                    print_wrapped_lines(f'Monster has {m.hp} hp.')
                    print_wrapped_lines(f'You have {p.hp} hp.')
                    print('\n')
                    if 'shield' not in inventory_list:
                        print_wrapped_lines('You have a sword but no shield. What will you do?')
                    else:
                        print_wrapped_lines('You have a sword and a shield. What will you do?')

                    next_action = input('(a)ttack / (r)un / (q)uit :')
                    next_action = next_action.lower()

                    if next_action[0] == 'a':
                        if m.hp > 0 and p.hp > 0:
                            print(text_divider)
                            print_wrapped_lines('You swing your sword with all your might.')
                            print_wrapped_lines('Its a hit!')
                            m.hp = m.hp - 35
                            if m.hp <= 0:
                                print('\n')
                                print_wrapped_lines('You\'ve done it! You slayed the beast! You take your spoils of war and flee, living to fight another day.')
                                print('\n')
                                return print_wrapped_lines('Game over. Thanks for playing.')
                            print_wrapped_lines('The beast takes a swipe with its giant claws.')
                            print('\n')
                            if 'shield' in inventory_list:
                                p.hp = p.hp - 30
                            else:
                                p.hp = p.hp - 50
                            if p.hp <= 0:
                                print_wrapped_lines('Your wounds are too great. You collapse and the beast eats you alive. If only you had found something to defend yourself with...')
                                print('\n')
                                return print_wrapped_lines('Game over.')
                    elif next_action[0] == 'r':
                        print(text_divider)
                        print_wrapped_lines('You foolishly tried to run but could not escape. The beast devoured you. If only you had been braver...')
                        print('\n')
                        return print_wrapped_lines('Game over.')
                    elif next_action[0] == 'q':
                        print(text_divider)
                        print_wrapped_lines('Do you really want to quit?')
                        print('\n')
                        confirm_exit = input('(y)es / (n)o :')
                        confirm_exit = confirm_exit.lower()

                        if confirm_exit == 'yes' or confirm_exit == 'y':
                            print(text_divider)
                            print_wrapped_lines('See ya!')
                            return print('/n')
                        else:
                            print(text_divider)
                            continue
        if currRoom.is_light == True or isinstance(currRoom.item, LightSource) or True in [True for item in inventory if isinstance(item, LightSource)]:
            print_wrapped_lines(f'You are currently in the {currRoom.name}.')
            print_wrapped_lines(currRoom.description)
            print('\n')
            if hasattr(currRoom.item, 'value'):
                print_wrapped_lines(f'This room has {currRoom.item.description}. Thats quite a treasure.')
            else:
                print_wrapped_lines(f'This room has {currRoom.item.description}.')
        else:
            print_wrapped_lines('It\'s pitch black!')

        print('\n')

        print_wrapped_lines('What would you like to do?')
        next_action = input('(g)et <item> / (d)rop <item> / (i)nventory / (s)core / (k)eep moving / (q)uit :')
        next_action = next_action.lower()

        if next_action[:4] == 'get ':
            if currRoom.is_light == True or isinstance(currRoom.item, LightSource) or True in [True for item in inventory if isinstance(item, LightSource)]:
                try_get_item(next_action[4:])
            else:
                print(text_divider)
                print_wrapped_lines('Good luck finding that in the dark!')
                print('\n')
            continue

        elif next_action[:2] == 'g ':
            if currRoom.is_light == True or isinstance(currRoom.item, LightSource) or True in [True for item in inventory if isinstance(item, LightSource)]:
                try_get_item(next_action[2:])
            else:
                print(text_divider)
                print_wrapped_lines('Good luck finding that in the dark!')
                print('\n')
            continue

        elif next_action[:5] == 'drop ':
            try_drop_item(next_action[5:])
            print('\n')
            continue

        elif next_action[:2] == 'd ':
            try_drop_item(next_action[2:])
            print('\n')
            continue

        elif next_action == 'inventory' or next_action == 'i':
            print(text_divider)
            view_inventory()
            print('\n')
            continue
        
        elif next_action == 'score' or next_action == 's':
            print(text_divider)
            print(f'You have {p.score} points.')
            print('\n')
            continue

        elif next_action == 'keep moving' or next_action == 'k':
            pass
        
        elif next_action == 'quit' or next_action == 'q':
            print(text_divider)
            print_wrapped_lines('Do you really want to quit?')
            print('\n')
            confirm_exit = input('(y)es / (n)o :')
            confirm_exit = confirm_exit.lower()

            if confirm_exit == 'yes' or confirm_exit == 'y':
                print(text_divider)
                print_wrapped_lines('See ya!')
                return print('/n')
            else:
                print(text_divider)
                continue

        else:
            print(text_divider)
            print_wrapped_lines(f'Invalid input: {next_action}')
            print('\n')
            continue

        print(text_divider)
        print_wrapped_lines('You decide to keep moving.')
        print('\n')
        print_wrapped_lines('Which direction do you want to go?')

        next_move = input('(n)orth / (s)outh / (e)ast / (w)est / (q)uit :')

        next_move = next_move.lower()
        print(text_divider)
        room_attr = f'{next_move[0]}_to'

        if (len(next_move) == 1 and next_move[0] in valid_moves.keys()) or next_move in valid_moves.values():
            if hasattr(currRoom, room_attr):
                currRoom = getattr(currRoom, room_attr)
            else:
                print_wrapped_lines(f'There is nothing to the {valid_moves[next_move[0]]}. Pick another direction.')
                print('\n')
        elif next_move == 'quit' or next_move == 'q':
            print_wrapped_lines('Do you really want to quit?')
            print(text_divider)
            print('\n')
            confirm_exit = input('(y)es / (n)o :')
            confirm_exit = confirm_exit.lower()

            if confirm_exit == 'yes' or confirm_exit == 'y':
                print(text_divider)
                print_wrapped_lines('See ya!')
                return print('/n')
            else:
                print(text_divider)
        else:
            print(text_divider)
            print_wrapped_lines(f'Invalid direction: {next_move}')
            print('\n')

if __name__ == '__main__':
    start_game()
