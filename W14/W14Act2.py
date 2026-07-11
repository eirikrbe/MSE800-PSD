
# Registering decorated objects to an API

'''
    This is a example of a decorator that registers decorated functions and classes to a registry dictionary.  
'''

registry = {} 
'''this is a dictionary that registers decorated functions and classes'''
def register(obj):
    '''this is the decorator function that stores the decorated function or classes in the registry{}
        this decorator does not modify the decorated function or class, it just registers it in the registry dictionary
    '''                          
    registry[obj.__name__] = obj            
    return obj                              

@register
def spam(x):
    '''
    this is a register decorated function that returns the square of the input x
    '''
    return(x ** 2)                          # spam = register(spam)

@register
def ham(x):
    '''
    this is a register decorated function that returns the cube of the input x
    '''
    return(x ** 3)

@register
class Eggs:                                 # Eggs = register(Eggs)
    '''
    this is a register decorated class that returns the fourth power of the input x
    '''
    def __init__(self, x):
        self.data = x ** 4
    def __str__(self):
        return str(self.data)

print('Registry:')
'''
this for loop prints the decorated functions and classes that are registered in the registry {} dictionary
and prints the name of the decorated function or class, the object
'''
for name in registry:
    print(name, '=>', registry[name], type(registry[name]))

print('\nManual calls:')
'''
these manual prints show that the decorated functions and class are not modified by the decorator. 
'''
print(spam(2))                              # Invoke objects manually
print(ham(2))                               # Later calls not intercepted
X = Eggs(2)
print(X)

print('\nRegistry calls:')
'''
this show the real usability of the decorator, it can invoke things dynamically by string name without knowing them ahead of time
'''
for name in registry:
    print(name, '=>', registry[name](2))    # Invoke from registry