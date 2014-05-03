Examples
========

The following examples demonstrate the use of Cassowary in practical
constraint-solving problems.

Quadrilaterals
--------------

The "Bounded Quadrilateral" demo is the `online example`_ provided for
Cassowary.  The online example is implemented in JavaScript, but the
implementation doesn't alter the way the Cassowary algoritm is used.

.. _online example: http://www.badros.com/greg/cassowary/js/quaddemo.html

The Bounded quadrilateral problem starts with a bounded, two dimensional
canvas. We want to draw a quadilateral on this plane, subject to a number of
constraints.

Firstly, we set up the solver system itself::

    from cassowary import SimplexSolver, Variable, Constraint
    solver = SimplexSolver()

Then, we set up a convenience class for holding information about points
on a 2D plane::

    class Point(object):
        def __init__(self, identifier, x, y):
            self.x = Variable('x' + identifier, x)
            self.y = Variable('y' + identifier, y)

        def __repr__(self):
            return u'(%s, %s)' % (self.x.value, self.y.value)

Now we can set up a set of points to describe the initial location of our
quadrilateral - a 190x190 square::

    points = [
        Point('0', 10, 10),
        Point('1', 10, 200),
        Point('2', 200, 200),
        Point('3', 200, 10),

        Point('m0', 0, 0),
        Point('m1', 0, 0),
        Point('m2', 0, 0),
        Point('m3', 0, 0),
    ]
    midpoints = points[4:]

Note that even though we're drawing a quadrilateral, we have 8 points. We're
tracking the position of the midpoints independent of the corners of our
quadrilateral. However, we don't need to define the position of the midpoints.
The position of the midpoints will be set by defining constraints.

Next, we set up some stays. A stay is a constraint that says that a particular
variable shouldn't be modified unless it needs to be - that it should "stay"
as is unless there is a reason not to. In this case, we're going to set a stay
for each of the four corners - that is, don't move the corners unless you have
to. These stays are defined as ``WEAK`` stays -- so they'll have a very low
priority in the constraint system. As a tie breaking mechanism, we're also
going to set each stay to have a different weight - so the top left corner
(point 1) will be moved in preference to the bottom left corner (point 2), and
so on::

    weight = 1.0
    multiplier = 2.0
    for point in points[:4]:
        solver.add_stay(point.x, strength=WEAK, weight=weight)
        solver.add_stay(point.y, strength=WEAK, weight=weight)
        weight = weight * multiplier

Now we can set up the constraints to define where the midpoints fall. By
definition, each midpoint **must** fall exactly halfway between two points
that form a line, and that's exactly what we describe - an expression that
computes the position of the midpoint. This expression is used to construct a
:class:`Constraint`, describing that the value of the midpoint must equal the
value of the expression. The :class:`Constraint` is then added to the solver
system::

    for start, end in [(0, 1), (1, 2), (2, 3), (3, 0)]:
        cle = (points[start].x + points[end].x) / 2
        cleq = midpoints[start].x == cle
        solver.add_constraint(cleq)

        cle = (points[start].y + points[end].y) / 2
        cleq = midpoints[start].y == cle
        solver.add_constraint(cleq)

When we added these constraints, we didn't provided any arguments - that means
that they will be added as ``REQUIRED`` constraints.

Next, lets add some constraints to ensure that the left side of the quadrilateral
stays on the left, and the top stays on top::

    solver.add_constraint(points[0].x + 20 <= points[2].x)
    solver.add_constraint(points[0].x + 20 <= points[3].x)

    solver.add_constraint(points[1].x + 20 <= points[2].x)
    solver.add_constraint(points[1].x + 20 <= points[3].x)

    solver.add_constraint(points[0].y + 20 <= points[1].y)
    solver.add_constraint(points[0].y + 20 <= points[2].y)

    solver.add_constraint(points[3].y + 20 <= points[1].y)
    solver.add_constraint(points[3].y + 20 <= points[2].y)

Each of these constraints is posed as an :class:`Constraint`. For example, the first
expression describes a point 20 pixels to the right of the x coordinate of the top
left point. This :class:`Constraint` is then added as a constraint on the x coordinate
of the bottom right (point 2) and top right (point 3) corners - the x coordinate of these
points must be at least 20 pixels greater than the x coordinate of the top left corner
(point 0).

Lastly, we set the overall constraints -- the constraints that limit how large our
2D canvas is. We'll constraint the canvas to be 500x500 pixels::

    for point in points:
        solver.add_constraint(point.x >= 0)
        solver.add_constraint(point.y >= 0)

        solver.add_constraint(point.x <= 500)
        solver.add_constraint(point.y <= 500)

This gives us a fully formed constraint system. Now we can use it to answer
layout questions. The most obvious initial question -- where are the midpoints?

    >>> print midpoints[0]
    (10.0, 105.0)
    >>> print midpoints[1]
    (105.0, 200.0)
    >>> print midpoints[2]
    (200.0, 105.0)
    >>> print midpoints[3]
    (105.0, 10.0)

You can see from this that the midpoints have been positioned exactly where you'd
expect - half way between the corners - without having to explicitly specify their
positions.

These relationships will be maintained if we then edit the position of the corners.
Lets move the position of the bottom right corner (point 2). We mark the variables
associated with that corner as being *Edit variables*::

    solver.add_edit_var(points[2].x)
    solver.add_edit_var(points[2].y)

