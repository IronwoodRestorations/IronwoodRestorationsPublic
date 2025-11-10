import importlib
import subprocess
import sys

# Dependencies
dependencies = [("reportlab", True)]
mainScript = "custom_dtc_builder.py"

# Loop for each dependency
for dep, is_critical in dependencies:
    try:
        importlib.import_module(dep)
        print(f"'{dep}' is already installed.")
    except ImportError:
        print(f"'{dep}' is not installed.")
        # Warning for critical dependencies
        if is_critical:
            result = f"Not installing '{dep}' means it will not be able to print to PDF"
        else:
            result = f"'{dep}' is optional, skipping may reduce functionality"
        install = input(f"Do you want to install '{dep}' now? (y/n): ").lower()
        if install == "n":
            installDoubleCheck = input(f"{result}, are you sure you want to skip installation of '{dep}'? (y/n): ").lower()
            if installDoubleCheck != "y":
                install = "y"
            else:
                print(f"Install of '{dep}' skipped")
        elif install == "y":
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
            except Exception as e:
                print(f"'{dep}' failed to install. Exception: {e}")
                quit()
            print(f"'{dep}' successfully installed. You may now run main project's python script: '{mainScript}'")
        else:
            print(f"Install of '{dep}' skipped")
