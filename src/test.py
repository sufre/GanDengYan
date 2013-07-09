
class A:
	"""docstring for A"""
	def aa(self, msg):
		print msg

class B(A):
	def aa(self):
		A.aa(self, 'hello')
		print 'bb'

a = A()
#a.aa()
b = B()
#b.aa()	
a = b
a.aa()