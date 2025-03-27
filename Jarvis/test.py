import winreg
import subprocess
import os

def get_installed_apps():
    """Retrieve a list of installed applications from the Windows Registry."""
    apps = {}
    registry_paths = [
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
        r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
    ]
    
    for path in registry_paths:
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path) as key:
                for i in range(winreg.QueryInfoKey(key)[0]):  # Iterate through subkeys
                    try:
                        subkey_name = winreg.EnumKey(key, i)
                        with winreg.OpenKey(key, subkey_name) as subkey:
                            app_name, _ = winreg.QueryValueEx(subkey, "DisplayName")
                            app_path, _ = winreg.QueryValueEx(subkey, "InstallLocation")
                            if app_name and app_path:
                                apps[app_name.lower()] = app_path
                    except (OSError, FileNotFoundError, ValueError):
                        continue
        except FileNotFoundError:
            print(f"Registry path not found: {path}")
            continue

    return apps

def open_app(app_name):
    """Automatically find and open the application."""
    app_name = app_name.lower()
    installed_apps = get_installed_apps()

    # Find the closest matching application
    for name, path in installed_apps.items():
        if app_name in name:
            executable = os.path.join(path, f"{name}.exe")
            if os.path.exists(executable):
                print(f"Opening {name} from {executable}...")
                subprocess.Popen(executable, shell=True)
                return True
            else:
                print(f"Executable not found in {path}")
                return False

    print(f"Application '{app_name}' not found.")
    return False

# Example Usage
open_app("whatsapp")  # This will automatically find and open WhatsApp