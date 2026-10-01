#!/usr/bin/env python3
"""Run the generated DeviceDB artifacts in dependency order."""
from __future__ import annotations
import subprocess
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
STEPS = [
    "generate_function_catalog.py",
    "generate_learning_feature_order.py",
    "generate_learning_features_by_device_type.py",
    "generate_learning_ui_templates.py",
    "generate_ui_template_index.py",
]


def main() -> int:
    for script in STEPS:
        path = TOOLS / script
        print(f"\n=== Running {script} ===", flush=True)
        subprocess.run([sys.executable, str(path)], check=True)
    print("\nAll DeviceDB generated files, learning UI templates and UI-template index are up to date.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
