Solving constraint systems
==========================

Constraint solving systems are an algorithmic approach to solving Linear
Programming problems. A linear programming problem is a mathematical problem
where you have a set of non- negative, real valued variables (``x[1], x[2],
... x[n]``), and a series of linear constraints (i.e, no exponential terms) on
those variables. These constraints are expressed as a set of equations of the
form:

    ``a[1]x[1] + ... + a[n]x[n] = b``,

    ``a[1]x[1] + ... + a[n]x[n] <= b``, or

    ``a[1]x[1] + ... + a[n]x[n] >= b``,

Given these contraints, the problem is to find the values of ``x[i]`` that
minimizes or maximizes the value of an **objective function**:

    ``c + d[1]x[1] + ... + d[n]x[n]``

Cassowary is an algorithm designed to solve linear programming problems of
this type. Published in 1997, it now forms the basis fo the UI layout  tools
in OS X Lion, and iOS 6+ (the approach known as `Auto Layout`_). The Cassowary
algorithm (and this implementation of it) provides the tools to describe a set
of constraints, and then find an optimal solution for that set of constraints.

.. _Auto Layout: https://developer.apple.com/library/ios/documentation/userexperience/conceptual/AutolayoutPG/Introduction/Introduction.html

Variables
---------

At the core of the constraint problem are the variables in the system.
In the formal mathematical system, these are the ``x[n]`` terms; in Python,
these are rendered as instances of the :class:`~cassowary.Variable` class.

Each variable is named, and can accept a default value. To create a variable,
instantiate an instance of :class:`~cassowary.Variable`::

    from cassowary import Variable

    # Create a variable with a default value.
    x1 = Variable('x1')

    # Create a variable with a specific value
    x2 = Variable('x1', 42.0)

Any value provided for the variable is just a starting point. When constraints
are imposed, this value can and will change, subject to the requirements of
the constraints. However, providing an initial value may affect the search process;
if there's an ambiguity in the constraints (i.e., there's more than one
possible solution), the initial value provided to variables will affect the solution
on which the system converges.

Constraints
-----------

A constraint is a mathematical equality or inequality that defines the linear
programming system.

A constraint is declared by providing the Python expression that encompasses the
logic described by the constraint. The syntax looks essentially the same as the
raw mathematical expression::

    from cassowary import Variable

    # Create a variable with a default value.
    x1 = Variable('x1')
    x2 = Variable('x2')
    x3 = Variable('x4')

    # Define the constraint
    constraint = x1 + 3 * x2 <= 4 * x3 + 2

In this example, `constraint` holds the defintion for the constraint system.
Although the statement uses the Python comparison operator `<=`, the result is
*not* a boolean. The comparison operators `<=`, `<`, `>=`, `>`, and `==` have
been overridden for instances of :class:`~cassowary.Variable` to enable you to
easily define constraints.

Solvers
-------

The solver is the engine that resolves the linear constraints into a solution.
There are many approaches to this problem, and the development of algorithmic
approaches has been the subject of math and computer science research for over
70 years. Cassowary provides one implementation -- a
:class:`~cassowary.SimplexSolver`, implementing the Simplex algorithm defined
by Dantzig in the 1940s.

The solver takes no arguments during constructions; once constructed, you simply
add constraints to the system.

As a simple example, let's solve the problem posed in Section 2 of the `Badros
& Borning's paper on Cassowary`_. In this problem, we have a 1 dimensional
number line spanning from 0 to 100. There are three points on it (left, middle
and right), with the following constraints:

* The middle point must be halfway between the left and right point;
* The left point must be at least 10 to the left of the right point;
* All points must fall in the range 0-100.

This system can be defined in Python as follows::

    from cassowary import SimplexSolver, Variable

    solver = SimplexSolver()

    left = Variable('left')
    middle = Variable('middle')
    right = Variable('right')

    solver.add_constraint(middle == (left + right) / 2)
    solver.add_constraint(right == left + 10)
    solver.add_constraint(right <= 100)
    solver.add_constraint(left >= 0)

There are an infinite number of possible solutions to this system; if we
interrogate the variables, you'll see that the solver has provided one
possible solution::

    >>> left.value
    90.0
    >>> middle.value
    95.0
    >>> right.value
    100.0

.. _Badros & Borning's paper on Cassowary: http://www.cs.washington.edu/research/constraints/cassowary/cassowary-tr.pdf

Stay constraints
----------------

If we want a particular solution to our left/right/middle problem, we need to
fix a value somewhere. To do this, we add a `Stay` - a special constraint that
says that the value should not be altered.

For example, we might want to enforce the fact that the middle value should
stay at a value of 45. We construct the system as before, but add::

    middle.value = 45.0
    solver.add_stay(middle)

Now when we interrogate the solver, we'll get values that reflect this fixed
point::

    >>> left.value
    40.0
    >>> middle.value
    45.0
    >>> right.value
    50.0

Constraint strength
-------------------

Not all constraints are equal. Some are absolute requirements - for example, a
requirement that all values remain in a specific range. However, other
constraints may be suggestions, rather than hard requirements.

To accomodate this, Cassowary allows all constraints to have a **strength**.
Strength can be one of:

* ``REQUIRED``
* ``STRONG``
* ``MEDIUM``
* ``WEAK``

``REQUIRED`` constraints **must** be satisfied; the remaining strengths will
be satisfied with declining priority.

To define a strength, provide the strength value as an argument when adding
the constraint (or stay)::

    from cassowary import SimplexSolver, Variable, STRONG, WEAK

    solver = SimplexSolver()
    x = Variable('x')

    # Define some non-required constraints
    solver.add_constraint(x <= 100, strength=STRONG)
    solver.add_stay(x, strength=WEAK)

Unless otherwise specified, all constraints are ``REQUIRED``.

Constraint weight
-----------------

If you have multiple constraints of the same strength, you may want to have a
tie-breaker between them. To do this, you can set a **weight**, in addition to
a strength::

    from cassowary import SimplexSolver, Variable, STRONG

    solver = SimplexSolver()
    x = Variable('x')

    # Define some non-required constraints
    solver.add_constraint(x <= 100, strength=STRONG, weight=10)
    solver.add_constraint(x >= 50, strength=STRONG, weight=20)

Editing constraints
-------------------

Any constraint can be removed from a system; just retain the reference provided
when you add the constraint::

    from cassowary import SimplexSolver, Variable

    solver = SimplexSolver()
    x = Variable('x')

    # Define a constraint
    constraint = solver.add_constraint(x <= 100)

    # Remove it again
    solver.remove_constraint(constraint)

Once a constraint is removed, the system will be automatically re-evaluated,
with the possible side effect that the values in the system will change.

But what if you want to change a variable's value without introducing a
new constraint? In this case, you can use an edit context.

Here's an example of an edit context in practice::

    from cassowary import SimplexSolver, Variable

    solver = SimplexSolver()
    x = Variable('x')

    # Add a stay to x - that is, don't change the value.
    solver.add_stay(x)

    # Now, mark x as being editable...
    solver.add_edit_variable(x)

    # ... start and edit context...
    with solver.edit():
        # ... and suggest a new value for the variable.

        solver.suggest_value(x, 42.0)

When the edit context exits, the system will re-evaluate itself, and the
variable will have the new value. However, the variable isn't guaranteed
to have the value you suggested - in this case it will, but if your
constraint system has other constraints, they may affect the value of
the variable after the suggestion has been applied.

All variables in the system will be re-evaluated when you leave the edit
context; however, if you need to force a re-evaluation in the middle of an
edit context, you can do so by calling :meth:`~cassowary.Solver.resolve()`.
