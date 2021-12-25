import bfn
import sys

interpreter = bfn.Brainfunc(functions={
    'pushR': '[->+<]', # push right
    'pushL': '[-<+>]', # push left
    '255': '[-]+[+~]', # set to 255
})

if len(sys.argv) == 1:
    # shell
    while True:
        try:
            line = input(str(interpreter.tape) + "> ")
            success, err = interpreter.run(line)
            if not success:
                print(f"""Brainfunc {err.name} @ {err.human_line}:{err.human_char}:
    {err.line}
    {str(err)}""")
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
    with open(sys.argv[1], 'r') as f:
        for line in f:
            success, err = interpreter.run(line)
            if not success:
                print(f"""Brainfunc {err.name} @ {err.human_line}:{err.human_char}:
    {err.line}
    {str(err)}""")