import argparse
from datetime import datetime

from file_monitor import baseline, detect_changes


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


def display_results(results):
    '''
    Displays the results of file change detection.
    '''

    total = sum(len(files) for files in results.values())
    print('\n[!] File integrity scan completed')

    if total == 0:
        print('[GOOD] No file changes detected')

    for name in results['added']:
        print(f'[ADDED] {name}')
    for name in results['modified']:
        print(f'[MODIFIED] {name}')
    for name in results['deleted']:
        print(f'[DELETED] {name}')

    print(f'[INFO] Total changes detected: {total}')


def main():
    #argparse is a built in python library for processing command-line args
    parser = argparse.ArgumentParser(
        description='BaseOne Security Monitoring System'
    )
    parser.add_argument(
        'command',
        # Limits values to 'baseline' or 'scan'
        choices=['baseline', 'scan'],
        help='Create a baseline or scan for changes'
    )

    parser.add_argument(
        'directory',
        help='Directory to monitor'
    )

    args = parser.parse_args()


    display_banner()
    system_status()

    if args.command == 'baseline':
        baseline(args.directory)
    elif args.command == 'scan':
        results = detect_changes(args.directory)
        display_results(results)

if __name__ == "__main__":
    main()