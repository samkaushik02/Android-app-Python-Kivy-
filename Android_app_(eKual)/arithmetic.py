#MadeBy_SameerKaushik
#sam4python@gmail.com
import random

class Arithmetic(object):
    #Used for Addition, Subtraction, Multiplication and Division Questions
    def __init__(self, min_num=0, max_num=10):
        self.max_num = max_num
        self.min_num = min_num
        self.operation = None
        self.num_one = None
        self.num_two = None
        self.QUESTION = "What is {} {} {}?"

    def prep_rand_num(self):
        #gives num_one and num_two random value from the range
        self.num_one = random.randint(self.min_num, self.max_num)
        self.num_two = random.randint(self.min_num, self.max_num)

    def get_addition_question(self):
        # Addition ques
        self.prep_rand_num()
        self.operation = "+"

        return self.QUESTION.format(self.num_one, self.operation, self.num_two)

    def get_subtraction_question(self):
        # Subtraction ques
        self.prep_rand_num()
        self.operation = "-"

        while self.num_one < self.num_two:
            self.prep_rand_num()

        return self.QUESTION.format(self.num_one, self.operation, self.num_two)

    def get_multiplication_question(self):
        # Multiplication ques
        self.prep_rand_num()
        self.operation = "x"

        return self.QUESTION.format(self.num_one, self.operation, self.num_two)

    def get_division_question(self):
        # Division ques
        self.prep_rand_num()
        self.operation = "%"

        while self.num_two == 0 or self.num_one % self.num_two != 0:
            self.prep_rand_num()

        return self.QUESTION.format(self.num_one, self.operation, self.num_two)

    def get_next_question(self, rand=False):
        # Next maths question
        if rand:
            _list = "+ - x %".split()
            self.operation = _list[random.randint(0, len(_list) - 1)]
        _dict = {
            "+": self.get_addition_question,
            "-": self.get_subtraction_question,
            "x": self.get_multiplication_question,
            "%": self.get_division_question
                }
        return _dict[self.operation]()

    def get_answer(self):
        # Get the answer
        if self.operation == "+":
            return self.num_one + self.num_two
        elif self.operation == "-":
            return self.num_one - self.num_two
        elif self.operation == "x":
            return self.num_one * self.num_two
        else:
            return self.num_one / self.num_two

#Made_By_Sameer_Kaushik
        
