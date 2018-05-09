def getBig(a,b):
    if a >= b:
        return  a
    else:
        return b

if __name__ == '__main__' :
    print('自己调用')
else:
    print('三方引用')
b = 1
__version__ = '0.0.0.1'

def reverse(text):
    return text[::-1]

class ToolClass:
    def saytool(self):
        print("I am Tool.")