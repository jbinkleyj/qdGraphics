# qdGraphics.py
#
# The purpose of this module is to provide Processing-API-like 2D (static) drawing for python in
# a Jupyter notebook. I don't know if anyone else will find it useful, but here it is.
#
# Author: John C. Bowers <bowersjc@jmu.edu>
#

from IPython.display import SVG
from functools import reduce

class GraphicsStyleSettings:
    
    def __init__(self, gssCopy = None):
        if gssCopy == None:
            self.__stroke = "black"
            self.__strokeWidth = 1
            self.__strokeCap = "inherit"
            self.__fill = "white"
        else:
            self.__stroke = gssCopy.stroke
            self.__strokeWidth = gssCopy.strokeWidth
            self.__strokeCap = gssCopy.strokeCap
            self.__fill = gssCopy.fill

    @property
    def stroke(self):
        return self.__stroke

    @stroke.setter
    def stroke(self, stroke):
        self.__stroke = stroke

    @property
    def strokeWidth(self):
        return self.__strokeWidth

    @strokeWidth.setter
    def strokeWidth(self, strokeWidth):
        self.__strokeWidth = strokeWidth

    @property
    def strokeCap(self):
        return self.__strokeCap

    @strokeWidth.setter
    def strokeCap(self, strokeCap):
        self.__strokeCap = strokeCap

    @property
    def fill(self):
        return self.__fill

    @fill.setter
    def fill(self, fill):
        self.__fill = fill

    def css(self):
        return ('fill:%s;' % self.fill if self.fill != None else '') + \
               (('stroke:%s;stroke-width:%d;' % (self.stroke, int(self.strokeWidth))) if self.stroke != None else '')

class GraphicsContext:

    def __init__(self):
        self.clear()

    def clear(self):
        self.__width = 100
        self.__height = 100
        self.__styleSettings = [GraphicsStyleSettings()]
        self.__primitives = []
        self.__transform = [""]

    def pushTransform(self):
        self.__transform.append("")

    def pushMatrix(self):
        self.pushTransform()

    def popTransform(self):
        if len(self.__transform) > 1:
            del self.__transform[-1]

    def popMatrix(self):
        self.popTransform()

    @property
    def transform(self):
        return self.__transform[-1]

    def translate(self, x, y):
        self.__transform[-1] += (" translate(%d %d)" % (x, y))

    def rotate(self, theta):
        self.__transform[-1] += (" rotate(%d)" % theta)

    def append(self,gObj):
        self.__primitives.append(gObj)

    def svg(self):
        return '<svg height="%d" width="%d">%s</svg>' % (
            int(self.__height),
            int(self.__width),
            reduce(lambda svgStr, gObj: svgStr + gObj.svg(), self.__primitives, "")
        )

    def size(self, w, h):
        self.__width = w
        self.__height = h

    @property
    def style(self):
        return self.__styleSettings[-1]

    @property
    def width(self):
        return self.__width

    @width.setter
    def width(self, width):
        self.__width = width

    @property
    def height(self):
        return self.__height

    @height.setter
    def height(self, height):
        self.__height = height

    @property
    def stroke(self):
        return self.__styleSettings[-1].stroke

    @stroke.setter
    def stroke(self, stroke):
        self.__styleSettings[-1].stroke = stroke

    @property
    def strokeWidth(self, strokeWidth):
        return self.__styleSettings[-1].strokeWidth

    @strokeWidth.setter
    def strokeWidth(self, strokeWidth):
        self.__styleSettings[-1].strokeWidth = strokeWidth

    @property
    def fill(self):
        return self.__styleSettings[-1].fill

    @fill.setter
    def fill(self, fill):
        self.__styleSettings[-1].fill = fill

    def pushStyle(self):
        self.__styleSettings.append(GraphicsStyleSettings(self.__styleSettings[-1]))

    def popStyle(self):
        if (len(self.__styleSettings) > 1):
            del self.__styleSettings[-1]

_defaultContext = GraphicsContext()

class ellipse:

    def __init__(self, x, y, w, h, context=_defaultContext):
        self.__x = x
        self.__y = y
        self.__w = w
        self.__h = h
        context.append(self)
        self.__context = context
        self.__gss = GraphicsStyleSettings(context.style)
        self.__transform = context.transform

    def svg(self):
        st = self.__gss
        return '<ellipse cx="%d" cy="%d" rx="%d" ry="%d" style="%s" transform="%s" />' % (
            int(self.__x),
            int(self.__y),
            int(self.__w),
            int(self.__h),
            st.css(),
            self.__transform
        )

class line:

    def __init__(self, x1, y1, x2, y2, context=_defaultContext):
        self.__x1 = x1
        self.__y1 = y1
        self.__x2 = x2
        self.__y2 = y2
        context.append(self)
        self.__context = context
        self.__gss = GraphicsStyleSettings(context.style)
        self.__transform = context.transform

    def svg(self):
        st = self.__gss
        return '<line x1="%d" y1="%d" x2="%d" y2="%d" style="%s" transform="%s" />' % (
            int(self.__x1),
            int(self.__y1),
            int(self.__x2),
            int(self.__y2),
            st.css(),
            self.__transform
        )

