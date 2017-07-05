import chessboard
from copy import deepcopy
from datetime import datetime, timedelta
from knight import Knight
from sys import exit
from ttk import Frame, Style
import Tkinter


class Interface(Frame):

	def __init__(self, parent):

		Frame.__init__(self, parent)
		self.parent = parent
		self.initUI()

	def initUI(self):

		self.parent.title("Knight's Tour")
		Style().configure("TButton", padding=(0, 0, 0, 0), font='serif 10')

		for i in range(chessboard.board_size):
			self.columnconfigure(i, pad=0)
			self.rowconfigure(i, pad=0)

		for i in range(chessboard.board_size):
			for j in range(chessboard.board_size):
				coordinate = chr(i + ord('A'))+str(j+1)
				button = Tkinter.Button(self, text=coordinate, command=lambda coordinate=coordinate: self.run(coordinate))
				button.grid(row=j, column=i)

		self.pack()

	def run(self, starting_point):
		original_knight = Knight(next_move=starting_point)
		knight = deepcopy(original_knight)
		time_limit = timedelta(seconds=1)
		start_time = datetime.now()
		solved = False
		while not solved:
			knight = deepcopy(original_knight)
			iteration_start = datetime.now()
			# sometimes this can run a long time with bad paths
			# this attempts to cut off unnecessarily long dead ends
			solved = knight.make_move((iteration_start + time_limit))
		end_time = datetime.now()
		print knight
		print chessboard.Chessboard(knight.get_tour_progress())
		print "Elapsed time: ", (end_time - start_time)


def init(starting_point=None):
	if starting_point is None:
		print chessboard.Chessboard()
		starting_point = raw_input('Please select a starting point: ')

		if starting_point.lower() in ['exit', 'stop', 'quit']:
			print "\nMaybe some other time, then.\n"
			exit()

	try:
		chessboard.coordinate_to_indexes(starting_point)
	except:
		print
		starting_point = raw_input(
			'Sorry, that was an invalid entry! Please enter a value in the following format - "A1": ')
		try:
			chessboard.coordinate_to_indexes(starting_point)
		except:
			print "\nGo home, you're drunk.\n"

	return starting_point[0].upper() + starting_point[1]


if __name__ == '__main__':
	root = Tkinter.Tk()
	app = Interface(root)
	root.mainloop()

	# original_knight = Knight(next_move=init())
	# knight = deepcopy(original_knight)
	# time_limit = timedelta(seconds=1)
	# start_time = datetime.now()
	# solved = False
	# while not solved:
	# 	knight = deepcopy(original_knight)
	# 	iteration_start = datetime.now()
	# 	# sometimes this can run a long time with bad paths
	# 	# this attempts to cut off unnecessarily long dead ends
	# 	solved = knight.make_move((iteration_start + time_limit))
	# end_time = datetime.now()
	# print knight
	# print chessboard.Chessboard(knight.get_tour_progress())
	# print "Elapsed time: ", (end_time - start_time)
