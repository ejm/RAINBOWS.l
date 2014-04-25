#RAINBOWS.l Interpreter by Douglas Reilly
from sys import stdin, stdout, argv
import time
code = open(argv[1],'r').read()
data_types = {
    '$':'string',
    '%':'integer',
    '@':'variable',
    '_':'input',
}
stack = deque([0,0,0])
flags = {'ifstat':0,'moveahead':1,'pointer':0,'setmode':0,'back':0,}
variables = {}
arguments = []
functions = {}
lines = code.split('\n')
error = lambda line: print('"%s" Contained Error'%line)
label = lambda var: var.replace('@','')
def data(arg):
    if type(arg)==list:
        arg = ' '.join(arg)
    if Type(arg)=='string':
        if flags['setmode']: return arg
        else: return str(arg[1:]).replace('>n','\n').replace('>t','\t').replace('>:',';')
    if Type(arg)=='integer':
        if flags['setmode']: return arg
        else: return int(arg[1:])
    if Type(arg)=='variable':
        return data(variables[arg[1:]])
    if Type(arg)=='input':
        return data('%s%s'%(arg[1],input(arg[3:arg.index(']')])))
    
def Type(data):
    try: return [data_types[prefix] for prefix in data_types if data.startswith(prefix)][0]
    except: pass
    
def evaluate(line):
    #print('\t'+line) # for debugging
    for subline in line.split(';'):
        flags['moveahead']=1
        tokens = subline.split(' ')
        
        if tokens[0] == 'set':
            flags['setmode']=1
            variables[label(tokens[1])]=data(tokens[2:])
            flags['setmode']=0
        if tokens[0] == 'add':
            if Type(tokens[3])!='variable':
                    error(line)
            else:
                variables[label(tokens[3])]='%'+'%d'%(data(tokens[1])+data(tokens[2]))
        if tokens[0] == 'sub':
            if Type(tokens[3])!='variable':
                    error(line)
            else:
                variables[label(tokens[3])]='%'+'%d'%(data(tokens[1])-data(tokens[2]))
        if tokens[0] == 'mult':
            if Type(tokens[3])!='variable':
                    error(line)
            else:
                variables[label(tokens[3])]='%'+'%d'%(data(tokens[1])*data(tokens[2]))
        if tokens[0] == 'div':
            if Type(tokens[3])!='variable':
                    error(line)
            else:
                variables[label(tokens[3])]='%'+'%d'%(data(tokens[1])/data(tokens[2]))
        if tokens[0] == 'disp':
             stdout.write(str(data(' '.join(tokens[1:])))+'\n')
        if tokens[0] == 'if':
            if tokens[2] == '=':
                if data(tokens[1])==data(tokens[3]): flags['ifstat']=1
                else: flags['ifstat']=0
            elif tokens[2]=='!=':
                if data(tokens[1])!=data(tokens[3]): flags['ifstat']=1
                else: flags['ifstat']=0
            else: error(line)
        if tokens[0] == 'then':
            if flags['ifstat']==1: evaluate(' '.join(tokens[1:]))
        if tokens[0] == 'else':
            if flags['ifstat']==0: evaluate(' '.join(tokens[1:]))
        if tokens[0] == 'jump':
            flags['pointer'] = data(tokens[1])-1
        if tokens[0]=='go': flags['pointer'],flags['back']=parsedcode.index('.%s'%tokens[1]),flags['pointer']
        if tokens[0]=='end': flags['pointer']=flags['back']
        if tokens[0]=='delay': time.sleep(data(tokens[1]))
        if tokens[0]=='inc': variables[Id(token[1])]+=1
        if tokens[0]=='dec': variables[Id(token[1])]-=1
        if tokens[0]=='func':
            functions[tokens[1]]={'number_of_arguments':data(tokens[2]),'expression':' '.join(tokens[3:]).replace('->',';')}
        if tokens[0]=='call':
            expr = functions[tokens[1]]['expression']
            for i in range(functions[tokens[1]]['number_of_arguments']):
                expr = expr.replace('|%d'%i,str(data(' '.join(tokens[2:]).split(',')[i])))
            evaluate(expr)
        if tokens[0]=='read':
            try: variables[label(tokens[2])]='$%s'%open(data(tokens[1]),'r').read()
            except: pass
        if tokens[0]=='write':
            try: open(data(tokens[1]),'w').write(data(' '.join(tokens[2:]))).close()
            except: pass
        if tokens[0]=='stack':
            if tokens[1]=='push': stack.append(' '.join(tokens[2:]))
        
 
        
        
            
            
parsedcode = [line[:line.index('`')-1] if '`' in line else line for line in code.split('\n')]
while flags['pointer']<len(parsedcode):
    evaluate(parsedcode[flags['pointer']])
    flags['pointer']+=flags['moveahead']
