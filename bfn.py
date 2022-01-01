# Brainfunc - Brainfuck with functions (and a bunch of neat features)

import re
function = type(lambda: None) # native function type

class NotASCIIError:
    def __init__(self, pos, line_string, data):
        self.name = 'NotASCIIError'

        self.line = pos[0]
        self.char = pos[1]
        self.human_line = self.line + 1
        self.human_char = self.char + 1
        self.line_string = line_string
        self.data = data
    
    def __str__(self):
        return "Number {c} does not represent an ASCII character".format(c=self.data)

class HaltError:
    def __init__(self, pos, line_string, data):
        self.name = 'HaltError'

        self.line = pos[0]
        self.char = pos[1]
        self.human_line = self.line + 1
        self.human_char = self.char + 1
        self.line_string = line_string
        self.data = data
    
    def __str__(self):
        return "Halted with code {c}".format(c=self.data)

class UnmatchedBracketError:
    def __init__(self, pos, line_string, data):
        self.name = 'UnmatchedBracketError'

        self.line = pos[0]
        self.char = pos[1]
        self.human_line = self.line + 1
        self.human_char = self.char + 1
        self.line_string = line_string
        self.data = data
    
    def __str__(self):
        return "Closing bracket '{cb}' not matched with opening bracket '{ob}'".format(cb=self.data, ob='[' if self.data == ']' else '(')

class BreakOutOfLoopError:
    def __init__(self, pos, line_string, data):
        self.name = 'BreakOutOfLoopError'

        self.line = pos[0]
        self.char = pos[1]
        self.human_line = self.line + 1
        self.human_char = self.char + 1
        self.line_string = line_string
        self.data = data
    
    def __str__(self):
        return "Used break outside of loop"

class InvalidFunctionNameError:
    def __init__(self, pos, line_string, data):
        self.name = 'InvalidFunctionNameError'

        self.line = pos[0]
        self.char = pos[1]
        self.human_line = self.line + 1
        self.human_char = self.char + 1
        self.line_string = line_string
        self.data = data
    
    def __str__(self):
        corrected_function_name = [c for c in self.data]
        for charindex in range(len(self.data)):
            if not re.match("[a-zA-Z0-9_]", self.data[charindex]):
                corrected_function_name[charindex] = "_"
        corrected_function_name = "".join(corrected_function_name)
        return "Invalid function name '{n}', consider using {cfn}".format(n=self.data, cfn=corrected_function_name)

class FunctionNotDefinedError:
    def __init__(self, pos, line_string, data):
        self.name = 'FunctionNotDefinedError'

        self.line = pos[0]
        self.char = pos[1]
        self.human_line = self.line + 1
        self.human_char = self.char + 1
        self.line_string = line_string
        self.data = data
    
    def __str__(self):
        return "Function '{n}' not defined".format(n=self.data)

class Brainfunc:
    def __init__(self, source = 'unknown', functions = {}):
        self.source = source
        self.functions = functions
        self.tape = [0]
        self.pointer = 0
        self.output = ''
    
    def reset(self):
        self.tape = [0]
        self.pointer = 0
    
    def run(self, code):
        deftree = []
        self.output = ''
        lines = code.split('\n')
        li = 0
        while li < len(lines):
            line = lines[li]
            ci = 0
            while ci < len(line):
                char = line[ci]
                if char == '#': # Comment
                    break
                elif char == '%': # Comment (multiline)
                    # go to matching %
                    ci += 1
                    while ci < len(line):
                        if line[ci] == '%':
                            break
                        ci += 1
                elif char == '>': # Increment pointer if pointer + 1 < tape length, else append 1 to tape
                    self.pointer += 1
                    if self.pointer >= len(self.tape):
                        self.tape.append(0)
                elif char == '<': # Decrement pointer if pointer > 0, else go to last element in tape
                    self.pointer -= 1
                    if self.pointer < 0:
                        self.pointer = len(self.tape) - 1
                elif char == '+': # Increment value at pointer
                    self.tape[self.pointer] += 1
                elif char == '-': # Decrement value at pointer
                    self.tape[self.pointer] -= 1
                elif char == '.': # Output value at pointer
                    self.output += chr(self.tape[self.pointer])
                elif char == ':': # Output literal number value
                    self.output += str(self.tape[self.pointer])
                elif char == ',': # Input value at pointer (multiple characters)
                    user_input = input()
                    for char_index in range(len(user_input)):
                        if self.pointer + char_index >= len(self.tape):
                            self.tape.append(0)
                        self.tape[self.pointer + char_index] = ord(user_input[char_index])
                elif char == '!': # Halt
                    return False, HaltError((li, ci), line, self.tape[self.pointer])
                else:
                    self.output += char # Debug
                ci += 1
            li += 1
        return True, None