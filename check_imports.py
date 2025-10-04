# check_imports.py
import os
import importlib.util

# فقط پوشه اصلی پروژه
project_root = os.path.join(os.getcwd(), "skymind_sim")
broken_imports = []

def try_import(module_path):
    spec = importlib.util.spec_from_file_location("temp_module", module_path)
    try:
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
    except Exception as e:
        broken_imports.append((module_path, str(e)))

for root, _, files in os.walk(project_root):
    for file in files:
        if file.endswith(".py") and "__pycache__" not in root:
            try_import(os.path.join(root, file))

print("\n[ Broken Imports Found ]")
for path, error in broken_imports:
    print(f"{path} --> {error}")

print(f"\nTotal broken imports: {len(broken_imports)}")
