from unittest import TestCase

# Internals
from cassowary.tableau import Tableau


class TableauTestCase(TestCase):

    def test_tableau(self):
        "A Tableau can be constructed"
        tableau = Tableau()

        self.assertEqual(len(tableau.columns), 0)
        self.assertEqual(len(tableau.rows), 0)
        self.assertEqual(len(tableau.infeasible_rows), 0)
        self.assertEqual(len(tableau.external_rows), 0)
        self.assertEqual(len(tableau.external_parametric_vars), 0)
