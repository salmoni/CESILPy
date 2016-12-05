

# CESILPy - A CESIL interpreter for Python
# Yes, it's fairly basic

import sys, os
import pdb

class CESILObj(object):
    def __init__(self, fname):
        try:
            fin = open(fname,'r')
        except IOError:
            print("Cannot open "+fname)
            sys.exit()
        try:
            script = fin.read()
        except:
            print("Cannot read the file "+fname)
            sys.exit()
        try:
            fin.close()
        except IOError:
            print("Cannot close the file %s but will continue nevertheless"%fname)
        print("Opening and running ",fname)
        self.fname = fname
        self.script = script.split(os.linesep)
        self.commands = ["LOAD","STORE","JUMP","JINEG","JIZERO","PRINT","OUT",
                "IN","LINE","HALT","ADD","SUBTRACT","MULTIPLY","DIVIDE"]
        self.acc = 0 # accumulator
        self.labels = {}
        self.variables = {}
        self.ParseLabels()
        self.ParseVariables()
        self.RunScript()
        #print self.labels
        #print self.variables

    def ParseLabels(self):
        """
        This runs through and extracts all label names and stores them with the line number
        Duplicates are not allowed.
        """
        print("Parsing label names")
        for idx, line in enumerate(self.script):
            words = line.split()
            if len(words) > 0:
                initword = words[0]
                if initword not in self.commands:
                    if initword not in self.labels.keys():
                        self.labels[initword] = idx
                    else:
                        print("DUPLICATE LABEL ON LINE "+str(idx))
                        print ("PROGRAM FINISHING")
                        sys.exit()
        print (self.labels)

    def ParseVariables(self):
        """
        This runs through and extracts all variable names and initialised them
        All variables are initialised to zero (0)
        """
        print("Parsing variable names")
        vars = {}
        for idx, line in enumerate(self.script):
            words = line.split()
            try:
                poss_var = words[-1]
                if poss_var not in self.commands:
                    if poss_var[0] != '"':
                        if poss_var not in self.labels:
                            try:
                                val = int(poss_var)
                            except ValueError: # should not be integer
                                self.variables[poss_var] = 0
            except IndexError:
                pass
        print (self.variables)

    def halt_good(self):
        print("END OF PROGRAM - SUCCESSFUL COMPLETION")
        sys.exit()

    def RunScript(self):
        print("Running script. Hold on...")
        self.linenum = 0
        while True:
            line = self.script[self.linenum]
            #print ("LN = ",str(self.linenum+1))
            old_line = self.linenum
            res = self.parse_line(line)
            if old_line == self.linenum:
                self.linenum = self.linenum + 1
                if self.linenum > len(self.script):
                    self.halt_good()

    def parse_line(self, line):
        strings = line.split('"')
        words = strings[0].split()
        try:
            words.append(strings[1])
        except IndexError:
            pass
        if len(words) < 1:
            return
        elif len(words) == 1: # command only
            if words[0] == "HALT":
                cmd = "HALT"
            elif words[0] == "IN":
                # get input
                cmd = "IN"
            elif words[0] == "LINE":
                cmd = "LINE"
            elif words[0] == "OUT":
                cmd = "OUT"
        elif len(words) == 3: # label, command, literal/id
            label = words[0]
            cmd = words[1]
            operand = words[2]
            if operand[0] == '"':
                # is a string
                optype = "string"
            elif operand in self.labels:
                optype = "label"
            elif operand in self.variables:
                print("IS VARIABLE")
                value = self.variables[operand]
                optype = "variable"
                print(operand, type(operand), value, type(value))
            else:
                try:
                    value = int(operand)
                    optype = "integer"
                    print(operand, type(operand), value, type(value))
                except ValueError:
                    print ("FAILED TO WORK OUT OPERAND TYPE LINE "+str(self.linenum))
                    sys.exit()
        elif len(words) == 2: #label + command, or command + operand
            if words[0] in self.labels: # is a label + command
                label = words[0]
                cmd = words[1]
            elif words[0] in self.commands: # is command + operand
                #pdb.set_trace()
                cmd = words[0]
                operand = words[1]
            if operand[0] == '"':
                # is a string
                optype = "string"
            elif operand in self.labels:
                optype = "label"
            elif operand in self.variables:
                print("IS VARIABLE")
                value = self.variables[operand]
                optype = "variable"
                print(operand, type(operand), value, type(value))
            else:
                try:
                    value = int(operand)
                    optype = "integer"
                    print(operand, type(operand), value, type(value))
                except ValueError:
                    print ("FAILED TO WORK OUT OPERAND TYPE LINE "+str(self.linenum))
                    sys.exit()
        try:
            # Now begin commands
            print ("TRACE: %s %s "%(str(self.linenum+1), str(self.acc)))
            if cmd == "HALT":
                self.halt_good()
            elif cmd == "IN":
                print("? ",end="")
                while True:
                    val = input()
                    try:
                        self.acc = int(val)
                        break
                    except ValueError:
                        print("? ",end="")
            elif cmd == "LINE":
                print("\n")
            elif cmd == "OUT":
                print(str(self.acc), end="")
            elif cmd == "PRINT":
                print(operand,end="")
            elif cmd == "ADD":
                if optype == "integer" or optype == "variable":
                    self.acc = self._add(value)
                else:
                    print ("CANNOT ADD ANYTHING TO "+value)
                    sys.exit()
            elif cmd == "SUBTRACT":
                if optype == "integer" or optype == "variable":
                    self.acc = self._subtract(value)
                else:
                    print ("CANNOT SUBTRACT ANYTHING FROM "+value)
                    sys.exit()
            elif cmd == "MULTIPLY":
                if optype == "integer" or optype == "variable":
                    self.acc = self._multiply(value)
                else:
                    print ("CANNOT MULTIPLY ANYTHING FROM "+value)
                    sys.exit()
            elif cmd == "DIVIDE":
                if optype == "integer" or optype == "variable":
                    self.acc = self._multiply(value)
                else:
                    print ("CANNOT DIVIDE ANYTHING FROM "+value)
                    sys.exit()
            elif cmd == "JUMP":
                self.linenum = self.labels[operand]
            elif cmd == "JIZERO":
                if self.acc == 0:
                    self.linenum = self.labels[operand]
            elif cmd == "JINEG":
                if self.acc < 0:
                    self.linenum = self.labels[operand]
            elif cmd == "LOAD":
                self.acc = operand
            elif cmd == "STORE":
                self.variables[operand] = value #int(self.acc)
        except:
            print(self.acc, self.variables, operand)
            sys.exit()

    def _add(self, val):
        self.acc = self.acc + val

    def _subtract(self, val):
        self.acc = self.acc - val

    def _multiply(self, val):
        self.acc = self.acc * val

    def _divide(self, val):
        if val == 0:
            print ("DIVIDE BY ZERO ERROR LINE "+str(self.linenum))
            print ("PROGRAM FINISHING")
            sys.exit()
        else:
            self.acc = int(self.acc / val)

    def _print(self, val):
        print (val)

    def _line(self):
        print ("/n")

    def _in(self):
        # return input as self.input which is then put into variable
        pass

def CESILParse(fname):
    try:
        fin = open(fname,'r')
    except IOError:
        print("Cannot open "+fname)
        sys.exit()
    try:
        script = fin.read()
    except:
        print("Cannot read the file "+fname)
        sys.exit()
    try:
        fin.close()
    except IOError:
        print("Cannot close the file %s but will continue nevertheless"%fname)
    print("Parsing ",fname)
    lines = script.split(os.linesep)
    for idx, line in enumerate(lines):
        words = parse(line)
        print (idx, words)


if __name__ == "__main__":
    # Get filename, load, run
    try:
        fname = sys.argv[1]
    except:
        print("No filename specified")
        sys.exit()
    CESIL = CESILObj(fname)
    #CESILParse(fname)
