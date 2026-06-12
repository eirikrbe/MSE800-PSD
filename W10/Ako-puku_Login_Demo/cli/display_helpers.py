
# display_helpers.py

import os
import platform

def clear_screen():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def pause():
    input("\nPress Enter to continue...")

def display_title(title):
    print("\n========================================")
    print(f"  {title}")
    print("========================================")


def display_success(message):
    print(f"\n[SUCCESS] {message}")


def display_error(message):
    print(f"\n[ERROR] {message}")


def display_info(message):
    print(f"\n[INFO] {message}")