Then, we start an edit, change the coordinates of the corner, and stop the edit::

    solver.begin_edit()

    solver.suggest_value(points[2].x, 300)
    solver.suggest_value(points[2].y, 400)

    solver.end_edit()

As a result of this edit, the midpoints have automatically been updated::

    >>> print midpoints[0]
    (10.0, 105.0)
    >>> print midpoints[1]
    (155.0, 300.0)
    >>> print midpoints[2]
    (250.0, 205.0)
    >>> print midpoints[3]
    (105.0, 10.0)

If you want, you can now repeat the edit process for any of the points - including
the midpoints.

GUI layout
----------

The most common usage (by deployment count) of the Cassowary algoritm is as
the Autolayout mechanism that underpins GUIs in OS X Lion and iOS6. Although
there's lots of code required to make a full GUI toolkit work, the layout
problem is a relatively simple case of solving constraints regarding the size
and position of widgets in a window.

In this example, we'll show a set of constraints used to determine the
placement of a pair of buttons in a GUI. To simplify the problem, we'll only
worry about the X coordinate; expanding the implementation to include the Y
coordinate is a relatively simple exercise left for the reader.

When laying out a GUI, widgets have a width; however, widgets can also change
size. To accomodate this, a widget has two size constraints in each dimension:
a minimum size, and a preferred size. The miniumum size is an ``REQUIRED``
constraint that must be met; the preferred size is a ``STRONG`` constraint
that the solver should try to accomodate, but may break if necessary.

The GUI also needs to be concerned about the size of the window that is being
laid out. The size of the window can be handled in two ways:

* a ``REQUIRED`` constraint -- i.e., this *is* the size of the window;
  show me how to lay out the widgets; or

* a ``WEAK`` constraint -- i.e., come up with a value for the window size that
  accomodates all the other widget constraints. This is the interpretation used
  to determine an initial window size.

As with the Quadrilateral demo, we start by creating the solver, and creating
a storage mechanism to hold details about buttons::

    from cassowary import SimplexSolver, Variable, Constraint

    solver = SimplexSolver()

    class Button(object):
        def __init__(self, identifier):
            self.left = Variable('left' + identifier, 0)
            self.width = Variable('width' + identifier, 0)

        def __repr__(self):
            return u'(x=%s, width=%s)' % (self.left.value, self.width.value)

We then define our two buttons, and the variables describing the size of the
window on which the buttons will be placed::

    b1 = Button('b1')
    b2 = Button('b2')
    left_limit = Variable('left', 0)
    right_limit = Variable('width', 0)

    left_limit.value = 0
    solver.add_stay(left_limit)
    solver.add_stay(right_limit, WEAK)

The left limit is set as a ``REQUIRED`` constraint -- the left border can't
move from coordinate 0. However, the window can expand if necessary to accomodate
the widgets it contains, so the right limit is a ``WEAK`` constraint.

Now we can define the constraints on the button layouts::

    # The two buttons are the same width
    solver.add_constraint(b1.width == b2.width)

    # Button1 starts 50 from the left margin.
    solver.add_constraint(b1.left == left_limit + 50)

    # Button2 ends 50 from the right margin
    solver.add_constraint(left_limit + right_limit == b2.left + b2.width + 50)

    # Button2 starts at least 100 from the end of Button1. This is the
    # "elastic" constraint in the system that will absorb extra space
    # in the layout.
    solver.add_constraint(b2.left == b1.left + b1.width + 100)

    # Button1 has a minimum width of 87
    solver.add_constraint(b1.width >= 87)

    # Button1's preferred width is 87
    solver.add_constraint(b1.width == 87, strength=STRONG)

    # Button2's minimum width is 113
    solver.add_constraint(b2.width >= 113)

    # Button2's preferred width is 113
    solver.add_constraint(b2.width == 113, strength=STRONG)

Since we haven't imposed a hard constraint on the right hand side, the constraint
system will give us the smallest window that will satisfy these constraints::

    >>> print b1
    (x=50.0, width=113.0)
    >>> print b2
    (x=263.0, width=113.0)

    >>> print right_limit.value
    426.0

That is, the smallest window that can accomodate these constraints is 426 pixels
wide. However, if the user makes the window larger, we can still lay out widgets.
We impose a new ``REQUIRED`` constraint with the size of the window::

    right_limit.value = 500
    right_limit_stay = solver.add_constraint(right_limit, strength=REQUIRED)

    >>> print b1
    (x=50.0, width=113.0)
    >>> print b2
    (x=337.0, width=113.0)

    >>> print right_limit.value
    500.0

That is - if the window size is 500 pixels, the layout will compensate by putting
``button2`` a little further to the right. The ``WEAK`` stay on the right limit that
we established at the start is ignored in preference for the ``REQUIRED`` stay.

If the window is then resized again, we can remove the 500 pixel limit, and impose
a new limit::

    solver.remove_constraint(right_limit_stay)

    right_limit.value = 475
    right_limit_stay = solver.add_constraint(right_limit, strength=REQUIRED)
    solver.add_constraint(right_limit_stay)

    >>> print b1
    (x=50.0, width=113.0)
    >>> print b2
    (x=312.0, width=113.0)

    >>> print right_limit.value
    475.0

Again, ``button2`` has been moved, this time to the left, compensating for the
space that was lost by the contracting window size.
