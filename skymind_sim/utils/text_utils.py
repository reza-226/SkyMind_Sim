#
# فایل: skymind_sim/utils/text_utils.py
#
import arabic_reshaper
from bidi.algorithm import get_display

def prepare_persian_text(text: str) -> str:
    """
    این تابع یک متن فارسی را برای نمایش صحیح در کتابخانه‌هایی مانند Pygame آماده می‌کند.
    1. حروف را به شکل صحیح (اول، وسط، آخر) تبدیل می‌کند.
    2. ترتیب نمایش را از چپ به راست به راست به چپ اصلاح می‌کند.

    Args:
        text (str): متن ورودی فارسی.

    Returns:
        str: متن آماده شده برای نمایش.
    """
    if not text:
        return ""
        
    # مرحله 1: شکل‌دهی به حروف
    reshaped_text = arabic_reshaper.reshape(text)
    
    # مرحله 2: اصلاح ترتیب نمایش (راست به چپ)
    bidi_text = get_display(reshaped_text)
    
    return bidi_text
