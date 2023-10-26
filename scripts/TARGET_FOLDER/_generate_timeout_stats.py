# _timeout_log.txt
# vt2182_attackcase8.r2py timed out against reference_monitor_vt2182.r2py


# Split the data into lines
with open("_timeout_log.txt", "r") as f:
    data = f.read()

lines = data.strip().split('\n')

# 1. Total number of timeouts
total_timeouts = len(lines)
print(f"Total number of timeouts: {total_timeouts}")

print()

# 2. Attackers and their frequency
attackcases = {}
for line in lines:
    attackcase = line.split(" timed out against ")[0]
    if attackcase in attackcases:
        attackcases[attackcase] += 1
    else:
        attackcases[attackcase] = 1

print("\nAttackcases and their frequency:")
for attackcase, count in sorted(attackcases.items(), key=lambda item: item[1], reverse=True):
    print(f"  - `{attackcase}`: {count} timeouts")

print()

# 3. Reference monitors and their frequency
reference_monitors = {}
for line in lines:
    reference_monitor = line.split(" timed out against ")[1]
    if reference_monitor in reference_monitors:
        reference_monitors[reference_monitor] += 1
    else:
        reference_monitors[reference_monitor] = 1

print("\nReference monitors and their frequency:")
for reference_monitor, count in sorted(reference_monitors.items(), key=lambda item: item[1], reverse=True):
    print(f"  - `{reference_monitor}`: {count} timeouts")

print()

# 4. Attack cases timed out against reference_monitor_vt2182
vt2182_reference_monitor_timeouts = [
    line for line in lines if "reference_monitor_vt2182.r2py" in line]

print("Attack cases that timed out against reference_monitor_vt2182:")
for line in vt2182_reference_monitor_timeouts:
    attackcase = line.split(" timed out against ")[0]
    print(f"  - `{attackcase}`")

print()

# 5. Reference monitors timed out against vt2182_attackcases
vt2182_attackcase_timeouts = [
    line for line in lines if "vt2182_attackcase" in line]

print("\nReference monitors that timed out against vt2182_attackcases:")
for line in vt2182_attackcase_timeouts:
    reference_monitor = line.split(" timed out against ")[1]
    print(f"  - `{reference_monitor}`")
