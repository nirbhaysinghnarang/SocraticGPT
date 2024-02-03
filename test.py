from question import Question
from main import *
q = Question(""" 
What is theory behind continuous time markov chains
""")

q.get_answer()
obj = to_json(q)

print(obj)