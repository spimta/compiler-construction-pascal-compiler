import sys
from Scanner import Scanner
from Parser import Parser
from StackMachine import StackMachine

if len(sys.argv) == 1:
    filename = input("please input your file directory: ")

else:
    filename = sys.argv[1]
    if not open(filename):
        print("please input correct filename")
        sys.exit(1)

scanner = Scanner()
token_list = scanner.scan_file(filename)

# print(token_list)

parsed = Parser(token_list, 0).run()

# print(parsed)

stack_machine = StackMachine(parsed["symbol_table"], parsed["opcode_list"])
stack_machine.run()