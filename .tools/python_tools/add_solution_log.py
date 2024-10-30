import yaml
import sys
import os

def add_log(solution_name, architecture, pass_flag):

    log_file = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..','solution_log.yml'))

    # Load the solution log file
    with open(log_file, 'r', encoding='utf8') as f:
        config_data = yaml.safe_load(f)
        
    config_data[solution_name] = {architecture: bool(pass_flag)}

    # Write the solution log file
    with open(log_file, 'w', encoding='utf8') as new_f:
        yaml.safe_dump(config_data, new_f, width=10e10, default_flow_style=False, allow_unicode=True)

if __name__ == "__main__":
    if len(sys.argv) == 4:
        sys.exit(add_log(solution_name=sys.argv[1], architecture=sys.argv[2], pass_flag=sys.argv[3]))
    else:
        sys.exit(1)