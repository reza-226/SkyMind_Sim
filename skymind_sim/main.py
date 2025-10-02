# skymind_sim/main.py
import pygame

# وارد کردن کلاس‌های اصلی از لایه‌های مربوطه
from skymind_sim.layer_1_simulation.simulation import Simulation
from skymind_sim.layer_0_presentation.renderer import Renderer

# تنظیمات اصلی صفحه نمایش
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60  # فریم بر ثانیه برای نمایش

def main_game_loop():
    print("="*41 + "\n=       SkyMind_Sim Initializing        =\n" + "="*41)
    
    # 1. مقداردهی اولیه لایه شبیه‌سازی
    sim = Simulation()
    sim.setup_world()
    
    # 2. مقداردهی اولیه لایه نمایش
    renderer = Renderer(SCREEN_WIDTH, SCREEN_HEIGHT)
    
    # 3. ایجاد ساعت برای کنترل نرخ فریم و محاسبه dt
    clock = pygame.time.Clock()
    
    # 4. شروع شبیه‌سازی (برای تنظیم زمان اولیه)
    sim.start()
    
    print("\nStarting Main Loop...")
    running = True
    while running:
        # مدیریت رویدادهای پنجره (مثل بستن)
        running = renderer.handle_events()
        
        # محاسبه زمان سپری شده از فریم قبل (dt) به ثانیه
        # این کار باعث می‌شود سرعت شبیه‌سازی مستقل از نرخ فریم رندر باشد
        dt = clock.tick(FPS) / 1000.0
        
        # آپدیت منطق شبیه‌سازی
        sim.update(dt)
        
        # گرفتن وضعیت فعلی دنیا از شبیه‌سازی
        world_state = sim.get_world_state()
        
        # رسم وضعیت دنیا روی صفحه
        renderer.draw(world_state)

    print("...Main Loop Exited.")
    renderer.cleanup()
    print("\n" + "="*41 + "\n=         Application Closed          =\n" + "="*41)

if __name__ == "__main__":
    main_game_loop()
