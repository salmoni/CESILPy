# CESILPy
A CESIL interpreter written in Python. CESIL is the Computer Education in Schools Instruction Language, created by ICL

It works only on the command line. Just type:

python CESILPy.py test01.ces

And the output should appear.

## FORMAT ##

I've tried to keep CESILPy as accurate as possible. I think this was standard for CESIL but until I can get my hands on an official manual, I'll have to rely on memory. All mistakes are, of course, entirely my own. I'd be happy to get a copy of the original manual or recollections by others.

Programs are formatted into 3 columns.

Comments begin with "%" as the first character in the line. Anything else on the line is ignored. Multi-line comments are not possible.

Empty lines are not parsed but ignored.

If the line is not a comment and is not empty, parsing begins. Labels appear in the first column. Labels can currently be anything without a space other than operators (commands). All spaces are stripped. Labels can be upper or lower case, can start with any or contain any character. I'm fairly sure that labels had to be alphanumeric only but I need this to be confirmed. Labels can be a maximum of 8 characters long. Anything longer spills into the operators (see below). Labels cannot be duplicated and the program will terminate if it finds any.

The second column (characters 9-16) are the operators (or commands). These are reserved words that cannot be labels or identifiers. All must be in upper case only.

The third column (characters 17 onwards) are operands (what operators operate on). These might be identifers (variable names or labels), or literals (strings or integer numbers). Strings require double quotes and these are naturally stripped out when being printed.
