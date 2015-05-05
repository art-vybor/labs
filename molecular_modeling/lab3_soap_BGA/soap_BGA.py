import random
from copy import copy, deepcopy

kind_of_body = {'C': -0.5, 'O': 1.3, 'N': 9.4}

kind_of_head = {'CO_2': 20.1, 'SO_4': 38.7, 'O': 1.9}

kind_of_tail = {'C': -0.5}

class Molecule:
    def __init__(self, tail, body, head):
        self.body = body
        self.head = head
        self.tail = tail

    def HLB(self):
        hlb = kind_of_tail[self.tail] + kind_of_head[self.head]
        hlb += sum([kind_of_body[body_elem] for body_elem in self.body])
        return hlb + 7

    def get_elements(self):
        return [self.tail] + self.body + [self.head]

    def apply_elements(self, elements):
        self.head = elements[len(elements) - 1]
        self.tail = elements[0]
        self.body = elements[1:len(elements) - 1]
        return self

    def mutation(self):
        elements = self.get_elements()
        i = random.randrange(len(elements) - 1) + 1 #remove tail with index 0
        if i == len(elements) - 1: # head
            elements[i] = random.choice(list(kind_of_head.iterkeys()))
        else: #body
            elements[i] = random.choice(list(kind_of_body.iterkeys()))

        self.apply_elements(elements)
        return self

    def check(self):
        #print self
        head_condition = self.head in kind_of_head
        tail_condition = self.tail in kind_of_tail
        body_condition = sum([elem in kind_of_body for elem in self.body]) == len(self.body) #and len(self.body) < 50
        elems_condition = True
        elems = self.get_elements()
        for i in range(len(elems)-1):
            if elems[i] == 'O' and elems[i+1] == 'O':
                elems_condition = False
            if elems[i] == 'N' and elems[i+1] == 'N':
                elems_condition = False    
            if elems[i] == 'N' and elems[i+1] == 'O':
                elems_condition = False

        #print head_condition and body_condition and tail_condition

        return head_condition and body_condition and tail_condition and elems_condition

    
    def __str__(self):
        return '-'.join(self.get_elements())


def htransfer(m1, m2):
    def split(elems):
        
        left_len = random.randrange(len(elems)-1)
        left, center_right = elems[:left_len], elems[left_len:]
        
        center_len = random.randrange(1, len(center_right))

        center, right = center_right[:center_len], center_right[center_len:]
        return left, center, right

    elems1, elems2 = m1.get_elements(), m2.get_elements()

    left1, center1, right1 = split(elems1)
    left2, center2, right2 = split(elems2)
        
    return m1.apply_elements(left1+center2+right1), m2.apply_elements(left2+center1+right2)

def division_stage(molecule_list):
    res = []
    for m in molecule_list:
        res.append(deepcopy(m))
    res.extend(molecule_list)
    return res

def mutation_stage(molecule_list, mutation_probability):
    mutation_indexes = set()

    while len(mutation_indexes) != int(len(molecule_list)*mutation_probability):
        mutation_indexes.add(random.randrange(len(molecule_list)))

    for i in mutation_indexes:
        molecule_list[i].mutation().mutation().mutation().mutation().mutation().mutation().mutation().mutation()

    for i in sorted(mutation_indexes, reverse=True):
        if not molecule_list[i].check():
            molecule_list.pop(i)
    return molecule_list

def htransfer_stage(molecule_list, htransfer_probability):
    num = int(len(molecule_list)*htransfer_probability)
    for _ in range(num):
        i = random.randrange(len(molecule_list))
        j = i
        while j == i:
            j = random.randrange(len(molecule_list))        
        molecule_list[i], molecule_list[j] = htransfer(molecule_list[i], molecule_list[j])
        i, j = max(i,j), min(i,j)

        if not molecule_list[i].check():
            molecule_list.pop(i)

        if not molecule_list[j].check():
            molecule_list.pop(j)

    return molecule_list

def selection_stage(molecule_list, molecule_list_restriction):
    molecule_dict = {str(molecule): molecule for molecule in molecule_list}

    
    return sorted(molecule_dict.itervalues(), key=lambda x: abs(x.HLB()-10.5))[:molecule_list_restriction]

def BGA_iteration (molecule_list, 
                    mutation_probability = 0.5,
                    htransfer_probability = 0.5,
                    molecule_list_restriction = 1000):

    #print map(lambda x: (str(x), x.HLB()), molecule_list[:10])
    molecule_list = division_stage(molecule_list)
    #print map(lambda x: (str(x), x.HLB()), molecule_list[:10])
    molecule_list = mutation_stage(molecule_list, mutation_probability)
    #print map(lambda x: (str(x), x.HLB()), molecule_list[:10])
    molecule_list = htransfer_stage(molecule_list, htransfer_probability)
    #print map(lambda x: (str(x), x.HLB()), molecule_list[:10])
    molecule_list = selection_stage(molecule_list, molecule_list_restriction)
    #print map(lambda x: (str(x), x.HLB()), molecule_list[:10])

    return molecule_list

m1 = Molecule('C', ['C']*16, 'CO_2')

num_of_iteration = 300
molecule_list = [m1]
for i in range(num_of_iteration):
    molecule_list = BGA_iteration(molecule_list)

print map(lambda x: (str(x), x.HLB()), molecule_list[:10])


