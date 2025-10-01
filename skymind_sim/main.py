# skymind_sim/main.py

from skymind_sim.core.simulation import Simulation
from skymind_sim.core.environment import Environment
from skymind_sim.core.drone import Drone
from skymind_sim.core.visualizer import Visualizer

def main():
    """
    Main function to set up and run the drone simulation.
    """
    print("Simulation setup starting...")
    
    # 1. Setup Environment
    env = Environment(width=800, height=600)

    # 2. Setup Visualizer using environment dimensions
    visualizer = Visualizer(env.width, env.height)

    # 3. Setup Simulation with a fixed time step and duration
    # end_time is the total duration in seconds.
    sim = Simulation(environment=env, visualizer=visualizer, end_time=120.0)

    # 4. Create Drones with different battery parameters for testing
    # Drone 1: Standard battery, should complete its mission.
    drone1 = Drone(drone_id="Alpha-1", position=[50, 50], speed=50, 
                   battery_capacity=1000.0, consumption_rate=2.0)
    
    # Drone 2: High consumption rate, might not make it.
    drone2 = Drone(drone_id="Bravo-2", position=[750, 550], speed=60, 
                   battery_capacity=500.0, consumption_rate=15.0)
                   
    # Drone 3: Very low starting battery, will definitely stop early.
    drone3 = Drone(drone_id="Charlie-3", position=[600, 250], speed=40,
                   battery_capacity=80.0, consumption_rate=5.0)

    # 5. Set Missions for each drone
    drone1.set_mission(path=[[200, 200], [50, 400], [300, 50]])
    drone2.set_mission(path=[[400, 400], [100, 100]])
    drone3.set_mission(path=[[400, 100], [100, 300]]) # A longer path to ensure it fails

    # 6. Add drones to the simulation
    sim.add_drone(drone1)
    sim.add_drone(drone2)
    sim.add_drone(drone3)

    # 7. Run the simulation
    print("Simulation setup complete. Running...")
    sim.run()

    # 8. Cleanly close the visualizer window
    sim.close()

    print("Simulation finished.")


if __name__ == "__main__":
    main()
