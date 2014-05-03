from .variable import Variable, AbstractVariable
from .error import InternalError
from .utils import approx_equal


class Expression(object):
    def __init__(self, variable=None, value=1.0, constant=0.0):
        assert isinstance(constant, (float, int))
        assert variable is None or isinstance(variable, AbstractVariable)

        self.constant = float(constant)
        self.terms = {}

        if variable:
            self.set_variable(variable, float(value))

    def __repr__(self):
        parts = []
        if not approx_equal(self.constant, 0.0) or self.is_constant:
            parts.append(repr(self.constant))
        for clv, coeff in sorted(self.terms.items(), key=lambda x:repr(x)):
            if approx_equal(coeff, 1.0):
                parts.append(repr(clv))
            else:
                parts.append(repr(coeff) + "*" + repr(clv))
        return ' + '.join(parts)

    @property
    def is_constant(self):
        return not self.terms

    def clone(self):
        expr = Expression(constant=self.constant)
        for clv, value in self.terms.items():
            expr.set_variable(clv, value)
        return expr

    ######################################################################
    # Mathematical operators
    ######################################################################

    def __rmul__(self, x):
        return self.__mul__(x)

    def __mul__(self, x):
        if isinstance(x, Expression):
            if self.is_constant:
                result = x * self.constant
            elif x.is_constant:
                result = self * x.constant
            else:
                raise TypeError('Cannot multiply expression by non-constant')
        elif isinstance(x, Variable):
            if self.is_constant:
                result = Expression(x, self.constant)
            else:
                raise TypeError('Cannot multiply a variable by a non-constant expression')
        elif isinstance(x, (float, int)):
            result = Expression(constant=self.constant * x)
            for clv, value in self.terms.items():
                result.set_variable(clv, value * x)
        else:
            raise TypeError('Cannot multiply expression by object of type %s' % type(x))
        return result

    def __div__(self, x):
        if isinstance(x, (float, int)):
            if approx_equal(x, 0):
                raise ZeroDivisionError()
            result = Expression(constant=self.constant / x)
            for clv, value in self.terms.items():
                result.set_variable(clv, value / x)
        else:
            if x.is_constant:
                result = self / x.constant
            else:
                raise TypeError('Cannot divide expression by non-constant')
        return result

    def __radd__(self, x):
        return self.__add__(x)

    def __add__(self, x):
        if isinstance(x, Expression):
            result = self.clone()
            result.add_expression(x, 1.0)
            return result
        elif isinstance(x, Variable):
            result = self.clone()
            result.add_variable(x, 1.0)
            return result
        elif isinstance(x, (int, float)):
            result = self.clone()
            result.add_expression(Expression(constant=x), 1.0)
            return result
        else:
            raise TypeError('Cannot add object of type %s to expression' % type(x))

    def __rsub__(self, x):
        if isinstance(x, Expression):
            result = self.clone()
            result.multiply(-1.0)
            result.add_expression(x, 1.0)
            return result
        elif isinstance(x, Variable):
            result = self.clone()
            result.multiply(-1.0)
            result.add_variable(x, 1.0)
            return result
        elif isinstance(x, (int, float)):
            result = self.clone()
            result.multiply(-1.0)
            result.add_expression(Expression(constant=x), 1.0)
            return result
        else:
            raise TypeError('Cannot subtract object of type %s from expression' % type(x))

    def __sub__(self, x):
        if isinstance(x, Expression):
            result = self.clone()
            result.add_expression(x, -1.0)
            return result
        elif isinstance(x, Variable):
            result = self.clone()
            result.add_variable(x, -1.0)
            return result
        elif isinstance(x, (int, float)):
            result = self.clone()
            result.add_expression(Expression(constant=x), -1.0)
            return result
        else:
            raise TypeError('Cannot subtract object of type %s from expression' % type(x))

    ######################################################################
    # Mathematical operators
    ######################################################################

    def __eq__(self, other):
        # Import needed here to avoid circular dependencies
        from .constraint import Constraint
        if isinstance(other, (Expression, Variable, float, int)):
            return Constraint(self, Constraint.EQ, other)
        else:
            raise TypeError('Cannot compare expression with object of type %s' % type(other))

    def __lt__(self, other):
        # < and <= are equivalent in the API; it's effectively true
        # due to float arithmetic, and it makes the API a little less hostile,
        # because all the comparison operators exist.
        return self.__le__(other)

    def __le__(self, other):
        # Import needed here to avoid circular dependencies
        from .constraint import Constraint
        if isinstance(other, (Expression, Variable, float, int)):
            return Constraint(self, Constraint.LEQ, other)
        else:
            raise TypeError('Cannot compare expression with object of type %s' % type(other))

    def __gt__(self, other):
        # > and >= are equivalent in the API; it's effectively true
        # due to float arithmetic, and it makes the API a little less hostile,
        # because all the comparison operators exist.
        return self.__ge__(other)

    def __ge__(self, other):
        # Import needed here to avoid circular dependencies
        from .constraint import Constraint
        if isinstance(other, (Expression, Variable, float, int)):
            return Constraint(self, Constraint.GEQ, other)
        else:
            raise TypeError('Cannot compare expression with object of type %s' % type(other))

    ######################################################################
    # Internal mechanisms
    ######################################################################

    def add_expression(self, expr, n=1.0, subject=None, solver=None):
        if isinstance(expr, AbstractVariable):
            expr = Expression(variable=expr)

        self.constant = self.constant + n * expr.constant
        for clv, coeff in expr.terms.items():
            self.add_variable(clv, coeff * n, subject, solver)

    def add_variable(self, v, cd=1.0, subject=None, solver=None):
        # print 'expression: add_variable', v, cd
        coeff = self.terms.get(v)
        if coeff:
            new_coefficient = coeff + cd
            if approx_equal(new_coefficient, 0.0):
                if solver:
                    solver.note_removed_variable(v, subject)
                self.remove_variable(v)
            else:
                self.set_variable(v, new_coefficient)
        else:
            if not approx_equal(cd, 0.0):
                self.set_variable(v, cd)
                if solver:
                    solver.note_added_variable(v, subject)

    def set_variable(self, v, c):
        self.terms[v] = float(c)

    def remove_variable(self, v):
        del self.terms[v]

    def any_pivotable_variable(self):
        if self.is_constant:
            raise InternalError('any_pivotable_variable called on a constant')

        retval = None
        for clv, c in self.terms.items():
            if clv.is_pivotable:
                retval = clv
                break

        return retval

    def substitute_out(self, outvar, expr, subject=None, solver=None):
        multiplier = self.terms.pop(outvar)
        self.constant = self.constant + multiplier  * expr.constant

        for clv, coeff in expr.terms.items():
            old_coefficient = self.terms.get(clv)
            if old_coefficient:
                new_coefficient = old_coefficient + multiplier * coeff
                if approx_equal(new_coefficient, 0):
                    solver.note_removed_variable(clv, subject)
                    del self.terms[clv]
                else:
                    self.set_variable(clv, new_coefficient)
            else:
                self.set_variable(clv, multiplier * coeff)
                if solver:
                    solver.note_added_variable(clv, subject)

    def change_subject(self, old_subject, new_subject):
        self.set_variable(old_subject, self.new_subject(new_subject))

    def multiply(self, x):
        self.constant = self.constant * float(x)
        for clv, value in self.terms.items():
            self.set_variable(clv, value * x)

    def new_subject(self, subject):
        # print "new_subject", subject
        value = self.terms.pop(subject)
        reciprocal = 1.0 / value
        self.multiply(-reciprocal)
        return reciprocal

    def coefficient_for(self, clv):
        return self.terms.get(clv, 0.0)
