import argparse

def main():
    # Create the parser
    parser = argparse.ArgumentParser(description='A simple file processor.')

    # Add positional argument
    parser.add_argument('input', help='Input file path')

    # Add optional argument with a default value
    parser.add_argument('-o', '--output', help='Output file path', default='output.txt')

    # Parse the command-line arguments
    args = parser.parse_args()

    # Accessing parsed values
    print(f'Input file: {args.input}')
    print(f'Output file: {args.output}')

if __name__ == "__main__":
    main()
