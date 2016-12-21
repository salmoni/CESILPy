

# CESILPy - A CESIL interpreter for Python
# Yes, it's fairly basic
# (c) 2016, Alan James Salmoni

import sys, os

class CESILObj(object):
    def __init__(self, fname):
        try:
            fin = open(fname,'r')
        except IOError:
            print("### ERROR ### CANNOT OPEN "+fname)
            sys.exit()
        try:
            script = fin.read()
        except:
            print("### ERROR ### CANNOT READ "+fname)
            sys.exit()
        try:
            fin.close()
        except IOError:
            print("Cannot close the file %s but will continue nevertheless"%fname)
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

    def ParseLabels(self):
        """
        This runs through and extracts all label names and stores them with the
        line number.
        Duplicates are not allowed and cause termination.
        """
        for idx, line in enumerate(self.script):
            words = line.split()
            if len(words) > 0:
                initword = words[0]
                if initword not in self.commands:
                    if initword not in self.labels.keys():
                        self.labels[initword] = idx
                    else:
                        print("### ERROR ### DUPLICATE LABEL ON LINE "+str(idx))
                        sys.exit()

    def ParseVariables(self):
        """
        This runs through and extracts all variable names and initialised them
        All variables are initialised to zero (0)
        """
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

    def halt_good(self):
        print ('\n%')
        sys.exit()

    def RunScript(self):
        print("%")
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
        # Split the line into words
        # First by partitioning quotes out (strings)...
        strings = line.split('"')
        # ...then but "chunk"
        words = strings[0].split()
        try:
            words.append(strings[1])
        except IndexError:
            pass
        # Calculate the number of words
        num_words = len(words)
        # Run through commands in turn
        if num_words > 0:
            if "HALT" in words:
                self.halt_good()
            elif "IN" in words:
                print ("? ",end="")
                while True:
                    val = input()
                    try:
                        self.acc = int(val)
                        break
                    except ValueError:
                        print("REDO? ",end="")
            elif "OUT" in words:
                print (str(self.acc), end="")
            elif "LINE" in words:
                print ("\n")
            elif "LOAD" in words[:-1]:
                operand = words[-1]
                try:
                    self.acc = int(operand)
                except ValueError:
                    self.acc = self.variables[operand]
            elif "STORE" in words[:-1]:
                var_name = words[-1]
                self.variables[var_name] = self.acc
            elif "PRINT" in words[:-1]:
                print (words[-1], end="")
            elif ("ADD" in words[:-1]) or ("SUBTRACT" in words[:-1]) or ("MULTIPLY" in words[:-1]) or ("DIVIDE" in words[:-1]):
                operand = words[-1]
                try:
                    value = int(operand)
                except ValueError:
                    value = self.variables[operand]
                if "ADD" in words[:-1]:
                    self.acc = self.acc + value
                elif "SUBTRACT" in words[:-1]:
                    self.acc = self.acc - value
                elif "MULTIPLY" in words[:-1]:
                    self.acc = self.acc * value
                elif "DIVIDE" in words[:-1]:
                    if value == 0:
                        print ("### ERROR ### DIVIDE BY ZERO LINE "+str(self.linenum))
                        sys.exit()
                    else:
                        self.acc = int(self.acc / value)
            elif "JUMP" in words[:-1]:
                self.linenum = self.labels[words[-1]]
            elif "JIZERO" in words[:-1]:
                if self.acc == 0:
                    self.linenum = self.labels[words[-1]]
            elif "JINEG" in words[:-1]:
                if self.acc < 0:
                    self.linenum = self.labels[words[-1]]

if __name__ == "__main__":
    try:
        fname = sys.argv[1]
    except:
        print("### ERROR ### NO FILENAME SPECIFIED")
        sys.exit()
    CESIL = CESILObj(fname)
