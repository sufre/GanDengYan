import cmd

class A(cmd.Cmd):
	def do_hello(self, line):
		print line

a = A()

a.cmdloop()