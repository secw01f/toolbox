import argparse
import os

# Update the the values in the key value pairs with the appropriate information for the module
def details():
    details = {'name': str(os.path.basename(__file__)).split('.')[0], 'category': 'misc', 'description': 'This is a template for toolbox modules', 'path': os.path.abspath(__file__), 'key': False}
    return(details)

def module(args):
    argparser = argparse.ArgumentParser(add_help=False)
    # Add your arguments below
    # argparser.add_argument("-t", "--temparg", required=True)
    # argparser.add_argument("-e", "--example", required=False)
    cmd = argparser.parse_args(args)

    # Add your module code here

    return()

if __name__ == '__main__':
    # Allows you to use the script independently if desired
    argparser = argparse.ArgumentParser(add_help=False)
    # Add your arguments below
    # argparser.add_argument("-t", "--temparg", required=True)
    # argparser.add_argument("-e", "--example", required=False)
    args = argparser.parse_args()

    # Add your module code here