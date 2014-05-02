from .utils import approx_equal


class AbstractVariable(object):
    def __init__(self, name):
        self.name = name
        self.is_dummy = False
        self.is_external = False
        self.is_pivotable = False
        self.is_restricted = False

    def __rmul__(self, x):
        return self.__mul__(x)

    def __mul__(self, x):
        from .expression import Expression
        if isinstance(x, (float, int)):
            return Expression(self, x)
        elif isinstance(x, Expression):
            if x.is_constant:
                return Expression(self, value=x.constant)
            else:
                raise TypeError('Cannot multiply variable by non-constant expression')
        else:
            raise TypeError('Cannot multiply variable by object of type %s' % type(x))

    def __div__(self, x):
        from .expression import Expression
        if isinstance(x, (float, int)):
            if approx_equal(x, 0):
                raise ZeroDivisionError()
            return Expression(self, 1.0 / x)
        elif isinstance(x, Expression):
            if x.is_constant:
                return Expression(self, value=1.0/x.constant)
            else:
                raise TypeError('Cannot add non-constant expression to variable')
        else:
            raise TypeError('Cannot divide variable by object of type %s' % type(x))

    def __radd__(self, x):
        return self.__add__(x)

    def __add__(self, x):
        from .expression import Expression
        if isinstance(x, (int, float)):
            return Expression(self, constant=x)
        elif isinstance(x, Expression):
            return Expression(self) + x
        elif isinstance(x, AbstractVariable):
            return Expression(self) + Expression(x)
        else:
            raise TypeError('Cannot add object of type %s to expression' % type(x))

    def __rsub__(self, x):
        from .expression import Expression
        if isinstance(x, (int, float)):
            return Expression(self, -1.0, constant=x)
        elif isinstance(x, Expression):
            return x - Expression(self)
        elif isinstance(x, AbstractVariable):
            return Expression(x) - Expression(self)
        else:
            raise TypeError('Cannot subtract variable from object of type %s' % type(x))

    def __sub__(self, x):
        from .expression import Expression
        if isinstance(x, (int, float)):
            return Expression(self, constant=-x)
        elif isinstance(x, Expression):
            return Expression(self) - x
        elif isinstance(x, AbstractVariable):
            return Expression(self) - Expression(x)
        else:
            raise TypeError('Cannot subtract object of type %s from variable' % type(x))


class Variable(AbstractVariable):
    def __init__(self, name, value=0.0):
        super(Variable, self).__init__(name)
        self.value = float(value)
        self.is_external = True

    def __repr__(self):
        return '%s[%s]' % (self.name, self.value)


class DummyVariable(AbstractVariable):
    def __init__(self, number):
        super(DummyVariable, self).__init__(name='d%s' % (number))
        self.is_dummy = True
        self.is_restricted = True

    def __repr__(self):
        return '%s:dummy' % self.name


class ObjectiveVariable(AbstractVariable):
    def __init__(self, name):
        super(ObjectiveVariable, self).__init__(name)

    def __repr__(self):
        return '%s:obj' % self.name


class SlackVariable(AbstractVariable):
    def __init__(self, prefix, number):
        super(SlackVariable, self).__init__(name='%s%s' % (prefix, number))
        self.is_pivotable = True
        self.is_restricted = True

    def __repr__(self):
        return '%s:slack' % self.name
