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
    
    def reset(self):
        self.tape = [0]
        self.pointer = 0
    
    def run(self, code):
        deftree = []
        lines = code.split('\n')
        li = 0
        while li < len(lines):
            line = lines[li]
            ci = 0
            while ci < len(line):
                char = line[ci]
                if char == '#': # Comment
                    break
                elif char == '>': # Increment pointer
                    # If out of bounds, extend tape
                    if len(deftree) == 0:
                        if self.pointer + 1 >= len(self.tape):
                            self.tape.append(0)
                        self.pointer += 1
                elif char == '<': # Decrement pointer
                    # If out of bounds, go to end of tape
                    if len(deftree) == 0:
                        if self.pointer - 1 < 0:
                            self.pointer = len(self.tape) - 1
                        else:
                            self.pointer -= 1
                elif char == '+': # Increment value
                    if len(deftree) == 0:
                        self.tape[self.pointer] += 1
                elif char == '-': # Decrement value
                    if len(deftree) == 0:
                        self.tape[self.pointer] -= 1
                elif char == '.': # Output value as ASCII character
                    # If not valid ASCII, raise error
                    if len(deftree) == 0:
                        if self.tape[self.pointer] < 0 or self.tape[self.pointer] > 255:
                            return False, NotASCIIError((li, ci), line, self.tape[self.pointer])
                        print(chr(self.tape[self.pointer]), end='')
                elif char == ':': # print literal number value
                    if len(deftree) == 0:
                        print(self.tape[self.pointer], end='')
                elif char == ',': # Input value
                    if len(deftree) == 0:
                        uinput = input()
                        if len(uinput) == 0:
                            self.tape[self.pointer] = 0
                        else:
                            for uici in range(len(uinput)):
                                self.tape[self.pointer + uici] = ord(uinput[uici])
                elif char == '[': # While tape[pointer] != 0, loop
                    if len(deftree) == 0:
                        if self.tape[self.pointer] == 0:
                            nests = 0
                            # run through code until ] is found, while accounting for loop nesting
                            while nests != 0 or line[ci] != ']':
                                if line[ci] == '[':
                                    nests += 1
                                elif line[ci] == ']':
                                    nests -= 1
                                ci += 1
                                if ci >= len(line): li += 1
                        else:
                            deftree.append(["loop", li, ci])
                elif char == ']': # End loop
                    if len(deftree) == 0 or deftree[-1][0] != "loop":
                        return False, UnmatchedBracketError((li, ci), line, self.tape[self.pointer])
                    else:
                        if deftree[-1][0] == "loop":
                            if self.tape[self.pointer] != 0:
                                li = deftree[-1][1]
                                ci = deftree[-1][2]
                            else:
                                deftree.pop()
                elif char == '~': # Break out of loop if tape[pointer] > 255
                    if len(deftree) == 0 or deftree[-1][0] != "loop":
                        return False, BreakOutOfLoopError((li, ci), line, self.tape[self.pointer])
                    else:
                        if deftree[-1][0] == "loop":
                            if self.tape[self.pointer] > 255:
                                nests = 0
                                # run through code until ] is found, while accounting for loop nesting
                                while nests != 0 or line[ci] != ']':
                                    if line[ci] == '[':
                                        nests += 1
                                    elif line[ci] == ']':
                                        nests -= 1
                                    ci += 1
                                    if ci >= len(line): li += 1
                        else:
                            return False, BreakOutOfLoopError((li, ci), line, self.tape[self.pointer])
                elif char == '$': # Start definition (syntax: $name{code})
                    deftree.append(["def", '', '', 'name'])
                elif char == '(': # Start function call (syntax: (name))
                    deftree.append(["call", ''])
                elif char == ')': # End function call and run
                    if len(deftree) == 0 or deftree[-1][0] != "call":
                        return False, UnmatchedBracketError((li, ci), line, self.tape[self.pointer])
                    if not re.match("[a-zA-Z0-9_]+", deftree[-1][1]):
                        return False, InvalidFunctionNameError((li, ci), line, deftree[-1][1])
                    if not deftree[-1][1] in self.functions:
                        return False, FunctionNotDefinedError((li, ci), line, deftree[-1][1])
                    self.run(self.functions[deftree[-1][1]])
                else:
                    if len(deftree) != 0:
                        if deftree[-1][0] == 'def':
                            if deftree[-1][3] == 'name':
                                if char == '{':
                                    if not re.match('[a-zA-Z0-9_]+', line[ci+1:].strip()):
                                        return False, InvalidFunctionNameError((li, ci), line, line[ci+1:].strip())
                                    deftree[-1][3] = 'code'
                                else:
                                    deftree[-1][1] += char
                            elif deftree[-1][3] == 'code':
                                if char == '}':
                                    self.functions[deftree[-1][1]] = deftree[-1][2]
                                    deftree.pop()
                                else:
                                    deftree[-1][2] += char
                        elif deftree[-1][0] == 'call':
                            if char == ')':
                                if deftree[-1][1] in self.functions:
                                    self.run(self.functions[deftree[-1][1]])
                                else:
                                    return False, FunctionNotDefinedError((li, ci), line, deftree[-1][1])
                                deftree.pop()
                            else:
                                deftree[-1][1] += char
                ci += 1
            li += 1
        return True, None