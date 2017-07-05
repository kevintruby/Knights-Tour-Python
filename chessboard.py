import string

board_size = 8


def coordinate_to_indexes(coordinate):
	if not isinstance(coordinate, str) or len(coordinate) < 2:
		raise Exception('invalid coordinate')

	inner_index = coordinate[0]
	outer_index = coordinate[1]

	if not inner_index.isalpha() or not outer_index.isdigit():
		raise Exception('invalid coordinate')

	inner_index = string.lowercase.index(inner_index.lower())
	outer_index = int(outer_index) - 1

	if index_out_of_range(inner_index) or index_out_of_range(outer_index):
		raise Exception('invalid coordinate')

	return inner_index, outer_index


def index_out_of_range(i):
	return bool(i < 0 or i > (board_size - 1))


def column_labels():
	return [chr(i + ord('A')) for i in range(board_size)]


def row_labels():
	return [str(i+1) for i in range(board_size)]


class Chessboard(object):

	def __init__(self, tour_progress=None):
		self.matrix = [[None for x in range(board_size)] for x in range(board_size)]
		if tour_progress is not None and isinstance(tour_progress, list):
			step = 1
			for move in tour_progress:
				inner_index, outer_index = coordinate_to_indexes(move)
				self.matrix[outer_index][inner_index] = str(step)
				step += 1

	def __repr__(self):
		return self.prep_for_print()

	def prep_for_print(self):
		rsp = '\n   '
		for col_header in column_labels():
			rsp += '  ' + col_header + ' '
		rsp += '\n'
		row = 0
		for x in self.matrix:
			row_header = row_labels()[row]
			rsp += row_header + ('  ' if len(row_header) < 2 else ' ')
			for y in x:
				step = y if y is not None else '  '
				step = (' ' if len(step) < 2 else '') + step
				rsp += '[%s]' % step
			rsp += '\n'
			row += 1
		return rsp
