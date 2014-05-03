from .error import InternalError
from .expression import Expression
from .strength import REQUIRED, STRONG, repr_strength
from .variable import Variable


class AbstractConstraint(object):
    def __init__(self, strength, weight=1.0):
        self.strength = strength
        self.weight = weight
        self.is_edit_constraint = False
        self.is_inequality = False
        self.is_stay_constraint = False

    @property
    def is_required(self):
        return self.strength == REQUIRED

    def __repr__(self):
        return u'%s:{%s}(%s)' % (repr_strength(self.strength), self.weight, self.expression)

class EditConstraint(AbstractConstraint):
    def __init__(self, variable, strength=STRONG, weight=1.0):
        super(EditConstraint, self).__init__(strength, weight)
        self.variable = variable
        self.expression = Expression(variable, -1.0, variable.value)
        self.is_edit_constraint = True

    def __repr__(self):
        return u'edit:%s' % super(EditConstraint, self).__repr__()


class StayConstraint(AbstractConstraint):
    def __init__(self, variable, strength=STRONG, weight=1.0):
        super(StayConstraint, self).__init__(strength, weight)
        self.variable = variable
        self.expression = Expression(variable, -1.0, variable.value)
        self.is_stay_constraint=True

    def __repr__(self):
        return u'stay:%s' % super(StayConstraint, self).__repr__()


class Constraint(AbstractConstraint):
    LEQ = -1
    EQ = 0
    GEQ = 1

    def __init__(self, param1, operator=EQ, param2=None, strength=REQUIRED, weight=1.0):
        """Define a new linear constraint.

        param1 may be an expression or variable
        param2 may be an expression, variable, or constant, or may be ommitted entirely.
        If param2 is specified, the operator must be either LEQ, EQ, or GEQ
        """
        if isinstance(param1, Expression):
            if param2 is None:
                super(Constraint, self).__init__(strength=strength, weight=weight)
                self.expression = param1
            elif isinstance(param2, Expression):
                super(Constraint, self).__init__(strength=strength, weight=weight)
                self.expression = param1.clone()
                if operator == self.LEQ:
                    self.expression.multiply(-1.0)
                    self.expression.add_expression(param2, 1.0)
                elif operator == self.EQ:
                    self.expression.add_expression(param2, -1.0)
                elif operator == self.GEQ:
                    self.expression.add_expression(param2, -1.0)
                else:
                    raise InternalError("Invalid operator in Constraint constructor")
            elif isinstance(param2, Variable):
                super(Constraint, self).__init__(strength=strength, weight=weight)
                self.expression = param1.clone()
                if operator == self.LEQ:
                    self.expression.multiply(-1.0)
                    self.expression.add_variable(param2, 1.0)
                elif operator == self.EQ:
                    self.expression.add_variable(param2, -1.0)
                elif operator == self.GEQ:
                    self.expression.add_variable(param2, -1.0)
                else:
                    raise InternalError("Invalid operator in Constraint constructor")

            elif isinstance(param2, (float, int)):
                super(Constraint, self).__init__(strength=strength, weight=weight)
                self.expression = param1.clone()
                if operator == self.LEQ:
                    self.expression.multiply(-1.0)
                    self.expression.add_expression(Expression(constant=param2), 1.0)
                elif operator == self.EQ:
                    self.expression.add_expression(Expression(constant=param2), -1.0)
                elif operator == self.GEQ:
                    self.expression.add_expression(Expression(constant=param2), -1.0)
                else:
                    raise InternalError("Invalid operator in Constraint constructor")
            else:
                raise InternalError("Invalid parameters to Constraint constructor")

        elif isinstance(param1, Variable):
            if param2 is None:
                super(Constraint, self).__init__(strength=strength, weight=weight)
                self.expression = Expression(param1)
            elif isinstance(param2, Expression):
                super(Constraint, self).__init__(strength=strength, weight=weight)
                self.expression = param2.clone()
                if operator == self.LEQ:
                    self.expression.add_variable(param1, -1.0)
                elif operator == self.EQ:
                    self.expression.add_variable(param1, -1.0)
                elif operator == self.GEQ:
                    self.expression.multiply(-1.0)
                    self.expression.add_variable(param1, 1.0)
                else:
                    raise InternalError("Invalid operator in Constraint constructor")

            elif isinstance(param2, Variable):
                super(Constraint, self).__init__(strength=strength, weight=weight)
                self.expression = Expression(param2)
                if operator == self.LEQ:
                    self.expression.add_variable(param1, -1.0)
                elif operator == self.EQ:
                    self.expression.add_variable(param1, -1.0)
                elif operator == self.GEQ:
                    self.expression.multiply(-1.0)
                    self.expression.add_variable(param1, 1.0)
                else:
                    raise InternalError("Invalid operator in Constraint constructor")

            elif isinstance(param2, (float, int)):
                super(Constraint, self).__init__(strength=strength, weight=weight)
                self.expression = Expression(constant=param2)
                if operator == self.LEQ:
                    self.expression.add_variable(param1, -1.0)
                elif operator == self.EQ:
                    self.expression.add_variable(param1, -1.0)
                elif operator == self.GEQ:
                    self.expression.multiply(-1.0)
                    self.expression.add_variable(param1, 1.0)
                else:
                    raise InternalError("Invalid operator in Constraint constructor")
            else:
                raise InternalError("Invalid parameters to Constraint constructor")

        elif isinstance(param1, (float, int)):
            if param2 is None:
                super(Constraint, self).__init__(strength=strength, weight=weight)
                self.expression = Expression(constant=param1)

            elif isinstance(param2, Expression):
                super(Constraint, self).__init__(strength=strength, weight=weight)
                self.expression = param2.clone()
                if operator == self.LEQ:
                    self.expression.add_expression(Expression(constant=param1), -1.0)
                elif operator == self.EQ:
                    self.expression.add_expression(Expression(constant=param1), -1.0)
                elif operator == self.GEQ:
                    self.expression.multiply(-1.0)
                    self.expression.add_expression(Expression(constant=param1), 1.0)
                else:
                    raise InternalError("Invalid operator in Constraint constructor")

            elif isinstance(param2, Variable):
                super(Constraint, self).__init__(strength=strength, weight=weight)
                self.expression = Expression(constant=param1)
                if operator == self.LEQ:
                    self.expression.add_variable(param2, -1.0)
                elif operator == self.EQ:
                    self.expression.add_variable(param2, -1.0)
                elif operator == self.GEQ:
                    self.expression.multiply(-1.0)
                    self.expression.add_variable(param2, 1.0)
                else:
                    raise InternalError("Invalid operator in Constraint constructor")

            elif isinstance(param2, (float, int)):
                raise InternalError("Cannot create an inequality between constants")

            else:
                raise InternalError("Invalid parameters to Constraint constructor")
        else:
            raise InternalError("Invalid parameters to Constraint constructor")

        self.is_inequality = operator != self.EQ

    def clone(self):
        c = Constraint(self.expression, strength=self.strength, weight=self.weight)
        c.is_inequality = self.is_inequality
        return c
