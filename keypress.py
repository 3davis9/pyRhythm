import time

# Define the number of keys and the initial empty arrays to hold their beats
NUM_KEYS = 4
key_beats = [[] for _ in range(NUM_KEYS)]

# Define the function to handle a key press
def handle_key_press(key_idx):
    # Get the current time in seconds
    now = time.time()
    # Add the current time to the key's array of beats
    key_beats[key_idx].append(now)
    # Print a confirmation message
    print(f"Added beat to key {key_idx+1} at {now:.3f} seconds")

# Example usage: press keys 1, 2, 1, 3, 4 in sequence
handle_key_press(0)
handle_key_press(1)
handle_key_press(0)
handle_key_press(2)
handle_key_press(3)

# Print the resulting arrays of beats for each key
for key_idx, beats in enumerate(key_beats):
    print(f"Key {key_idx+1}: {beats}")
