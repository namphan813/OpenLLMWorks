import ast
from pathlib import Path
import re
import unittest


RUNNER_PATH = (
    Path(__file__).resolve().parents[1]
    / "runner"
    / "run_benchmark.py"
)


def load_matching_function():
    source = RUNNER_PATH.read_text(encoding="utf-8-sig")
    tree = ast.parse(source)

    names = {
        "normalize_accelerator_name",
        "match_selected_runtime_device",
    }
    functions = [
        node for node in tree.body
        if isinstance(node, ast.FunctionDef)
        and node.name in names
    ]

    if len(functions) != len(names):
        raise RuntimeError("Expected Runner functions not found.")

    namespace = {"re": re}

    exec(
        compile(
            ast.Module(body=functions, type_ignores=[]),
            str(RUNNER_PATH),
            "exec",
        ),
        namespace,
    )

    return namespace["match_selected_runtime_device"]


class RunnerDeviceMatchingTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.match = staticmethod(load_matching_function())

    def matches(self, selected, runtime):
        return self.match(
            {"name": selected},
            [{"device_id": "vulkan0", "name": runtime}],
        )

    def test_intel_arc_graphics_suffix(self):
        result = self.matches(
            "Intel(R) Arc(TM) A380 Graphics",
            "Intel Arc A380",
        )
        self.assertEqual(result["device_id"], "vulkan0")

    def test_explicit_vendor_conflict(self):
        with self.assertRaises(RuntimeError):
            self.matches("Intel Arc A380", "AMD Arc A380")

    def test_intel_different_models(self):
        with self.assertRaises(RuntimeError):
            self.matches("Intel Arc A380", "Intel Arc A580")

    def test_amd_different_models(self):
        with self.assertRaises(RuntimeError):
            self.matches(
                "AMD Radeon RX 560",
                "AMD Radeon RX 5600",
            )

    def test_nvidia_optional_vendor_prefix(self):
        result = self.matches("NVIDIA RTX 3060", "RTX 3060")
        self.assertEqual(result["device_id"], "vulkan0")

    def test_select_intel_among_multiple_vulkan_devices(self):
        result = self.match(
            {"name": "Intel(R) Arc(TM) A380 Graphics"},
            [
                {
                    "device_id": "vulkan0",
                    "name": "AMD Radeon RX 6700 XT",
                },
                {
                    "device_id": "vulkan1",
                    "name": "Intel Arc A380",
                },
            ],
        )
        self.assertEqual(result["device_id"], "vulkan1")

    def test_reject_ambiguous_runtime_matches(self):
        with self.assertRaisesRegex(
            RuntimeError,
            "matched multiple",
        ):
            self.match(
                {"name": "Intel Arc A380"},
                [
                    {
                        "device_id": "vulkan0",
                        "name": "Intel Arc A380",
                    },
                    {
                        "device_id": "vulkan1",
                        "name": "Intel Arc A380 Graphics",
                    },
                ],
            )

    def test_reject_missing_model(self):
        with self.assertRaises(RuntimeError):
            self.matches("Intel Arc A580", "Intel Arc A380")

    def test_iris_xe_suffix_remains_strict(self):
        with self.assertRaises(RuntimeError):
            self.matches(
                "Intel Iris Xe Graphics",
                "Intel Iris Xe",
            )


if __name__ == "__main__":
    unittest.main()
