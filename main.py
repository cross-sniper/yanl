import sys
import re

print_regex = r"echo (.*)"
function_regex = r"__(.*)\((.*)\)::(.*)->"
function_call_regex = r"call (.*)"
var_def_regex = r"var (.*):(.*) -> (.*)"

regex_patterns = [
    print_regex,
    function_regex,
    function_call_regex,
    var_def_regex,
]


class UnknownError(Exception):
    def __init__(self, text):
        super().__init__(text)


def process_line(line):
    line = line.rstrip()  # Remove trailing whitespace
    indentation_level = 0

    # Count leading tabs
    while line.startswith("\t"):
        indentation_level += 1
        line = line[1:]

    for regex_pattern in regex_patterns:
        if re.match(regex_pattern, line):
            if re.match(print_regex, line):
                # Process the print line
                match = re.match(print_regex, line)
                return " " * (indentation_level * 4) + f"print({match.group(1)})"
            elif re.match(function_regex, line):
                # Process the function definition line
                match = re.match(function_regex, line)
                function_name = match.group(1)
                args = match.group(2)
                return_type = match.group(3)
                return (
                    " " * (indentation_level * 4)
                    + f'def {function_name}({args})->"{return_type}":'
                )
            elif re.match(function_call_regex, line):
                match = re.match(function_call_regex, line)
                function_name = match.group(1)
                return " " * (indentation_level * 4) + f"{function_name}()"
            elif re.match(var_def_regex, line):
                match = re.match(var_def_regex, line)
                variable_name = match.group(1)
                variable_type = match.group(2)
                variable_value = match.group(3)
                return (
                    " " * (indentation_level * 4)
                    + f"{variable_name}:{variable_type} = {variable_value}"
                )

    # If the line doesn't match any regex, return it with appropriate indentation
    return " " * (indentation_level * 4) + line


def read_and_compile(file):
    with open(file) as f:
        code = f.read()

    lines = code.split("\n")
    compiled_code = []

    for line in lines:
        try:
            processed_line = process_line(line)  # Process the line based on its type
            compiled_code.append(processed_line)
        except Exception as e:
            raise UnknownError(f"An error occurred in {file}: {str(e)}")

    # Now, you can write the compiled code to a new file with the same name but ".py" extension
    output_file = file.replace(".neo", ".py")
    with open(output_file, "w") as f:
        for line in compiled_code:
            f.write(line + "\n")


files = sys.argv[1:]

for file in files:
    try:
        read_and_compile(file)
    except UnknownError as e:
        raise
    except Exception as e:
        print(f"An error occurred: {e}")
