def reverse(debugger, command, result, internal_dict):
    target = debugger.GetSelectedTarget()
    print("FT_" + str(target)[::-1])

def tohex(val, nbits):
      return hex((val + (1 << nbits)) % (1 << nbits))

def find_value(process, first_value):
    arrow = []
    if "0x00007f" in first_value:
        arrow.append(first_value)
        value = process.GetSelectedThread().GetFrameAtIndex(0).EvaluateExpression('*(long*)' + first_value).unsigned
        arrow.append(str(hex(value)))
        i = 1
        while "0x7fff" in arrow[i]:
            value = process.GetSelectedThread().GetFrameAtIndex(0).EvaluateExpression('*(long*)' + arrow[i]).unsigned
            arrow.append(str(hex(value)))
            i += 1
        if len(arrow) > 1:
            arrow[len(arrow) - 1] = str(hex(process.GetSelectedThread().GetFrameAtIndex(0).EvaluateExpression('*(int*)' + arrow[len(arrow) - 1]).unsigned))

    elif "0x7fff" in first_value:
        arrow.append(first_value)
        value = process.GetSelectedThread().GetFrameAtIndex(0).EvaluateExpression('*(long*)' + first_value).unsigned
        arrow.append(str(hex(value)))
        i = 1
        while "0x7fff" in arrow[i]:
            value = process.GetSelectedThread().GetFrameAtIndex(0).EvaluateExpression('*(long*)' + arrow[i]).unsigned
            arrow.append(str(hex(value)))
            i += 1
        if len(arrow) > 1:
            arrow[len(arrow) - 1] = str(hex(process.GetSelectedThread().GetFrameAtIndex(0).EvaluateExpression('*(long*)' + arrow[len(arrow) - 1]).unsigned))

    return arrow

def reg(debugger, command, result, internal_dict):
    print('\033[94m[------------------registers---------------]\033[0m')
    target = debugger.GetSelectedTarget()
    process = target.GetProcess()
    mainThread = process.GetThreadAtIndex(0)
    currentFrame = mainThread.GetSelectedFrame()
    registerList = currentFrame.GetRegisters()
    for value in registerList:
        for child in value:
            if child.GetName() in ['rax', 'rbx', 'rcx', 'rdx', 'rsi', 'rsi', 'rdi', 'rbp', 'rsp', 'rip', 'rflags']:
                if child.GetName() == 'rflags':
                    flags = []
                    if int(child.GetValue(), 0) & 0x0001:
                        flags.append("carry")
                    if int(child.GetValue(), 0) & 0x0004:
                        flags.append("parity")
                    if int(child.GetValue(), 0) & 0x0010:
                        flags.append("adjust")
                    if int(child.GetValue(), 0) & 0x0040:
                        flags.append("zero")
                    if int(child.GetValue(), 0) & 0x0080:
                        flags.append("sign")
                    if int(child.GetValue(), 0) & 0x0100:
                        flags.append("trap")
                    if int(child.GetValue(), 0) & 0x0200:
                        flags.append("interrupt")
                    if int(child.GetValue(), 0) & 0x0400:
                        flags.append("direction")
                    if int(child.GetValue(), 0) & 0x0800:
                        flags.append("overflow")

                    flags_peda = ['\033[92m' + x if i % 2 else '\033[91m' + x.upper() for i, x in enumerate(flags)]
                    print('\033[92mrflags \033[0m: ' +child.GetValue().replace("000000000000", "") + ' (' + " | ".join(flags_peda) + '\033[0m)')
                else:
                    arrow = find_value(process, child.GetValue())
                    if any(arrow):
                        print('\033[92m' + child.GetName() + "\033[0m: " + " --> ".join(arrow))
                    else:
                        print('\033[92m' + child.GetName() + "\033[0m: " + child.GetValue())

    print('\033[94m[------------------------------------------]\033[0m')

def code(debugger, command, result, internal_dict):
    print('\033[94m[--------------------Code------------------]\033[0m')
    cur_pc = debugger.GetSelectedTarget().GetProcess().GetSelectedThread().GetSelectedFrame().GetPC();
    debugger.HandleCommand('disassemble --start-address=' + str(cur_pc) + ' -c 4')
    print('\033[94m[------------------------------------------]\033[0m')

def stack(debugger, command, result, internal_dict):
    print('\033[94m[-------------------Stack------------------]\033[0m')
    target = debugger.GetSelectedTarget()
    process = target.GetProcess()
    cur_sp = process.GetSelectedThread().GetSelectedFrame().GetSP();
    debugger.HandleCommand('x/12gx ' + str(cur_sp))
    print('\033[94m[------------------------------------------]\033[0m')

def peda(debugger, command, result, internal_dict):
    reg(debugger, command, result, internal_dict)
    code(debugger, command, result, internal_dict)
    stack(debugger, command, result, internal_dict)

def __lldb_init_module(debugger, internal_dict):
    debugger.HandleCommand('command script add -f reverse.reverse reverse')
    debugger.HandleCommand('command script add -f reverse.reg reg')
    debugger.HandleCommand('command script add -f reverse.code code')
    debugger.HandleCommand('command script add -f reverse.stack stack')
    debugger.HandleCommand('command script add -f reverse.peda peda')