class polygon:

    # points should be a list of 2-tuples of integers
    def __init__(self, points, context=_defaultContext):
        self.__points = points
        context.append(self)
        self.__context = context
        self.__gss = GraphicsStyleSettings(context.style)
        self.__transform = context.transform

    def svg(self):
        st = self.__gss
        return '<polygon points="%s" style="%s" transform="%s" />' % (
            reduce(lambda ptStr, pt: ptStr + ("%d,%d " % pt), self.__points, ""),
            st.css(),
            self.__transform
        )

def quad(x1, y1, x2, y2, x3, y3, x4, y4, context=_defaultContext):
    return polygon([(x1, y1), (x2, y2), (x3, y3), (x4, y4)], context)

def rect(x, y, w, h, context=_defaultContext):
    x2 = x + w
    y2 = y + h
    return quad(x, y, x2, y, x2, y2, x, y2, context)

def triangle(x1, y1, x2, y2, x3, y3, context=_defaultContext):
    return polygon([(x1, y1), (x2, y2), (x3, y3)], context)

CLOSE = True

class shape:

    def __init__(self, context=_defaultContext):
        context.append(self)
        self.__pathStack = [[]]
        self.__context = context
        self.__ended = False
        self.__gss = GraphicsStyleSettings(context.style)
        self.__createdPaths = [self.__pathStack[0]]
        self.__transform = context.transform

    def raiseErrorIfEnded(self):
        if self.__ended:
            raise RuntimeError("Once endShape() is called on a shape the only allowed method calls are to svg()")

    def vertex(self, x, y):
        self.raiseErrorIfEnded()
        self.__pathStack[-1].append((x, y))

    def beginContour(self):
        self.raiseErrorIfEnded()
        self.__pathStack.append([])
        self.__createdPaths.append(self.__pathStack[-1])

    def endContour(self):
        self.raiseErrorIfEnded()
        if len(self.__pathStack) > 1:
            del self.__pathStack[-1]
        else:
            raise RuntimeError("endContour() called without having first called beginContour()")

    def endShape(self, close = False):
        self.raiseErrorIfEnded()
        self.__close = close
        self.__ended = True

    def _pathStr(self, i):
        return  "M%d %d %s" % (
            self.__createdPaths[i][0][0],
            self.__createdPaths[i][0][1],
            (
                # Creates a string with all but the first point of the form
                # Lx1 y1 Lx2 y2 Lx3 y3 etc.
                reduce(lambda pathStr, pt: pathStr + ("L%d %d " % pt), self.__createdPaths[i][1:], "") + \
                ("Z" if self.__close else "")
            )
        )

    def svg(self):
        if not self.__ended:
            if self.__editingPath == self.__vertices:
                raise RuntimeError("Shape is not ended. did you remember to call endShape()?")
            else:
                raise RuntimeError("Contour is not ended. Did you remember to call endContour()?")
        st = self.__gss
        return '<path d="%s" style="%s" transform="%s" />' % (
            reduce(lambda pathStr, pathIdx: pathStr + self._pathStr(pathIdx), range(len(self.__createdPaths)), ""),
            st.css(),
            self.__transform
        )

# Starter code for new drawing classes:
# class xyz:
#     def __init__(self, context=_defaultContext):
#         context.append(self)
#         self.__context = context
#         self.__transform = context.transform
#     def svg(self):
#         st = self.__context.style
#         return '<!-- style="%s" transform="%s" /-->' % (
#             st.css(),
#             self.__transform
#         )

########################################################
# Convenience Functions for dealing with _defaultContext
########################################################

def clear(): global _defaultContext; _defaultContext.clear()
def size(w, h): global _defaultContext; WIDTH = w; HEIGHT = h; _defaultContext.size(w, h)
def pushTransform(): global _defaultContext; _defaultContext.pushTransform()
def pushMatrix(): global _defaultContext; _defaultContext.pushMatrix()
def popTransform(): global _defaultContext; _defaultContext.popTransform()
def popMatrix(): global _defaultContext; _defaultContext.popMatrix()
def translate(x, y): global _defaultContext; _defaultContext.translate(x, y)
def rotate(theta): global _defaultContext; _defaultContext.rotate(theta)
def stroke(stroke): global _defaultContext; _defaultContext.stroke = stroke
def strokeWidth(strokeWidth): global _defaultContext; _defaultContext.strokeWidth = strokeWidth
def fill(fill): global _defaultContext; _defaultContext.fill = fill
def pushStyle(): global _defaultContext; _defaultContext.pushStyle()
def popStyle(): global _defaultContext; _defaultContext.popStyle()
def svg(context=_defaultContext): global _defaultContext; return context.svg()
def draw(context=_defaultContext): return SVG(svg(context))

_theShape = None
def beginShape(): global _theShape; _theShape = shape()
def vertex(x, y): global _theShape; _theShape.vertex(x, y)
def beginContour(): global _theShape; _theShape.beginContour()
def endContour(): global _theShape; _theShape.endContour()
def endShape(close = False): global _theShape; _theShape.endShape(close); _theShape = None

print("DONE")
