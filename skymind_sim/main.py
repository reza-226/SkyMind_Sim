# skymind_sim/main.py

from skymind_sim.layer_1_simulation.simulation import Simulation
import time

def run_simulation_in_terminal():
    """
    A simple function to test the simulation logic without any graphics.
    This demonstrates that Layer 1 can run independently of Layer 0.
    """
    print("=========================================")
    print("=      SkyMind_Sim Terminal Runner      =")
    print("=========================================")

    # 1. Create a simulation instance
    sim = Simulation()

    # 2. Setup the world
    sim.setup_world()

    # 3. Start the simulation
    sim.start()

    # 4. Run the simulation for a few steps
    time_step = 0.5  # Simulate a time step of 0.5 seconds
    num_steps = 5

    for i in range(num_steps):
        print(f"\n[Main Loop - Step {i+1}/{num_steps}]")
        sim.update(dt=time_step)

        # Get and print the world state after the update
        world_state = sim.get_world_state()
        print("Current World State:")
        print(f"  Time: {world_state['time']:.2f}s")
        for drone_state in world_state['drones']:
            print(f"  - Drone {drone_state['id']} at {drone_state['position']}")

        time.sleep(1) # Pause for 1 second to make the output readable

    # 5. Stop the simulation
    sim.stop()
    print("\n=========================================")
    print("=         Simulation Finished         =")
    print("=========================================")


if __name__ == "__main__":
    run_simulation_in_terminal()
