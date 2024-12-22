import json
import argparse
import sys
import traceback

def main():
    parser = argparse.ArgumentParser(description='Command-line tool for the training configuration language')
    parser.add_argument('-i', '--input', required=True, help='Input JSON file path')
    parser.add_argument('-o', '--output', required=True, help='Output configuration file path')
    args = parser.parse_args()

    try:
        with open(args.input, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Syntax error in JSON input: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print(f"Input file not found: {args.input}")
        sys.exit(1)

    try:
        output = convert_data(data)
    except Exception as e:
        traceback.print_exc()
        print(f"Error converting data: {e}")
        sys.exit(1)

    try:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
    except Exception as e:
        print(f"Error writing output file: {e}")
        sys.exit(1)

consts = {}

def convert_data(data, indent=4):
    output = ''
    indent_str = ' ' * indent

    if isinstance(data, dict):
        output = ''
        output += f"{{\n"
        indent_str = ' ' * indent
        for key, value in data.items():
            if key.startswith("comment") and isinstance(value, list):
                # Обработка комментариев
                if len(value) == 1:
                    # Однострочный комментарий
                    output += f"{indent_str}% {value[0]}\n"
                else:
                    # Многострочный комментарий
                    output += f"{indent_str}/#\n"
                    for line in value:
                        output += f"{indent_str}{line}\n"
                    output += f"{indent_str}#/\n"
            elif key.startswith("def "):
                # Объявление константы
                const_name = key[3:].strip()
                const_value = convert_data(value, indent)
                consts[const_name] = const_value
                output += f"{indent_str}def {const_name} := {const_value}\n"
            elif key.startswith('!(') and key.endswith(')'):
                const_name = key[2:-1]
                if const_name in consts:
                    output += f"{indent_str}{const_name} => {consts[const_name]}\n"
                else:
                    print(f"Undefined constant: {const_name}")
                    sys.exit(1)
            else:
                # Обычный элемент словаря
                item_str = f"{indent_str}{key} => {convert_data(value, indent + 4)}"
                output += f"{item_str}\n" # output += f"{item_str},\n"
        output += f"{' ' * (indent - 4)}}}\n"
        return output
    elif isinstance(data, list):
        # Handle arrays
        items = [convert_data(item, indent) for item in data]
        output += f"[ {', '.join(items)} ]"
    elif isinstance(data, str):
        # Handle strings
        output += f"'{data}'"
    elif isinstance(data, (int, float)):
        # Handle numbers
        output += str(data)
    else:
        output += str(data)
    return output

if __name__ == "__main__":
    main()