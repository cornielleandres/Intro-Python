# Write a class to hold player information, e.g. what room they are in
# currently.
class Player:
	def __init__(self, room, items, score, hp):
		self.room = room
		self.items = items
		self.score = score
		self.hp = hp

	def get_item(self, item):
		return self.items.append(item)

	def view_inventory(self):
		if len(self.items) > 0:
			print('Your inventory:')
			for item in self.items:
				print(' ' + item.description[0].upper() + item.description[1:].lower())
		else:
			print('No items in your inventory.')
