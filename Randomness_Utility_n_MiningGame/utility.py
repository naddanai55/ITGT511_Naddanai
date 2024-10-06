import random

class Marblebag_random:
    def __init__(self, bag):
        self.new_bag = bag
        self.pick = None
    
    def draw(self):
        random.shuffle(self.new_bag)
        self.pick = self.new_bag.pop(0)
        return self.pick, self.new_bag

class Progressive_random:
    def __init__(self, success_rate = 10, delta = 10):
        self.success_rate = success_rate
        self.draw_number = 0
        self.delta = delta

    def draw(self):
        possibility = random.uniform(0, 100)
        print("possibility = ", possibility)
        if possibility < (self.success_rate  + (self.draw_number * self.delta)):
            self.draw_number = 0
            return("success")
        else:
            self.draw_number += 1
            return("failed")

class Fixed_limit_random:
    def __init__(self, fixed = 3, success_rate = 10, delta = 10):
        self.success_rate = success_rate
        self.draw_number = 0
        self.delta = delta
        self.fixed_limit = fixed
    
    def draw(self):
        possibility = random.uniform(0, 100)
        print("possibility = ", possibility)
        if self.draw_number == self.fixed_limit:
            self.draw_number = 0
            return("success")
        else:
            if possibility < (self.success_rate  + (self.draw_number * self.delta)):
                self.draw_number = 0
                return("success")
            else:
                self.draw_number += 1
                return("failed")

class Predetermination_random:
    def __init__(self, determine = 3):
        self.draw_number = 0
        self.determine = determine

    def draw(self):
        if self.draw_number == self.determine:
            self.draw_number = 0
            return("success")
        else:
            self.draw_number += 1
            return("failed")
        
class Mining_random:
    def __init__(self):
        self.success_rate = 0
        self.draw_number = 0
        self.mineral_bag = ["silver", "gold", "diamond","silver", "gold","silver"]
        self.pick = None
        self.fixed_limit = None

    def to_break(self, success_rate = 50):
        self.success_rate = success_rate
        possibility = random.uniform(0, 100)
        if possibility < self.success_rate:
            return True
        else:
            return False
            
    def to_drop(self, success_rate = 30, fixed = 3):
        self.success_rate = success_rate
        self.fixed_limit = fixed
        possibility = random.uniform(0, 100)
        if self.draw_number == self.fixed_limit:
            self.draw_number = 0
            return True
        else:
            if possibility < self.success_rate:
                self.draw_number = 0
                return True
            else:
                self.draw_number += 1
                return False
       
    def shuffle_draw(self):
        random.shuffle(self.mineral_bag)
        self.pick = self.mineral_bag[0]
        return self.pick
    

        





    



