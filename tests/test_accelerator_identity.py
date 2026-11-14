from pathlib import Path
import unittest

from parser.device_identity import _matches


class AcceleratorIdentityTests(unittest.TestCase):

    def test_intel_identical_names(self):
        self.assertTrue(
            _matches("Intel Arc A380", "Intel Arc A380")
        )

    def test_intel_trademark_variation(self):
        self.assertTrue(
            _matches(
                "Intel(R) Arc(TM) A380 Graphics",
                "Intel Arc A380",
            )
        )

    def test_intel_runtime_without_vendor_prefix(self):
        self.assertTrue(
            _matches(
                "Intel(R) Arc(TM) A380 Graphics",
                "Arc A380 Graphics",
            )
        )

    def test_intel_vs_amd_vendor_conflict(self):
        self.assertFalse(
            _matches("Intel Arc A380", "AMD Arc A380")
        )

    def test_intel_vs_nvidia_vendor_conflict(self):
        self.assertFalse(
            _matches(
                "Intel Arc A380 Graphics",
                "NVIDIA Arc A380",
            )
        )

    def test_uhd_graphics_is_not_optional(self):
        self.assertFalse(
            _matches("Intel UHD Graphics 770", "Intel UHD 770")
        )

    def test_uhd_optional_vendor_prefix(self):
        self.assertTrue(
            _matches("Intel UHD Graphics 770", "UHD Graphics 770")
        )

    def test_iris_xe_graphics_is_not_optional(self):
        self.assertFalse(
            _matches("Intel Iris Xe Graphics", "Intel Iris Xe")
        )

    def test_arc_graphics_suffix_is_optional(self):
        self.assertTrue(
            _matches("Intel Arc A380 Graphics", "Intel Arc A380")
        )

    def test_arc_graphics_different_model(self):
        self.assertFalse(
            _matches("Intel Arc A380 Graphics", "Intel Arc A580")
        )

    def test_intel_different_models(self):
        self.assertFalse(
            _matches("Intel Arc A380", "Intel Arc A580")
        )

    def test_amd_different_models(self):
        self.assertFalse(
            _matches(
                "AMD Radeon RX 560",
                "AMD Radeon RX 5600",
            )
        )

    def test_nvidia_different_models(self):
        self.assertFalse(
            _matches(
                "NVIDIA GeForce RTX 3060",
                "NVIDIA GeForce RTX 3070",
            )
        )

    def test_amd_optional_vendor_prefix(self):
        self.assertTrue(
            _matches(
                "AMD Radeon RX 6700 XT",
                "Radeon RX 6700 XT",
            )
        )


if __name__ == "__main__":
    unittest.main()
