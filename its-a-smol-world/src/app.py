import time
import itertools
import threading
import sys
import argparse
from smol_mind import SmolMind, load_functions

# Thanks to @torymur for the bunny ascii art!
bunny_ascii = r"""
(\(\ 
 ( -.-)
 o_(")(")
"""

def spinner(stop_event):
    spinner = itertools.cycle(['-', '/', '|', '\\'])
    while not stop_event.is_set():
        sys.stdout.write(next(spinner))
        sys.stdout.flush()
        sys.stdout.write('\b')
        time.sleep(0.1)

def main():
    # Add command-line argument parsing
    parser = argparse.ArgumentParser(description="SmolMind CLI")
    parser.add_argument("-s", "--size", choices=["1.7B", "135M"], default="1.7B")
    args = parser.parse_args()

    print("loading SmolMind...")
    functions = load_functions("./src/functions.json")
    sm = SmolMind(functions, args.size)
    print(bunny_ascii)
    print(f"Welcome to the Bunny B1 (powered by SmolLM2-{args.size})! What do you need?")
    while True:
        user_input = input("> ")
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        
        # Create a shared event to stop the spinner
        stop_event = threading.Event()
        
        # Start the spinner in a separate thread
        spinner_thread = threading.Thread(target=spinner, args=(stop_event,))
        spinner_thread.daemon = True
        spinner_thread.start()

        response = sm.get_function_call(user_input)

        # Stop the spinner
        stop_event.set()
        spinner_thread.join()
        sys.stdout.write(' \b')  # Erase the spinner
        
        print(response)

if __name__ == "__main__":
    main()
