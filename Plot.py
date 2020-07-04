from time import sleep
from math import pi, atan2, sqrt
import matplotlib.text as mtext
import matplotlib.transforms as mtransforms
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as lines


class MyLine(lines.Line2D):

	def __init__(self, *args, **kwargs):
		# we'll update the position when the line data is set
		self.text = mtext.Text(0, 0, '')
		lines.Line2D.__init__(self, *args, **kwargs)

		# we can't access the label attr until *after* the line is
		# initiated
		self.text.set_text(self.get_label())

	def set_figure(self, figure):
		self.text.set_figure(figure)
		lines.Line2D.set_figure(self, figure)

	def set_transform(self, transform):
		# 2 pixel offset
		texttrans = transform + mtransforms.Affine2D().translate(2, 2)
		self.text.set_transform(texttrans)
		lines.Line2D.set_transform(self, transform)

	def set_data(self, x, y):
		if len(x):
			self.text.set_position((x[-1], y[-1]))

		lines.Line2D.set_data(self, x, y)

	def draw(self, renderer):
		# draw my label at the end of the line with 2 pixel offset
		lines.Line2D.draw(self, renderer)
		self.text.draw(renderer)



def display(title, R, T, O, P, F):
    fig, ax = plt.subplots()
    
    for o in O :
        b = [[o[0][0], o[1][0]], [o[0][1], o[1][1]]]
        ax.add_line(MyLine(b[0], b[1]))

    p = []
    for i in range(len(P)):
        if i == 0:
            p.append([R, P[i]])
        if i == len(P)-1:
            p.append([T, P[i]])
        else:
            p.append([P[i], P[i+1]])
    

    for i in p :
        b = [[i[0][0], i[1][0]], [i[0][1], i[1][1]]]
        L = MyLine(b[0], b[1])
        L.set_color((1, 0, 0, 1))
        ax.add_line(L)


    for f in range(len(F)):
        if f%2 == 0:
            F[f]-=100
        else:
            F[f]+=100
    plt.axis(F)


    plt.plot([R[0]], [R[1]], 'bs')
    plt.plot([T[0]], [T[1]], 'rs')
    plt.annotate('T', xy=T)
    plt.annotate('expert', xy=R)
    fig.suptitle(title, fontsize=16, color=(1, 0, 0, 1))
    plt.show()