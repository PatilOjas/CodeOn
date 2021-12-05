import random

class QuestionProvider:
    def __init__(self) -> None:
        self.qList = [
            {
            "question":"Given a list of integers, find out all the even numbers exist in the list using Stream functions?\n",
            "time":"900",
            "input":"[10,15,8,49,25,98,32]",
            "expectedOP":"10, 8, 98, 32"
            },
            {
            "question":"Given a list of integers, find out all the numbers starting with 1 using Stream functions?\n",
            "time":"900",
            "input":"[10,15,8,49,25,98,32]",
            "expectedOP":"10, 15"
            },
            {
            "question":"How to find duplicate elements in a given integers list in java using Stream functions?\n",
            "time":"900",
            "input":"[10,15,8,49,25,98,32]",
            "expectedOP":"98, 15"
            },
            {
            "question":"Given the list of integers, find the first element of the list using Stream functions?\n",
            "time":"900",
            "input":"[10,15,8,49,25,98,32]",
            "expectedOP":"10"
            },
            {
            "question":"Given a list of integers, find the total number of elements present in the list using Stream functions?\n",
            "time":"900",
            "input":"[10,15,8,49,25,98,32]",
            "expectedOP":"9"
            },
            {
            "question":"Given a list of integers, find the maximum value element present in it using Stream functions?\n",
            "time":"900",
            "input":"[10,15,8,49,25,98,32]",
            "expectedOP":"98"
            },
            {
            "question":"Given a String, find the first non-repeated character in it using Stream functions?\n",
            "time":"900",
            "input":"Java Hungry Blog Alive is Awesome",
            "expectedOP":"j"
            },
            {
            "question":"Given a String, find the first repeated character in it using Stream functions?\n",
            "time":"900",
            "input":"Java Hungry Blog Alive is Awesome",
            "expectedOP":"a"
            },
            {
            "question":"Given a list of integers, sort all the values present in it using Stream functions?\n",
            "time":"900",
            "input":"[10,15,8,49,25,98,32]",
            "expectedOP":" 8\n10\n15\n15\n25\n32\n49\n98\n98"
            },
        ]   

    def randomPicker(self,):
        pickedIndex = random.randint(0, len(self.qList)-1)
        return self.qList[pickedIndex], pickedIndex