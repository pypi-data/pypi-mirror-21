from collections import namedtuple
from functools import partial

import numpy as np
import pandas as pd
import pyqtgraph as pg

from pyqtgraph.Qt import QtGui, QtCore

from graphysio import algorithms, exporter, utils

Point     = namedtuple('Point', ['x', 'y'])
Cardinals = namedtuple('Cardinals', ['A', 'B', 'C'])
Angles    = namedtuple('Angles', ['alpha', 'beta', 'gala'])

def truncatevec(vecs):
    # Ensure all vectors have the same length by truncating the end
    # Not feeling so well about this function
    lengths = map(len, vecs)
    maxidx = min(lengths)
    newvecs = [vec[0:maxidx] for vec in vecs]
    return newvecs

class LoopWidget(*utils.loadUiFile('loopwidget.ui')):
    def __init__(self, u, p, subsetrange, parent):
        super().__init__(parent=parent)
        self.setupUi(self)

        self.parent = parent
        self.xmin, self.xmax = subsetrange

        self.exporter = exporter.PuExporter(self, p.name())

        self.btnPrev.clicked.connect(self.prevloop)
        self.btnNext.clicked.connect(self.nextloop)
        self.btnDelete.clicked.connect(self.delloop)

        self.curidx = 0
        self.loops = []
        self.pen = p.pen
        self.graphicsView.setBackground('w')

        self.curveitem = pg.PlotCurveItem()
        self.scatteritem = pg.ScatterPlotItem()
        plotitem = self.graphicsView.getPlotItem()
        plotitem.addItem(self.scatteritem)
        plotitem.addItem(self.curveitem)

        self.initloopdata(u, p)

        if len(self.loops) > 0:
            self.lblTot.setText(str(len(self.loops)))
            self.renderloop(0)

    def getDurations(self, series, feetitem):
        def clip(vec):
            # Only keep visible data based on subsetrange
            cond = (vec > self.xmin) & (vec < self.xmax)
            return vec[cond]

        if feetitem is None or feetitem.starts.size < 1:
            # We have no feet, treat the whole signal as one cycle
            begins = series.head(1).index.values
            ends = series.tail(1).index.values
        elif feetitem.stops.size < 1:
            # We have no stops, starts serve as stops for previous cycle
            begins = feetitem.starts.index.values
            ends = np.append(begins[1:], series.index[-1])
        else:
            begins = feetitem.starts.index.values
            ends = feetitem.stops.index.values

        # Only draw currently visible data
        begins, ends = map(clip, [begins, ends])

        # Handle the case where we start in the middle of a cycle
        while ends[0] <= begins[0]:
            ends = ends[1:]

        begins, ends = truncatevec([begins, ends])
        durations = ends - begins

        return (begins, durations)

    def initloopdata(self, u, p):
        us = u.series; ps = p.series
        ubegins, udurations = self.getDurations(us, u.feetitem)
        pbegins, pdurations = self.getDurations(ps, p.feetitem)

        durations = (min(pd, ud) for pd, ud in zip(udurations, pdurations))

        for ubegin, pbegin, duration in zip(ubegins, pbegins, durations):
            loopu = us.loc[ubegin:ubegin+duration]
            loopp = ps.loc[pbegin:pbegin+duration]
            self.loops.append(PULoop(loopu, loopp))

    def renderloop(self, idx=None):
        if idx is None:
            idx = self.curidx

        curloop = self.loops[idx]

        self.lblIdx.setText(str(idx + 1))

        delay = int(curloop.offset / 1e6) # ns to ms
        self.lblDelay.setText(str(delay))

        round1 = partial(round, ndigits=1)
        alpha, beta, gala = map(round1, curloop.angles)
        self.lblAlpha.setText(str(alpha))
        self.lblBeta.setText(str(beta))
        self.lblGala.setText(str(gala))

        card = curloop.cardpoints
        cardx, cardy = zip(*card)

        # Set visible range with quadratic aspect ratio
        bottomleft = QtCore.QPointF(card.A.x, card.A.y)
        size = max(card.B.x - card.A.x, card.C.y - card.A.y)
        qsize = QtCore.QSizeF(size, size)
        rect = QtCore.QRectF(bottomleft, qsize)
        self.graphicsView.setRange(rect=rect)

        self.curveitem.setData(curloop.u.values, curloop.p.values, pen=self.pen)
        self.scatteritem.setData(np.array(cardx), np.array(cardy))
        
    def prevloop(self):
        idx = self.curidx - 1
        if idx >= 0:
            self.curidx = idx
            self.renderloop()

    def nextloop(self):
        idx = self.curidx + 1
        if idx < len(self.loops):
            self.curidx = idx
            self.renderloop()

    def delloop(self):
        self.loops.pop(self.curidx)
        if self.curidx >= len(self.loops):
            # Handle the case where we deleted the last item
            self.curidx = len(self.loops) - 1
        self.lblTot.setText(str(len(self.loops)))
        self.renderloop()


class PULoop(object):
    def __init__(self, u, p):
        self.__angles = None
        self.__cardpoints = None

        # Realign pressure and flow
        offset = p.index[0] - u.index[0]
        u.index += offset
        self.offset = abs(offset)

        df = pd.concat([u, p], axis=1)
        self.df = df.interpolate(method='index')

        self.u = self.df[u.name]
        self.p = self.df[p.name]

    @property
    def cardpoints(self):
        if self.__cardpoints is None:
            idxpmax = self.p.argmax()
            idxvmax = self.u.argmax()
            A = Point(self.u.iloc[0], self.p.iloc[0])
            B = Point(self.u.loc[idxvmax], self.p.loc[idxvmax])
            C = Point(self.u.loc[idxpmax], self.p.loc[idxpmax])
            self.__cardpoints = Cardinals(A, B, C)
        return self.__cardpoints

    @property
    def angles(self):
        if self.__angles is None:
            card = self.cardpoints
            alpha = self.calcangle(card.A, card.B)
            beta  = self.calcangle(card.A, card.B, card.C)
            gala  = self.calcangle(card.A, card.C)
            self.__angles = Angles(alpha, beta, gala)
        return self.__angles

    def calcangle(self, looporigin, pointb, pointa=None):
        orig = complex(looporigin.x, looporigin.y)
        cb = complex(pointb.x, pointb.y) - orig
        if pointa is None:
            ca = complex(1, 0)
        else:
            ca = complex(pointa.x, pointa.y) - orig
        angca = np.angle(ca, deg=True)
        angcb = np.angle(cb, deg=True)
        return abs(angca - angcb)
