from unittest import TestCase

from cassowary import Variable, Constraint, SimplexSolver, STRONG, WEAK

# Internals
from cassowary.expression import Expression


class ConstraintTestCase(TestCase):
    def test_from_constant(self):
        "Constraint can be constructed from a constant expression"
        ex = Expression(constant=10)

        # Constant value is ported to a float.
        self.assertIsInstance(ex.constant, float)
        self.assertAlmostEqual(ex.constant, 10.0)

        c1 = Constraint(ex)

        self.assertEqual(c1.expression, ex)
        self.assertFalse(c1.is_inequality)

        c2 = Constraint(10)

        self.assertAlmostEqual(c2.expression.constant, 10)
        self.assertTrue(c2.expression.is_constant)
        self.assertFalse(c2.is_inequality)

    def test_variable_expression(self):
        "Variable expressions can be constructed"
        x = Variable('x', 167)
        y = Variable('y', 2)
        cly = Expression(y)
        cly.add_expression(x)

    # def test_equation_from_variable_expression(self):
    #     "Constraints can be constructed from variables and expressions"
    #     x = Variable(name='x', value=167)
    #     cly = Expression(constant=2)
    #     eq = Constraint(x, Constraint.EQ, cly)

    def test_strength(self):
        "Solvers should handle strengths correctly"
        solver = SimplexSolver()
        x = Variable(name='x', value=10)
        y = Variable(name='y', value=20)
        z = Variable(name='z', value=1)
        w = Variable(name='w', value=1)

        # Default weights.
        e0 = Constraint(x, Constraint.EQ, y)
        solver.add_stay(y)

        solver.add_constraint(e0)
        self.assertAlmostEqual(x.value, 20.0)
        self.assertAlmostEqual(y.value, 20.0)

        # Add a weak constraint.
        e1 = Constraint(x, Constraint.EQ, z, strength=WEAK)
        solver.add_stay(x)
        solver.add_constraint(e1)
        self.assertAlmostEqual(x.value, 20.0)
        self.assertAlmostEqual(z.value, 20.0)

        # Add a strong constraint.
        e2 = Constraint(z, Constraint.EQ, w, strength=STRONG)
        solver.add_stay(w)
        solver.add_constraint(e2)
        self.assertAlmostEqual(w.value, 1.0)
        self.assertAlmostEqual(z.value, 1.0)

    def test_numbers_in_place_of_variables(self):
        v = Variable(name='v', value=22)
        eq = Constraint(v, Constraint.EQ, 5)
        self.assertEqual(eq.expression, 5 - v)

    def test_equations_in_place_of_variables(self):
        e = Expression(constant=10)
        v = Variable(name='v', value=22)
        eq = Constraint(e, Constraint.EQ, v)

        self.assertEqual(eq.expression, 10 - v)

    def test_works_with_nested_expressions(self):
        e1 = Expression(constant=10)
        e2 = Expression(Variable(name='z', value=10), 2, 4)
        eq = Constraint(e1, Constraint.EQ, e2)

        self.assertEqual(eq.expression, e1 - e2)

    def test_inequality_expression_instantiation(self):
        e = Expression(constant = 10)
        ieq = Constraint(e)
        self.assertEqual(ieq.expression, e)

    def test_operator_arguments_to_inequality(self):
        v1 = Variable(name='v1', value=10)
        v2 = Variable(name='v2', value=5)
        ieq = Constraint(v1, Constraint.GEQ, v2)
        self.assertEqual(ieq.expression, v1 - v2)

        ieq = Constraint(v1, Constraint.LEQ, v2)
        self.assertEqual(ieq.expression, v2 - v1)

    def test_expression_with_variable_and_operators(self):
        v = Variable(name='v', value=10)
        ieq = Constraint(v, Constraint.GEQ, 5)
        self.assertEqual(ieq.expression, v - 5)

        ieq = Constraint(v, Constraint.LEQ, 5)
        self.assertEqual(ieq.expression, 5 - v)

    def test_expression_with_reused_variables(self):
        e1 = Expression(constant=10)
        e2 = Expression(Variable(name='c', value=10), 2, 4)
        ieq = Constraint(e1, Constraint.GEQ, e2)

        self.assertEqual(ieq.expression, e1 - e2)

        ieq = Constraint(e1, Constraint.LEQ, e2)
        self.assertEqual(ieq.expression, e2 - e1)

    def test_constructor_with_variable_operator_expression_args(self):
        v = Variable(name='v', value=10)
        e = Expression(Variable(name='x', value=5), 2, 4)
        ieq = Constraint(v, Constraint.GEQ, e)

        self.assertEqual(ieq.expression, v - e)

        ieq = Constraint(v, Constraint.LEQ, e)
        self.assertEqual(ieq.expression, e - v)

    def test_constructor_with_variable_operator_expression_args2(self):
        v = Variable(name='v', value=10)
        e = Expression(Variable(name='x', value=5), 2, 4)
        ieq = Constraint(e, Constraint.GEQ, v)
        self.assertEqual(ieq.expression, e - v)

        ieq = Constraint(e, Constraint.LEQ, v)
        self.assertEqual(ieq.expression, v - e)
