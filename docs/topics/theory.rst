Solving constraint systems
==========================

A linear  programming problem is a problem where you have a set of non-
negative, real valued variables (``x[1], x[2], ... x[n]``), and a
series of linear constraints on those variables. These constraints are
expressed as a set of equations of the form:

    ``a[1]x[1] + ... + a[n]x[n] = b``,

    ``a[1]x[1] + ... + a[n]x[n] <= b``, or

    ``a[1]x[1] + ... + a[n]x[n] >= b``,

Given these contraints, the problem is to find the values of x[i] that
minimizes or maximizes the value of the `objective function`:

    ``c + d[1]x[1] + ... + d[n]x[n]``

Cassowary is an algorithm designed to solve linear programming problems of
this type. This library provides the tools to describe a set of constraints,
and then find an optimal solution for that set of constraints.

Concepts
~~~~~~~~

Variables
---------

At the core of the constraint system are the variables in the system.
In the formal mathematical system, these are the ``x[n]`` terms; in Python,
these are rendered as instances of the :class:`Variable` class.

Each variable is named, and can accept

To create a variable, instantiate an instance of :class:`Variable`::

    from cassowary import Variable

    # Create a variable with a default value.
    x1 = Variable('x1')

    # Create a variable with a specific value
    x2 = Variable('x1', 42.0)

Any value provided for the variable is just a starting point. When constraints
are imposed, this value can and will change, subject to the requirements of
the constraints. However, providing an initial value may affect the search process;
if there's an ambiguity in the constraints (i.e., there's more than one
possible solution), the initial value provided to variables will affect which
solution the system converges on.

Expressions
-----------

An expression is the combination of a collection of variables with multipliers
and a constant term. Mathematically, this means:

    ``a[1]x[1] + ... + a[n]x[n]``

In Python, expressions are instances of the :class:`Expression` class. The
simplest expression is a constant::

    from cassowary import Expression

    # A constant: 5
    e1 = Expression(constant=5)

Almost as simple are expressions that involve a single variable::

    from cassowary import Expression, Variable

    x1 = Variable('x1')

    # A simple variable expression: x[1]
    e2 = Expression(x1)

    # A variable expression with a multiplier: x[1]
    e2 = Expression(x1)

    # A variable expression with a multiplier: 3 * x[1]
    e3 = Expression(x1, 3)

    # A variable expression with a multiplier and a constant: 3 * x[1] + 5
    e4 = Expression(x1, 3, 5)

The constructor for an Expression can only include a single variable. To build
an expression with multiple variables, you use arithmetic operators::

    from cassowary import Expression, Variable

    x1 = Variable('x1')
    x2 = Variable('x2')

    # A simple expression with 2 variables: x[1] + x[2]
    e1 = Expression(x1) + Expression(x2)

    # A simple expression with variables and multipliers: 3 * x[1] + 4 * x[2]
    e2 = Expression(x1, 3) + Expression(x2, 4)

    # A simple expression with variables and multipliers, plus a constant term: 3 * x[1] + 4 * x[2] + 5
    e3 = Expression(x1, 3) + Expression(x2, 4) + Expression(constant=5)

    # This last expression could be composed in other ways,
    # with exactly the same result. The constant could be
    # incorporated into either variable expression...
    e3 = Expression(x1, 3, 5) + Expression(x2, 4)
    e3 = Expression(x1, 3) + Expression(x2, 4, 5)

    # ... or split across both.
    e3 = Expression(x1, 3, 2) + Expression(x2, 4, 3)

However, in most circumstances, we don't even need to create an expression -
the mathematical operators have all been set up so that constants and variables
will produce expressions as their are combined::

    from cassowary import Expression, Variable

    x1 = Variable('x1')
    x2 = Variable('x2')

    # Back to the last expression again: 3 * x[1] + 4 * x[2] + 5
    e3 = 3 * x1 + 4 * x2 + 5

The most notable example where you *will* need to create an expression is
when dealing with single term expressions (e.g., ``x[1]``, or ``5``). If you
need to provide



Constraints
-----------


Solvers
-------

