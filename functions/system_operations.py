import os
import platform


def stop_chat():
    system_type = platform.system()
    if system_type == 'Windows':
        os.system('shutdown /s /t 0')
    elif system_type == 'Linux':
        os.system('sudo shutdown -h now')
    else:
        print("Unsupported operating system")
