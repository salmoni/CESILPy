# CESILPy
A CESIL interpreter written in Python. CESIL is the Computer Education in Schools Instruction Language, created by ICL

It works only on the command line. Just type:

python CESILPy.py test01.ces

And the output should appear.

### WARNING ###

There is little in the way of error checking so poor syntax will fly through.

Keywords must be in capital letters. I think this was standard for CESIL but until I can get my hands on an official manual, I'll have to rely on memory.

Identifiers (variable names) can, unlike real CESIL, contain or begin with any character other than double quotes. Probably unicode too. "'!##'" (without quotes) is a valid identifier name.

Strings are wrapped by a pair of double quotes.
