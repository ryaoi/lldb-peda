
from functools import wraps

OUTPUT_REGISTERS = [
    'rax',
    'rbx',
    'rcx',
    'rdx',
    'rsi',
    'rsi',
    'rdi',
    'rbp',
    'rsp',
    'rip'
]

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# https://gist.github.com/stek29/cdbbbe018f0aaf0b2a9a58c9173becb8
RFLAGS = [
	['CF', 'Carry Flag', 'carry'],
	[None, 'Reserved', None],
	['PF', 'Parity Flag', 'parity'],
	[None, 'Reserved', None],
	['AF', 'Adjust Flag', 'adjust'],
	[None, 'Reserved', None],
	['ZF', 'Zero Flag', 'zero'],
	['SF', 'Sign Flag', 'sign'],
	['TF', 'Trap Flag', 'trap'],
	['IF', 'Interrupt Enable Flag', 'interrupt'],
	['DF', 'Direction Flag', 'direction'],
	['OF', 'Overflow Flag', 'overflow'],
	['IOPL_H', 'I/O privilege level High bit', 'IOPL_H'],
	['IOPL_L', 'I/O privilege level Low bit', 'IOPL_L'],
	['NT', 'Nested Task Flag', 'nested'],
	[None, 'Reserved', None],

	# eflags
	['RF', 'Resume Flag', 'resume'],
	['VM', 'Virtual 8086 mode flag', 'VM'],
	['AC', 'Alignment check', 'alignement'],
	['VIF', 'Virtual interrupt flag', 'virtual interrpt'],
	['VIP', 'Virtual interrupt pending', 'VIP'],
	['ID', 'Able to use CPUID instruction', 'ID'],
	# 22-31 reserved

	# rflags 32-63 reserved
]

def ParseRflags(val):
    """ Returns list of set flags """
    rflags = list()

    for bit, desc in enumerate(RFLAGS):
        shortname, name, output = desc
        if val & (1 << bit) and name != 'Reserved':
            rflags.append(output)

    return rflags

def FormatOutput(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"{bcolors.OKBLUE}[{func.__name__.center(60, '-')}]{bcolors.ENDC}")
        results = func(*args, **kwargs)
        print(f"{bcolors.OKBLUE}[{'-'*60}]{bcolors.ENDC}")
        return results
    return wrapper

@FormatOutput
def Registers(debugger, command, result, internal_dict):
    target = debugger.GetSelectedTarget()
    process = target.GetProcess()
    mainThread = process.GetThreadAtIndex(0)
    currentFrame = mainThread.GetSelectedFrame()
    registerList = currentFrame.GetRegisters()
    generalPurposeRegister = registerList[0]
    for registers in registerList:
        for register in registers:
            regName = register.GetName()
            if regName in OUTPUT_REGISTERS:
                    print(f"{bcolors.OKGREEN}{regName}{bcolors.ENDC}: {register.GetValue()}")
            elif regName == 'rflags':
                regValue = int(register.GetValue(), 0)
                rflags = ParseRflags(regValue)
                colorizeFlagsOutput = [f"{bcolors.OKGREEN}{flag}" if index % 2 else f"{bcolors.FAIL}{flag.upper()}" for index, flag in enumerate(rflags)]
                print(f"{bcolors.OKGREEN}rflags {bcolors.ENDC}: {register.GetValue()}({' | '.join(colorizeFlagsOutput)}{bcolors.ENDC})")

@FormatOutput
def Code(debugger, command, result, internal_dict):
    cur_pc = debugger.GetSelectedTarget().GetProcess().GetSelectedThread().GetSelectedFrame().GetPC()
    debugger.HandleCommand('disassemble --start-address=' + str(cur_pc) + ' -c 4')

@FormatOutput
def Stack(debugger, command, result, internal_dict):
    cur_sp = debugger.GetSelectedTarget().GetProcess().GetSelectedThread().GetSelectedFrame().GetSP()
    debugger.HandleCommand('x/12gx ' + str(cur_sp))

def Peda(debugger, command, result, internal_dict):
    Registers(debugger, command, result, internal_dict)
    Code(debugger, command, result, internal_dict)
    Stack(debugger, command, result, internal_dict)

def __lldb_init_module(debugger, internal_dict):
    debugger.HandleCommand('command script add -f reverse.Registers reg')
    debugger.HandleCommand('command script add -f reverse.Code code')
    debugger.HandleCommand('command script add -f reverse.Stack stack')
    debugger.HandleCommand('command script add -f reverse.Peda peda')

