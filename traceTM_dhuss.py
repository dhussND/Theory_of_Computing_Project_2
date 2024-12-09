#!/usr/bin/env python3

from collections import deque
import sys

def parse_tm(file_name):
    # parse tm from file
    tm = {}
    with open(file_name, 'r') as file:
        lines = [line.strip() for line in file.readlines()]
        
        tm["name"] = lines[0]
        tm["states"] = lines[1].split(",")
        tm["input_alphabet"] = lines[2].split(",")
        tm["tape_alphabet"] = lines[3].split(",")
        tm["start_state"] = lines[4]
        tm["accept_state"] = lines[5]
        tm["reject_state"] = lines[6]
        
        tm["transitions"] = []
        for line in lines[7:]:
            current_state, read_symbol, next_state, write_symbol, direction = line.split(",")
            tm["transitions"].append({
                "current_state": current_state,
                "read_symbol": read_symbol,
                "next_state": next_state,
                "write_symbol": write_symbol,
                "direction": direction
            })
    return tm

def print_configuration(path):
    # print each config in path
    for config in path:
        tape_left, state, tape_right = config
        head_char = tape_right[0] if tape_right else "_"
        print(f"{tape_left}[{state}]{head_char}{tape_right[1:]}")

def execute_tm(tm, input_string, max_steps=100):
    # sim tm and track all paths
    initial_config = ("", tm["start_state"], input_string)  # (tape_left, state, tape_right)
    queue = deque([[initial_config]])  # lists of configurations
    visited = set()  
    all_paths = [] 
    transitions_count = 0 

    print(f"Machine: {tm['name']}")
    print(f"Initial string: {input_string}")

    # bfs
    while queue:
        current_level = queue.popleft()
        
        next_level = []
        
        for config in current_level:
            tape_left, state, tape_right = config
            
            transitions_count += 1
            
            if state == tm["accept_state"]:
                print(f"String accepted in {transitions_count} transitions.")
                print_configuration(current_level)
                return "accepted"
            
            if state == tm["reject_state"]:
                print(f"String rejected in {transitions_count} transitions.")
                print_configuration(current_level)
                return "rejected"
            
            current_char = tape_right[0] if tape_right else "_"
            
            # explore all transitions for the current config
            for transition in tm["transitions"]:
                if transition["current_state"] == state and transition["read_symbol"] == current_char:
                    new_tape_left = tape_left + transition["write_symbol"]
                    new_tape_right = tape_right[1:] if len(tape_right) > 1 else ""
                    new_state = transition["next_state"]
                    
                    new_config = (new_tape_left, new_state, new_tape_right)
                    
                    # if not visited, continue
                    if new_config not in visited:
                        visited.add(new_config)
                        next_level.append(new_config)
        
        if next_level:
            queue.append(next_level)
        else:
            print("No valid paths found. Halting.")
            print(f"Execution stopped after {transitions_count} transitions.")
            return "stopped"

        if transitions_count >= max_steps:
            print(f"Execution stopped after {transitions_count} transitions.")
            return "stopped"
    
    return "rejected"

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: ./traceTM.py <file.csv> <input_string>")
        sys.exit(1)
    
    file_name = sys.argv[1]
    input_string = sys.argv[2]
    tm = parse_tm(file_name)
    
    max_steps = 100  # adjust the max steps as desired
    result = execute_tm(tm, input_string, max_steps)
    print(f"String {input_string}: {result}")
