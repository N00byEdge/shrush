import sys

def dprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def read():
    c = sys.stdin.read(1)
    #dprint(f"Read byte '{c[0]}'")
    return c

def clean_read():
    while True:
        v = read()
        #dprint(f"clean_read: '{v[0]}'")
        if v == '\n': continue
        if v == ' ':  continue
        return v

def readword_finish(s):
    while True:
        c = read()
        #dprint(f"readword: '{s}', '{c[0]}'")
        if c == '\n': break
        if c == ' ':  break
        if c == '':   break
        s += c
    return s

def readword():
    return readword_finish(clean_read())

def readint():
    s = read()
    #dprint(f'readint: {s}')
    if s == 'x':
        return int(readword(), 16)
    if s == '\'':
        return ord(read()[0])
    return int(readword_finish(s), 10)

reg = [
    "rax", #0
    "rcx", #1
    "rdx", #2
    "rbx", #3
    "rsp", #4
    "rbp", #5
    "rsi", #6
    "rdi", #7
]

def translate():
    while True:
        op = readword()
        #dprint(f"opcode: '{op}'")
        if op == '!':
            print(f"""
                syscall
            """)
        elif op == 'A':
            dest = readint()
            lbl = readword()
            print(f"""
                lea {reg[dest]}, [{lbl}]
            """)
        elif op == 'B':
            print(f"""
                db {readint()}
            """)
        elif op == 'b':
            dest = readint()
            src = readint()
            print(f"""
                movzx {reg[dest]}, byte[{reg[src]}]
            """)
        elif op == 'C':
            lbl = readword()
            print(f"""
                call {lbl}
            """)
        elif op == 'D':
            lbl = readword()
            print(f"""
                {lbl}:
            """)
        elif op == 'E':
            lbl = readword()
            print(f"""
                je {lbl}
            """)
        elif op == 'e':
            print(f"""
                _start:
            """)
        elif op == 'I':
            value = readint()
            print(f"""
                dq {value}
            """)
        elif op == 'J':
            lbl = readword()
            print(f"""
                jmp {lbl}
            """)
        elif op == 'L':
            dest = readint()
            src = readint()
            print(f"""
                mov {reg[dest]}, [{reg[src]}]
            """)
        elif op == 'l':
            r = readint()
            num = readint()
            print(f"""
                shl {reg[r]}, {num}
            """)
        elif op == 'M':
            a = readint()
            b = readint()
            print(f"""
                cmp {reg[a]}, {b}
            """)
        elif op == 'm':
            a = readint()
            b = readint()
            print(f"""
                cmp {reg[a]}, {reg[b]}
            """)
        elif op == 'N':
            lbl = readword()
            print(f"""
                jne {lbl}
            """)
        elif op == 'P':
            print(f"""
                times 0x1000 db 0x00
            """)
        elif op == 'Q':
            lbl = readword()
            print(f"""
                dq {lbl}
            """)
        elif op == 'R':
            print(f"""
                ret
            """)
        elif op == 'S':
            src = readint()
            dest = readint()
            print(f"""
                mov [{reg[dest]}], {reg[src]}
            """)
        elif op == 'W':
            dest = readint()
            src = readint()
            value = readint()
            print(f"""
                lea {reg[dest]}, [{reg[src]} + {reg[value]}]
            """)
        elif op == 'w':
            dest = readint()
            src = readint()
            print(f"""
                sub {reg[dest]}, {reg[src]}
            """)
        elif op == '<':
            print(f"""
                pop {reg[readint()]}
            """)
        elif op == '=':
            dest = readint()
            value = readint()
            print(f"""
                mov {reg[dest]}, {value}
            """)
        elif op == '>':
            print(f"""
                push {reg[readint()]}
            """)
        elif op == '-':
            dest = readint()
            src = readint()
            value = readint()
            print(f"""
                lea {reg[dest]}, [{reg[src]} - {value}]
            """)
        elif op == '+':
            dest = readint()
            src = readint()
            value = readint()
            print(f"""
                lea {reg[dest]}, [{reg[src]} + {value}]
            """)
        elif op == '':
            return
        else:
            dprint(f"ERR: Unknwon op: '{op}'!")
            sys.exit(1)

if __name__ == '__main__':
    print(f"""
        [bits 64]
        [section .memes]
        extern _start
    """)
    translate()
