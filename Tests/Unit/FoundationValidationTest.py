import unittest

from CapacityEngine.Application.Security import AuthenticatedContext, RequireAuthenticated, RequireRole


class FoundationValidationTest(unittest.TestCase):
    def test_requires_authentication_and_role(self):
        with self.assertRaises(PermissionError):
            RequireAuthenticated(None)
        RequireRole(AuthenticatedContext("UserA", ("Operator",)), {"Operator"})


if __name__ == "__main__":
    unittest.main()
