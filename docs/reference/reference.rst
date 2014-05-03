Reference
=========


Variables
---------

.. class:: Variable

.. attribute:: Variable.value


Expressions
-----------


Constraints
-----------


Solvers
-------

.. class:: SimplexSolver

    A class for collecting constraints into a system and solving them.

.. method:: SimplexSolver.add_constraint(constraint)

    Add a new constraint to the solver system.

    Returns the constraint that was added.

.. method:: SimplexSolver.remove_constraint(var)

    Remove a new constraint to the solver system.

    Returns the constraint that was added.

.. method:: SimplexSolver.add_stay(var, strength=REQUIRED, weight=1.0)

    Add a stay constraint to the solver system based on t

    Returns the constraint that was added.

.. method:: SimplexSolver.add_edit_var(var)

.. method:: SimplexSolver.remove_edit_var(var)

.. method:: SimplexSolver.begin_edit()

.. method:: SimplexSolver.end_edit()

.. method:: SimplexSolver.suggest_value(var, value)
