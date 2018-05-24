from enum import Enum

CLASS_LIST = ['Y', 'Z', 'J', 'S', 'D', 'B', 'F', 'I', 'M', 'H', 'Q', 'V', 'K', 'L', 'X', 'R', 'T', 'G', 'N', 'A', 'P',
              'W', 'C', 'O', 'U', 'E', 'Closed', 'Other']

SUBCLASS_CLOSED = "Closed"


class ClassList(Enum):
    Subclass_Y = 1
    Subclass_Z = 2
    Subclass_J = 3
    Subclass_S = 4
    Subclass_D = 5
    Subclass_B = 6
    Subclass_F = 7
    Subclass_I = 8
    Subclass_M = 9
    Subclass_H = 10
    Subclass_Q = 11
    Subclass_V = 12
    Subclass_K = 13
    Subclass_L = 14
    Subclass_X = 15
    Subclass_R = 16
    Subclass_T = 17
    Subclass_G = 18
    Subclass_N = 19
    Subclass_A = 20
    Subclass_P = 21

    # rest
    Subclass_W = 22
    Subclass_C = 23
    Subclass_O = 24
    Subclass_U = 25
    Subclass_E = 26
    Subclass_Closed = 27
    Subclass_Last = 28

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented

    def get_subclass_letter(self):
        """

        :return: the subclass letter based on the value of the ClassList Enum
        """
        if 1 <= self.value <= len(CLASS_LIST):
            return CLASS_LIST[self.value - 1]
        else:
            return "Unknown"

    def get_subclass_number(self):
        return self.value


def get_las(subclass):
    if subclass == SUBCLASS_CLOSED:
        return ClassList.Subclass_Closed
    elif subclass == '':
        return ClassList.Subclass_Last
    else:
        subclass_name = 'Subclass_' + subclass
        return ClassList[subclass_name]