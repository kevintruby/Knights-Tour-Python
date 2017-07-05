import chessboard
import random
from copy import deepcopy
from datetime import datetime

_movement_directions = ['north_northwest', 'north_northeast',
						'east_northeast', 'east_southeast',
						'south_southeast', 'south_southwest',
						'west_southwest', 'west_northwest'
]

_direction_deltas = dict(
	north_northwest = [ -2, -1 ], north_northeast   = [ -2,  1 ],
	east_northeast	= [ -1,  2 ], east_southeast	= [  1,  2 ],
	south_southeast	= [  2,  1 ], south_southwest	= [  2, -1 ],
	west_southwest	= [  1, -2 ], west_northwest	= [ -1, -2 ]
)

_require_closed_tour = True


def compare_with_ties(a, b):
	diff = cmp(a, b)
	return diff if diff else random.choice([-1, 1])


def coordinates_in_range(last_coordinate):
	options = list()
	for direction in _movement_directions:
		inner_index, outer_index = chessboard.coordinate_to_indexes(last_coordinate)

		outer_index += _direction_deltas[direction][0]
		inner_index += _direction_deltas[direction][1]

		if chessboard.index_out_of_range(outer_index) or chessboard.index_out_of_range(inner_index):
			continue

		next_coordinate = chessboard.column_labels()[int(inner_index)] + chessboard.row_labels()[int(outer_index)]
		options.append(next_coordinate)
	return deepcopy(options)


class Knight(object):

	def __init__(self, tour_progress=list(), next_move=None):
		self.tour_progress = list()
		self.queued_moves = list()
		while len(tour_progress):
			self.tour_progress.append(tour_progress[0])
			self._next_moves()
			del tour_progress[0]
		if next_move is not None:
			# value of next_move should have already been evaluated, no need to double-check
			self.tour_progress.append(next_move)
			self._next_moves()

	def __repr__(self):
		return str(self.get_tour_progress())

	def _next_moves(self):
		self.queued_moves.append(list())
		tour_progress = self.get_tour_progress()
		last_coordinate = tour_progress[-1]
		vetted_moves = dict()
		penultimate_move = len(self.get_tour_progress()) == ((chessboard.board_size * chessboard.board_size) - 1)

		for next_coordinate in coordinates_in_range(last_coordinate):
			if next_coordinate not in tour_progress:
				secondary_moves = coordinates_in_range(next_coordinate)
				possible_moves = len(secondary_moves)
				for move in secondary_moves:
					if move in tour_progress:
						possible_moves -= 1
				if possible_moves > 0 or penultimate_move:
					vetted_moves[next_coordinate] = possible_moves

		optimized_moves = sorted(vetted_moves, key=vetted_moves.get, cmp=compare_with_ties)
		for coordinate in optimized_moves:
			self.add_to_queue(coordinate)

	def add_to_queue(self, move):
		if len(self.queued_moves):
			self.queued_moves[-1].append(move)

	def evaluate_move(self):
		if len(self.tour_progress) == (chessboard.board_size * chessboard.board_size):
			if not _require_closed_tour:
				return True
			elif self.tour_progress[-1] in coordinates_in_range(self.tour_progress[0]):
				return True
		return False

	def get_queued_moves(self):
		return deepcopy(self.queued_moves[-1]) if len(self.queued_moves) else []

	def get_tour_progress(self):
		return deepcopy(self.tour_progress)

	def make_move(self, time_limit=None):
		complete = False

		# sometimes this can run a long time with bad paths
		# this attempts to cut off unnecessarily long dead ends
		current_time = datetime.now()
		if time_limit is not None and current_time > time_limit:
			return complete

		while len(self.queued_moves) and len(self.queued_moves[-1]) and not complete:
			next_move = self.next_move()
			if next_move:
				self.tour_progress.append(next_move)
				self._next_moves()
				if self.evaluate_move():
					complete = True
				else:
					complete = self.make_move(time_limit)
					if not complete:
						self.undo_move()
		return complete

	def next_move(self):
		queued_move = None
		if len(self.queued_moves) > 0 and len(self.queued_moves[-1]) > 0:
			queued_move = self.queued_moves[-1][0]
			del self.queued_moves[-1][0]
		return queued_move

	def undo_move(self):
		if len(self.tour_progress) > 1:
			del self.tour_progress[-1]
			del self.queued_moves[-1]
