import yaml
import sys
import os

def add_log(solution_name, solution_version, architecture, pass_flag):

    # Path to the log file
    log_file = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..','solution_log.yml'))

    # Load the solution log file
    with open(log_file, 'r', encoding='utf8') as f:
        config_data = yaml.safe_load(f)

    # Check if the file is empty, if so override assigning a dictionary
    if config_data is None:
        config_data = {}
    
    # Correct the flag, from the CI will came as true or false, they need to be True and False
    if pass_flag == 'true':
        final_pass_flag = True
    elif pass_flag == 'false':
        final_pass_flag = False
    else:
        raise ValueError("The indicated flag needs to be true or false.")

    # Check if the solution name is already stored
    if solution_name in config_data.keys(): 
        if solution_version in config_data[solution_name]:
            # If so, add or replace the architecture and its status
            config_data[solution_name][solution_version][architecture] = final_pass_flag
        else:
            # Otherwise, initialize it
            config_data[solution_name][solution_version] = {architecture: final_pass_flag}
    else:
        # Otherwise, initialize it
        config_data[solution_name] = {solution_version: {architecture: final_pass_flag}}

    # Write the solution log file
    with open(log_file, 'w', encoding='utf8') as new_f:
        yaml.safe_dump(config_data, new_f, width=10e10, default_flow_style=False, allow_unicode=True)

if __name__ == "__main__":
    if len(sys.argv) == 5:
        sys.exit(add_log(solution_name=sys.argv[1], solution_version=sys.argv[2], architecture=sys.argv[3], pass_flag=sys.argv[4]))
    else:
        sys.exit(1)