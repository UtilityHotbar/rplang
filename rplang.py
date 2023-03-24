INTEGER = 'integer'
FLOAT = 'float'
STRING = 'string'
IDENTIFIER = 'identifier'
MACRO_PLAYBACK = 'macro_playback'

class Token:
    def __init__(self, kind, data) -> None:
        self.kind = kind
        self.data = data

def process(string):
    i = 0
    line = []
    exception = False
    stringing = False
    charing = False
    cbuf = []
    while (i < len(string)):
        print(string[i], line, cbuf)
        c = string[i]
        if (c == '\\'):
            exception = True
        elif (exception):
            cbuf.append(c)
            exception = False
        elif (c == '|'):
            if not stringing:
                cbuf.append(STRING)
                stringing = True
            else:
                stringing = False
        elif (stringing):
            cbuf.append(c)
        elif (c == '\''):
            cbuf.append(STRING)
            charing = True
        elif (charing):
            cbuf.append(c)
            charing = False
        elif (c == ','):
            line.append(package(cbuf))
            cbuf = []
        elif (c == 'i'):
            cbuf.append(INTEGER)
        elif (c == 'f'):
            cbuf.append(FLOAT)
        elif (c == '$'):
            cbuf.append(MACRO_PLAYBACK)
        elif (c == '!'):
            cbuf.append(evaluate(line))
        elif (c == '_'):
            cbuf = []
        elif (c == '%'):
            line = []
        else:
            cbuf.append(c)
        i += 1
    if (cbuf):
        line.append(package(cbuf))
    return line

def package(cbuf):
    if (cbuf[0] == INTEGER):
        return Token('integer', int(''.join([str(x) for x in cbuf[1:]])))
    elif (cbuf[0] == FLOAT):
        return Token('float', float(''.join([str(x) for x in cbuf[1:]])))
    elif (cbuf[0] == STRING):
        return Token('string', str(''.join([str(x) for x in cbuf[1:]])))
    elif (cbuf[0] == MACRO_PLAYBACK):
        return Token('macro_playback', str(''.join([str(x) for x in cbuf[1:]])))
    else:
        return Token('identifier', str(''.join([str(x) for x in cbuf])))

def evaluate(line):
    scope = {}
    stack = []
    macros = {}
    i = 0
    while (i < len(line)):
        curr_item = line[i]
        print(curr_item.kind, curr_item.data, scope, stack, macros, list(map(lambda x:x.data,line)))
        if curr_item.kind in ['integer', 'string', 'float']:
            stack.append(curr_item.data)
        elif curr_item.kind == 'macro_playback':
            line = line[:i] + process(macros[curr_item.data]) +line[i+1:]
            i -= 1
        elif curr_item.kind == 'identifier':
            func = curr_item.data
            if (func == 'm'):
                name = stack.pop()
                macro = stack.pop()
                if (type(macro) != str):
                    raise RuntimeError('macro must be string')
                print(name, macro)
                macros[str(name)] = macro
            elif (func == '+'):
                stack.append(stack.pop()+stack.pop())
            elif (func == '-'):
                stack.append(stack.pop()-stack.pop())
            elif (func == '*'):
                stack.append(stack.pop()*stack.pop())
            elif (func == '/'):
                stack.append(stack.pop()/stack.pop())
            elif (func == 'p'):
                print(stack.pop())
            elif (func == '~'):
                thing = stack.pop()
                name = stack.pop()
                if (type(name) != str):
                    raise RuntimeError('var name mut be string')
                scope[name] = thing
            elif (func == '?'):
                yes = stack.pop()
                no = stack.pop()
                eval = stack.pop()
                if (eval > 0):
                    line = line[:i] + process(macros[yes]) + line[i:]
                else:
                    line = line[:i] + process(macros[no]) + line[i:]
            elif (func == '>'):
                if (stack.pop() > stack.pop()):
                    stack.append(1)
                else:
                    stack.append(0)
            elif (func == '<'):
                if (stack.pop() < stack.pop()):
                    stack.append(1)
                else:
                    stack.append(0)
            elif (func == '='):
                if (stack.pop() == stack.pop()):
                    stack.append(1)
                else:
                    stack.append(0)
            elif (func == '^'):
                return stack.pop()
            else:
                if (func in scope):
                    stack.append(scope[func])
        i += 1
    return 1

if __name__ == '__main__':
    process(input())