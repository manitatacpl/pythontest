import time

# Get current time in seconds since epoch
current_time = time.time()
print(f"Current time in seconds since epoch: {current_time}")

# Get formatted local time
local_time = time.localtime()
formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
print(f"Formatted local time: {formatted_time}")

# Demonstrate sleep function
print("Waiting for 3 seconds...")
time.sleep(3)
print("Done waiting!")

# Get processor time
cpu_time = time.process_time()
print(f"CPU time: {cpu_time} seconds")
