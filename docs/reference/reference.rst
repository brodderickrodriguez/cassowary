.. module:: cassowary

Reference
=========


Variables
---------

.. class:: Variable

.. attribute:: Variable.value

    The current value of the variable. If the variable is part of a constraint,
    the value will be updated as constraints are applied and changed.

.. method:: Variable.__init__(name, value=0.0)

    Define a new variable. Value is optional, but will affect the constraint
    solving process if multiple solutions are possible.

Solvers
-------

.. class:: SimplexSolver

    A class for collecting constraints into a system and solving them.

.. method:: SimplexSolver.add_constraint(constraint, strength=REQUIRED, weight=1.0)

    Add a new constraint to the solver system. A constraint is a mathematical
    expression involving 1 or more variables, and an equality or inequality.

    ``strength`` is optional; by default, all constraints are added as
    ``REQUIRED`` constraints.

    ``weight`` is optional; by default, all constraints have an equal weight
    of 1.0.

    Returns the constraint that was added.

.. method:: SimplexSolver.remove_constraint(var)

    Remove a new constraint to the solver system.

    Returns the constraint that was added.

.. method:: SimplexSolver.add_stay(var, strength=REQUIRED, weight=1.0)

    Add a stay constraint to the solver system for the current value of
    the variable ``var``.

    ``strength`` is optional; by default, all constraints are added as
    ``REQUIRED`` constraints.

    ``weight`` is optional; by default, all constraints have an equal weight
    of 1.0.

    Returns the constraint that was added.

.. method:: SimplexSolver.add_edit_var(var)

    Mark a variable as being an edit variable. This allows you to
    suggest values for the variable once you start an edit context.

.. method:: SimplexSolver.remove_edit_var(var)

    Remove the variable from the list of edit variables.

.. method:: SimplexSolver.edit()

    Returns a context manager that can be used to manage the edit process.

.. method:: SimplexSolver.suggest_value(var, value)

    Suggest a new value for a edit variable.

    This method can only be invoked while inside an edit context.
    ``var`` must be a variable that has been identified as an edit
    variable in the current edit context.

.. method:: SimplexSolver.resolve()

    Force a solver system to resolve any ambiguities. Useful when
    introducing edit constraints.
