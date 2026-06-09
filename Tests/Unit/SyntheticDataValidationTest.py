import unittest

from CapacityEngine.Domain.Exceptions import ValidationError
from CapacityEngine.Domain.SyntheticData import (
    ValidateDays,
    ValidateLoadId,
    ValidateProfile,
    ValidateSeed,
    ValidateTestLoad,
    ValidateVolume,
    BuildToolValidationResult,
    TestLoad,
)


class SyntheticDataValidationTest(unittest.TestCase):
    def test_validate_load_id_rechaza_valores_inseguros(self):
        for Value in ["", "../unsafe", "bad value", "x" * 65]:
            with self.assertRaises(ValidationError):
                ValidateLoadId(Value)

    def test_validate_profile_volume_days_seed(self):
        self.assertEqual(ValidateProfile("mixed"), "mixed")
        self.assertEqual(ValidateVolume("small"), "small")
        self.assertEqual(ValidateDays("90"), 90)
        self.assertEqual(ValidateSeed("123"), 123)
        with self.assertRaises(ValidationError):
            ValidateProfile("invalido")
        with self.assertRaises(ValidationError):
            ValidateVolume("xlarge")
        with self.assertRaises(ValidationError):
            ValidateDays("0")
        with self.assertRaises(ValidationError):
            ValidateSeed("-1")

    def test_test_load_transiciones_validas(self):
        Load = TestLoad.Create("Demo001", "mixed", "small")
        self.assertEqual(Load.Status, "Planned")
        Running = Load.WithStatus("Running")
        Succeeded = Running.WithStatus("Succeeded")
        Deleted = Succeeded.WithStatus("Deleted")
        self.assertEqual(Deleted.Status, "Deleted")

    def test_test_load_transicion_invalida(self):
        Load = TestLoad.Create("Demo002", "mixed", "small")
        with self.assertRaises(ValidationError):
            Load.WithStatus("Deleted")

    def test_validate_test_load_requiere_marca_de_prueba(self):
        Load = TestLoad.Create("Demo003", "normal", "small")
        ValidateTestLoad(Load)
        Unsafe = TestLoad("Demo004", "normal", "small", IsTestData=False)
        with self.assertRaises(ValidationError):
            ValidateTestLoad(Unsafe)

    def test_tool_validation_result(self):
        Result = BuildToolValidationResult("Grafana", "http://localhost:3000", "HTTP", True, "OK")
        self.assertEqual(Result.Status, "Available")
        self.assertEqual(Result.ToolName, "Grafana")


if __name__ == "__main__":
    unittest.main()
