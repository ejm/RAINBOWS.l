#RAINBOWS.l Interpreter by Douglas Reilly
from sys import stdin, stdout, argv
import time
code = open(argv[1],'r').read()
data_types = {
    '$':'string',
    '%':'integer',
    '@':'variable',
}
flags = {'ifstat':0,'moveahead':1,'pointer':0,'setmode':0,'back':0,}
variables = {}
lines = code.split('\n')
error = lambda line: print('"%s" Contained Error'%line)
label = lambda var: var.replace('@','')
def data(arg):
    if Type(arg)=='string':
        if flags['setmode']: return arg
        else: return str(arg[1:])
    if Type(arg)=='integer':
        if flags['setmode']: return arg
        else: return int(arg[1:])
    if Type(arg)=='variable':
        return data(variables[label(arg)])
def Type(data):
    try: return data_types[data[0]]
    except: print('Unkown data type %s'%data[0])
    
def evaluate(line):
    #print('\t'+line) # for debugging
    for subline in line.split(';'):
        flags['moveahead']=1
        tokens = subline.split(' ')
        try:
            command = tokens[0]
            if command.startswith('-'): command,arg1 = 'goto',command[1:]
        except: pass
        try: command,arg1 = tokens[0],tokens[1]
        except: pass
        try: comand,arg1,arg2 = tokens[0],tokens[1],tokens[2]
        except: pass
        try: comand,arg1,arg2,arg3 = tokens[0],tokens[1],tokens[2],tokens[3]
        except: pass
        if command == 'set':
            if Type(arg1)!='variable':
                error(line)
            else:
                flags['setmode']=1
                variables[label(arg1)]=data(arg2)
                flags['setmode']=0
        if command == 'add':
            if Type(arg3)!='variable':
                    error(line)
            else:
                variables[label(arg3)]='%'+'%d'%(data(arg1)+data(arg2))
        if command == 'sub':
            if Type(arg3)!='variable':
                    error(line)
            else:
                variables[label(arg3)]='%'+'%d'%(data(arg1)-data(arg2))
        if command == 'mult':
            if Type(arg3)!='variable':
                    error(line)
            else:
                variables[label(arg3)]='%'+'%d'%(data(arg1)*data(arg2))
        if command == 'div':
            if Type(arg3)!='variable':
                    error(line)
            else:
                variables[label(arg3)]='%'+'%d'%(data(arg1)/data(arg2))
        if command == 'disp':
             stdout.write(str(data(arg1)).replace('\\\\','\n').replace('\\',' '))
        if command == 'input':
            if Type(arg1)!='variable': error(line)
            else: variables[label(arg1)]=input('')
        if command == 'if':
            if arg2 == '=':
                if data(arg1)==data(arg3): flags['ifstat']=1
                else: flags['ifstat']=0
            elif arg2=='!=':
                if data(arg1)!=data(arg3): flags['ifstat']=1
                else: flags['ifstat']=0
            else: error(line)
        if command == 'then':
            if flags['ifstat']==1: evaluate(' '.join(tokens[1:]))
        if command == 'else':
            if flags['ifstat']==0: evaluate(' '.join(tokens[1:]))
        if command == 'jump':
            flags['pointer'] = data(arg1)-1
        if command=='goto': flags['pointer'],flags['back']=parsedcode.index('lbl %s'%arg1),flags['pointer']
        if command=='end': flags['pointer']=flags['back']
        if command=='delay': time.sleep(data(arg1))
        
parsedcode = [line[:line.index('`')-1] if '`' in line else line for line in code.split('\n')]
while flags['pointer']<len(parsedcode):
    evaluate(parsedcode[flags['pointer']])
    flags['pointer']+=flags['moveahead']
