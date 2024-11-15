import os
import re
import yaml

def add_tag(code, new_tag):
    # Regular expression to match the tags list
    tags_regex = r"(tags=\[)(.*?)(\])"

    def replacer(match):
        # Extract the current tags
        before, tags, after = match.groups()
        # Add the new tag to the tags list
        updated_tags = f"{tags}, {new_tag}" if tags.strip() else new_tag
        # Return the updated string
        return f"{before}{updated_tags}{after}"
    
    # Apply the replacement
    return re.sub(tags_regex, replacer, code, flags=re.DOTALL)

def add_build_status(solution_path, flag_amd64, flag_arm64):

    # Load the solution.py file
    with open(solution_path, "r", encoding='utf8') as f:
        solution_code = f.read()

    if flag_amd64:
        amd64_tag = "\'AMD64 ✅\'"
    else:
        amd64_tag = "\'AMD64 ❌\'"

    if flag_arm64:
        arm64_tag = "\'ARM64 ✅\'"
    else:
        arm64_tag = "\'ARM64 ❌\'"

    updated_solution_code = add_tag(code=solution_code, new_tag=amd64_tag)
    updated_solution_code = add_tag(code=updated_solution_code, new_tag=arm64_tag)
    updated_solution_code = add_tag(code=updated_solution_code, new_tag="\'test\'")

    # Write the solution.py file
    with open(solution_path, "w", encoding='utf8') as solution_file:
        solution_file.write(updated_solution_code)

def main():
    import argparse
 
    parser = argparse.ArgumentParser(description="Add building status tag to a solution.py file",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-p", "--path", help="Path of the .py file")
    parser.add_argument("-d", "--amd64", help="Building status for AMD64")
    parser.add_argument("-r", "--arm64", help="Building status for ARM64")
    args = vars(parser.parse_args())
    
    # Get the absolute path of the file
    solution_path = os.path.abspath(args["path"])

    # In case it's used by the CI, to process the true/false arguments
    if args["amd64"] == 'true':
        flag_amd64 = True
    elif args["amd64"] == 'false':
        flag_amd64 = False
    else:
        flag_amd64 = args["amd64"]

    # In case it's used by the CI, to process the true/false arguments
    if args["arm64"] == 'true':
        flag_arm64 = True
    elif args["arm64"] == 'false':
        flag_arm64 = False
    else:
        flag_arm64 = args["arm64"]

    add_build_status(solution_path=solution_path, flag_amd64=flag_amd64, flag_arm64=flag_arm64)

if __name__ == "__main__":
    main()