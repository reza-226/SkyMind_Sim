# skymind_sim/config.py

# تنظیمات اصلی شبیه ساز SkyMind
SIM_CONFIG = {
    'window': {
        'width': 1280,
        'height': 720,
        'caption': 'SkyMind Drone Simulator'
    },
    'simulation': {
        'fps': 60
    },
    'drone': {
        # موقعیت شروع پهپاد را به مرکز پنجره تغییر می دهیم
        'start_pos': (1280 // 2, 720 // 2) 
    },
    # بخش جدید برای تنظیمات محیط
    'environment': {
        # رنگ پس زمینه (آبی تیره) به صورت (R, G, B)
        'background_color': (13, 27, 42) 
    }
}
