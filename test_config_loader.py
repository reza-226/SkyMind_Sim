# test_config_loader.py

import sys
from pathlib import Path

# Add the project root to the Python path to allow imports from skymind_sim
# This is a common pattern for test scripts located at the project root.
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))

from skymind_sim.utils.config_loader import ConfigLoader

def run_test():
    """
    A simple test function to validate the ConfigLoader functionality.
    """
    print("--- Starting ConfigLoader Test ---")
    
    # 1. Get the singleton instance
    config_loader = ConfigLoader()
    
    # Check if it's a true singleton (optional but good practice)
    config_loader_2 = ConfigLoader()
    if id(config_loader) == id(config_loader_2):
        print("✅ Singleton test passed: Both instances are the same object.")
    else:
        print("❌ Singleton test failed!")
        return

    # 2. Define the config directory path
    config_directory = project_root / 'data' / 'config'
    
    # 3. Load configurations from the directory
    try:
        config_loader.load_from_directory(config_directory)
    except Exception as e:
        print(f"❌ Test failed during loading: {e}")
        return

    # 4. Test retrieving values
    print("\n--- Testing 'get' method ---")
    
    # Test case 1: Get window width (expected: 1280)
    width = config_loader.get('window.width')
    print(f"Window width: {width} (Expected: 1280)")
    assert width == 1280, "Window width test failed!"

    # Test case 2: Get target FPS (expected: 60)
    fps = config_loader.get('simulation.target_fps')
    print(f"Target FPS: {fps} (Expected: 60)")
    assert fps == 60, "Target FPS test failed!"

    # Test case 3: Get grid line color (expected: [50, 50, 50])
    line_color = config_loader.get('grid.line_color')
    print(f"Grid line color: {line_color} (Expected: [50, 50, 50])")
    assert line_color == [50, 50, 50], "Grid line color test failed!"

    # Test case 4: Get a nested non-existent key with a default value
    non_existent = config_loader.get('window.non_existent_key', 'default_value')
    print(f"Non-existent key: {non_existent} (Expected: 'default_value')")
    assert non_existent == 'default_value', "Default value test failed!"
    
    # Test case 5: Get a non-existent primary key
    no_module = config_loader.get('database.host', 'localhost')
    print(f"Non-existent module: {no_module} (Expected: 'localhost')")
    assert no_module == 'localhost', "Non-existent module test failed!"

    print("\n--- All ConfigLoader tests passed successfully! ---")


if __name__ == "__main__":
    run_test()
