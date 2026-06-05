import os

HOSTS_PATH = r"C:\Windows\System32\drivers\etc\hosts"
REDIRECT_IP = "127.0.0.1"
DISTRACTING_SITES = [
    "www.instagram.com", "instagram.com",
    "www.facebook.com", "facebook.com",
    "www.reddit.com", "reddit.com"
]

def enable_distraction_blocker():
    try:
        with open(HOSTS_PATH, "r") as file:
            content = file.read()
        with open(HOSTS_PATH, "a") as file:
            for site in DISTRACTING_SITES:
                if site not in content:
                    file.write(f"\n{REDIRECT_IP} {site}")
        print("[System]: Distraction Blocker Activated.")
    except PermissionError:
        print("[System Note]: Run Terminal as Admin to block distracting websites.")
    except Exception as e:
        print(f"[System Blocker Error]: {e}")

def disable_distraction_blocker():
    try:
        if not os.path.exists(HOSTS_PATH):
            return
        with open(HOSTS_PATH, "r") as file:
            lines = file.readlines()
        with open(HOSTS_PATH, "w") as file:
            for line in lines:
                if not any(site in line for site in DISTRACTING_SITES):
                    file.write(line)
        print("[System]: Distraction Blocker Deactivated. Websites Restored.")
    except PermissionError:
        print("[System Note]: Run Terminal as Admin to restore websites automatically.")
    except Exception as e:
        print(f"[System Blocker Error]: {e}")