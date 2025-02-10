from datetime import*

# Task 1

print(f"1. {(datetime.now()).date() - timedelta(days=5)}")

# Task 2

print(f"\n2. Yesterday: {(datetime.now()).date() - timedelta(days=1)}\nToday: {(datetime.now()).date()}\nTomorrow: {(datetime.now()).date() + timedelta(days=1)}")

# Task 3

print(f"\n3. First: {(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')}")
