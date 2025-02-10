from datetime import*

# Task 1

print(f"1. {(datetime.now()).date() - timedelta(days=5)}")

# Task 2

print(f"\n2. Yesterday: {(datetime.now()).date() - timedelta(days=1)}\nToday: {(datetime.now()).date()}\nTomorrow: {(datetime.now()).date() + timedelta(days=1)}")

# Task 3

print(f"\n3. {(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')}")

#Task 4

date1 = datetime(2025, 2, 9) # 9 февраль 2025
date2 = datetime(2001, 9, 11)  # 11 сентября 2001

raznica = date1 - date2
print(f"\n4. Difference: {raznica}")
print(f"All days: {raznica.days}")