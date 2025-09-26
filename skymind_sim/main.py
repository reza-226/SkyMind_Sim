# skymind_sim/main.py

# کلاس Drone را از ماژول drone در همان پکیج وارد می‌کنیم.
# نقطه قبل از core به معنای "از داخل همین پکیج (skymind_sim)" است.
from .core.drone import Drone 

# from .core.simulation import Simulation
# from .core.environment import Environment

def run_simulation():
    """
    نقطه ورود اصلی برای اجرای شبیه‌سازی.
    """
    print("=========================================")
    print("  Initializing SkyMind Simulation...")
    print("=========================================")

    # -- ایجاد و تست یک نمونه از پهپاد --
    print("\n--- Testing Drone Class ---")
    
    # یک پهپاد جدید با شناسه 'Alpha-1' در موقعیت (0, 0) ایجاد می‌کنیم.
    try:
        drone1 = Drone(drone_id="Alpha-1", start_position=(0, 0))
        
        # وضعیت اولیه پهپاد را با استفاده از متد __str__ که خودمان نوشتیم، چاپ می‌کنیم.
        print(f"Successfully created drone: {drone1}")

        # دستور حرکت به پهپاد می‌دهیم.
        drone1.move_to(new_position=(10, 15))

        # وضعیت نهایی پهپاد را گزارش می‌کنیم.
        print("\nFinal status check:")
        drone1.report_status()

    except ValueError as e:
        print(f"[ERROR] Failed to create drone: {e}")


    print("\n[INFO] Basic drone class functionality is working. Ready for the next step!")


if __name__ == "__main__":
    run_simulation()
