import unittest
# Load this project's module explicitly, including when invoked from repository root.
import importlib.util as _import_util
from pathlib import Path as _Path
import sys as _sys
_spec = _import_util.spec_from_file_location(
    "sunil_agents_" + _Path(__file__).parent.name, _Path(__file__).with_name("main.py"))
_main = _import_util.module_from_spec(_spec)
_sys.modules[_spec.name] = _main
_spec.loader.exec_module(_main)
simulate = _main.simulate
retry = _main.retry

class RetryTests(unittest.TestCase):
    def test_transient_then_success(self):
        result=simulate(["transient","transient","success"])
        self.assertEqual(result["attempts"],3)
        self.assertEqual(result["delays"],[0.25,0.5])
    def test_permanent_does_not_retry(self):
        result=simulate(["permanent","success"])
        self.assertEqual(result["attempts"],1);self.assertEqual(result["delays"],[])
    def test_attempt_limit_has_no_final_sleep(self):
        result=simulate(["transient"],max_attempts=3)
        self.assertEqual(result["attempts"],3);self.assertEqual(len(result["delays"]),2)
    def test_delay_budget_prevents_next_attempt(self):
        result=simulate(["transient"],delay_budget=0.1)
        self.assertEqual(result["attempts"],1);self.assertEqual(result["delays"],[])
    def test_invalid_policy(self):
        with self.assertRaises(ValueError):retry(lambda:1,lambda _:None,max_attempts=0)

if __name__ == "__main__":unittest.main()
