# This is a basic example of how to use argparse to create a command line
# python script

import argparse

def parse_arguments():
    """Parse/check input arguments."""
    parser = argparse.ArgumentParser(prog='PROG')
    parser.add_argument('-a', '--num1', type=int, required=True,
                        help="First number")
    parser.add_argument('-b', '--num2', type=int, required=True,
                        help="Second number")
    arguments = parser.parse_args()
    return arguments

if __name__ == "__main__":
    args = parse_arguments()
    print(args.num1 + args.num2)