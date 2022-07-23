import numpy as np
kwargs = {
    'name': 'Bob',
    'age': 42,
    'job': 'dev',
    'pay': '100000',
        
}

kwargs = {
    'useid': np.array([1, 2, 3, 4]),
    'itemid': np.array([1, 2, 3, 4]),
}

# def FunctionName(name=None, age=None):
#     print(name, age)

# # def _FunctionName(**kwargs):
# #     print(kwargs['name'], kwargs['age'])

# FunctionName(**kwargs)
# pop age and name from kwargs
# kwargs.pop('name')
# kwargs.pop('age')
# print(kwargs)


A = [[974076680],
 [965431652],
 [978146863]]

B = np.array([a[0] for a in A])
print(type(B))



    
    