# qdGraphics

The initial purpose of the quick-and-dirty graphics library is to generate static images in [Jupyter](http://jupyter.org) using a set of commands based on the primities in the [Processing API](http://processing.org). I wasn't particularly happy using Calysto-Processing (though its an impressive feat, don't get me wrong), since its variables don't persist from one cell to the next in Jupyter, and I don't have the patience and time to learn the `matplotlib` library right now, so I hacked this out this evening. 

__THIS DOCUMENTATION IS INCOMPLETE__

So far the library supports the following: 

## Primitives

* `ellipse(x, y, w, h)`. Draws an ellipse with top-left corner at `(x, y)` and with width diameter of `w` and height diameter of `h`. 
* `line(x1, y1, x2, y2)`. Draws a line from `(x1, y1)` to `(x2, y2)`. 
* `polygon(points)` (where points is a list of 2-tuples of 2D point coordinates). Draws a polygon with vertices given by `points` parameter. 
* `quad(x1, y1, x2, y2, x3, y3, x4, y4)`. Draws a quadrilateral with vertices `(x1, y1)`, `(x2, y2)`, `(x3, y3)`, `(x4, y4)`. 
* `rect(x, y, w, h)`. Draws a rectangle with `(x, y)` as the top left corner and `w` and `h` as the width and height. 
* `triangle(x1, y1, x2, y2, x3, y3)`. Draws a traingle through `(x1, y1)`, `(x2, y2)`, `(x3, y3)`. 

## Shapes

More complicated shapes can be created via the following: 

* `beginShape()`. Start a new shape. 
* `vertex(x, y)`. Add a vertex to the shape. 
* `endShape(close)`. Finish the shape. Setting `close=True` closes the polygon. The global variable `CLOSE == True`. 
* `beginContour()`. Begin to define a secondary polygon for the shape, which is a hole. Once you call this, vertex modifies the current contour, not the outer shape. This should be specified in counter-clockwise order of vertices. 
* `endContour()`. End the current contour. 

## Transformations

TODO

* `pushTransform()`/`pushMatrix()`
* `popTransform()`/`popMatrix()`
* `translate(x, y)`
* `rotate(theta)`

## Style

TODO 

* `pushStyle()`
* `popStyle()`
* `fill(newFill)`
* `stroke(newStroke)`
* `strokeWidth(newStrokeWidth)`

## Setup and graphics context

* `clear()`
* `size(w, h)`

# Example code: 

```python
from qdGraphics import *

clear()
size(300,300)

fill("yellow")
strokeWidth(3)

ellipse(50, 50, 40, 30)
line (20, 30, 90, 100)
poly = polygon([(60,20), (100,40), (100,80), (60,100), (20,80), (20,40)])
quad(100,40,60,100,20,80,20,40)
rect(0, 0, 25, 10)

pushStyle()
pushTransform()
translate(30, 0)
fill("red")
strokeWidth(1)
stroke("green")
beginShape()
vertex(150, 0)
vertex(75, 200)
vertex(225, 200)
beginContour()
vertex(150, 40)
vertex(160, 70)
vertex(130, 60)
endContour()
endShape(CLOSE)
popStyle()

popMatrix()
fill("orange")

rotate(20)
translate(65, 75)

beginShape();
vertex(-40, -40);
vertex(40, -40);
vertex(40, 40);
vertex(-40, 40);
beginContour();
vertex(-20, -20);
vertex(-20, 20);
vertex(20, 20);
vertex(20, -20);
endContour();
endShape(CLOSE);

draw()
```
