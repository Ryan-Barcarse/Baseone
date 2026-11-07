from datetime import datetime

def display_banner():
    print("-"*45)
    print("             BaseOne Application")
    print("          Security Monitoring System")
    print("-"*45)


def system_status():
    current_time = datetime.now()

    print("\n[System Status] Active")
    print(f"[!] Current system time: {current_time}")
    print("[!] Monitoring status: Not active")
    print("[!] Notification service: Not configured")

def main():
    display_banner()
    system_status()

if __name__ == "__main__":
    main()