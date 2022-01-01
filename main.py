import bfn
import sys

def reset_pointer(self):
    self.pointer = 0

interpreter = bfn.Brainfunc(functions={
    'pushR': '[->+<]', # push right
    'pushL': '[-<+>]', # push left
    '255': '[-]+[+~]', # set to 255
    'newline': '>[-]++++++++++.[-]<', # newline (ascii 10)
    'resetPointer': reset_pointer, # reset pointer
})

if len(sys.argv) == 1:
    # shell
    while True:
        try:
            line = input(str(interpreter.tape) + "[" + str(interpreter.pointer) + "]" + "> ")
            success, err = interpreter.run(line)
            if not success:
                print(f"""Brainfunc {err.name} @ {err.human_line}:{err.human_char}:
    {err.line_string}
    {str(err)}""")
                if type(err) == bfn.HaltError:
                    break
            else:
                print(interpreter.output)
        except EOFError:
            break
else:
    # file
    # read input if necessary
    if len(sys.argv) == 3:
        uinput = sys.argv[2]
        if len(uinput) == 0:
            interpreter.tape[interpreter.pointer] = 0
        else:
            for uici in range(len(uinput)):
                interpreter.tape[uici] = ord(uinput[uici])
    try:
        with open(sys.argv[1], 'r') as f:
            for line in f:
                success, err = interpreter.run(line)
                if not success:
                    print(f"""Brainfunc {err.name} @ {err.human_line}:{err.human_char}:
        {err.line_string}
        {str(err)}""")
                else:
                    print(interpreter.output, end='')
    except FileNotFoundError:
        print("File not found")
    except EOFError:
        print("EOF")
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise