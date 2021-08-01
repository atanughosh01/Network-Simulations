#!/usr/bin/python3
""" 1. Write a single python program to do the following operations on a text file by writing
different user defined functions.
a. Remove all the special characters.
b. Remove all single characters.
c. Substitute multiple spaces with single space.
d. Convert all the words into Lowercase.
e. Convert the words into literal form from their contracted form (e.g., Couldn’t => Could
not) """


class TextProcessor:

    def __init__(self):
    	"""dictionary of words with contracted words as KEY and uncontracted words as VALUE"""
    	self.contractions = {
            "ain't": "am not / are not",
            "aren't": "are not / am not",
            "can't": "cannot",
            "can't've": "cannot have",
            "'cause": "because",
            "could've": "could have",
            "couldn't": "could not",
            "couldn't've": "could not have",
            "didn't": "did not",
            "doesn't": "does not",
            "don't": "do not",
            "hadn't": "had not",
            "hadn't've": "had not have",
            "hasn't": "has not",
            "haven't": "have not",
            "he'd": "he had / he would",
            "he'd've": "he would have",
            "he'll": "he shall / he will",
            "he'll've": "he shall have / he will have",
            "he's": "he has / he is",
            "how'd": "how did",
            "how'd'y": "how do you",
            "how'll": "how will",
            "how's": "how has / how is",
            "i'd": "I had / I would",
            "i'd've": "I would have",
            "i'll": "I shall / I will",
            "i'll've": "I shall have / I will have",
            "i'm": "I am",
            "i've": "I have",
            "isn't": "is not",
            "it'd": "it had / it would",
            "it'd've": "it would have",
            "it'll": "it shall / it will",
            "it'll've": "it shall have / it will have",
            "it's": "it has / it is",
            "let's": "let us",
            "ma'am": "madam",
            "mayn't": "may not",
            "might've": "might have",
            "mightn't": "might not",
            "mightn't've": "might not have",
            "must've": "must have",
            "mustn't": "must not",
            "mustn't've": "must not have",
            "needn't": "need not",
            "needn't've": "need not have",
            "o'clock": "of the clock",
            "oughtn't": "ought not",
            "oughtn't've": "ought not have",
            "shan't": "shall not",
            "sha'n't": "shall not",
            "shan't've": "shall not have",
            "she'd": "she had / she would",
            "she'd've": "she would have",
            "she'll": "she shall / she will",
            "she'll've": "she shall have / she will have",
            "she's": "she has / she is",
            "should've": "should have",
            "shouldn't": "should not",
            "shouldn't've": "should not have",
            "so've": "so have",
            "so's": "so as / so is",
            "that'd": "that would / that had",
            "that'd've": "that would have",
            "that's": "that has / that is",
            "there'd": "there had / there would",
            "there'd've": "there would have",
            "there's": "there has / there is",
            "they'd": "they had / they would",
            "they'd've": "they would have",
            "they'll": "they shall / they will",
            "they'll've": "they shall have / they will have",
            "they're": "they are",
            "they've": "they have",
            "to've": "to have",
            "wasn't": "was not",
            "we'd": "we had / we would",
            "we'd've": "we would have",
            "we'll": "we will",
            "we'll've": "we will have",
            "we're": "we are",
            "we've": "we have",
            "weren't": "were not",
            "what'll": "what shall / what will",
            "what'll've": "what shall have / what will have",
            "what're": "what are",
            "what's": "what has / what is",
            "what've": "what have",
            "when's": "when has / when is",
            "when've": "when have",
            "where'd": "where did",
            "where's": "where has / where is",
            "where've": "where have",
            "who'll": "who shall / who will",
            "who'll've": "who shall have / who will have",
            "who's": "who has / who is",
            "who've": "who have",
            "why's": "why has / why is",
            "why've": "why have",
            "will've": "will have",
            "won't": "will not",
            "won't've": "will not have",
            "would've": "would have",
            "wouldn't": "would not",
            "wouldn't've": "would not have",
            "y'all": "you all",
            "y'all'd": "you all would",
            "y'all'd've": "you all would have",
            "y'all're": "you all are",
            "y'all've": "you all have",
            "you'd": "you had / you would",
            "you'd've": "you would have",
            "you'll": "you shall / you will",
            "you'll've": "you shall have / you will have",
            "you're": "you are",
            "you've": "you have"
        }


    def del_special_char(self, s: str) -> str:
        """Remove special characters, i.e. characters which are not alphanumeric or whitespaces"""
        new_str = ''
        for element in s:
            if element.isalnum() or element.isspace():
                new_str += element
        print('\n _________________ Text From Input File _________________\n\n' + s)
        return new_str


    def del_single_char(self, s: str) -> str:
        """Remove single characters, i.e. characters of length = 1 (a non-space character surrounded by whitespaces)"""
        new_str = ''
        for (i, ch) in enumerate(s):
            if not ch.isspace() and not ((i == 0 and s[i+1].isspace()) or (i == (len(s)-1) and s[i-1].isspace()) or (s[i-1].isspace() and s[i+1].isspace())):
                new_str += ch
            elif ch.isspace():
                new_str += ch
        print('\n _________________ Text From Input File _________________\n\n' + s)
        return new_str


    def sub_mul_space(self, s: list, t: str) -> str:
        """Remove multiple whitespaces and substitute those with a single whitespace"""
        new_str = ''
        for whole_line in s:
            char_list = whole_line.split()
            no_newline = ' '.join(char_list)
            new_str += '\n' + no_newline
        print('\n _________________ Text From Input File _________________\n\n' + t)
        return new_str


    def convto_lower(self, s: str) -> str:
        """Convert all uppercase alphabatical characters to lowercase"""
        new_str = s.lower()
        print('\n _________________ Text From Input File _________________\n\n' + s)
        return new_str


    def convto_literal(self, s: str) -> str:
        """Convert contracted forms of characters ('can't') to their uncontracted forms ('cannot')"""
        old_str = s
        for element in s.split():
            if element.lower() in self.contractions:
                not_contracted = self.contractions[element.lower()]
                s = s.replace(element, not_contracted)
        new_str = s
        print('\n _________________ Text From Input File _________________\n\n' + old_str)
        return new_str


class DriverCode:

    def proc_func(self):
    	# creating a reference of class TextProcessor to implement different functionalities
        textP = TextProcessor()
        while True:
            print("\n\n\n Choose Option From the Menu Below to Process Text Read Feom the Input File (input.txt)\n")
            print("  ----------------------------- Transformation Menu ------------------------------- ")
            print("  |                                                                               | ")
            print("  |       a. Remove all special characters                                        | ")
            print("  |       b. Remove all single characters                                         | ")
            print("  |       c. Substitute multiple spaces with single space                         | ")
            print("  |       d. Convert all words into Lowercase                                     | ")
            print("  |       e. Convert the words into literal form from their contracted form       | ")
            print("  |       f. EXIT MENU                                                            | ")
            print("  |                                                                               | ")
            print("  --------------------------------------------------------------------------------- ")

            choice = input("\n Enter Your Choice : ")

            # using if-elif-else statement to pick different options
            if choice == 'a' or choice == 'A':
                try:
                    fin = open('input.txt', 'r')
                    lines = fin.read()
                    print('\n\n _______________ Text Without Special Characters _______________\n\n' + textP.del_special_char(lines))
                except Exception as ex:
                    print('\n Exception Caught :', ex)
                finally:
                    fin.close()

            elif choice == 'b' or choice == 'B':
                try:
                    fin = open('input.txt', 'r')
                    lines = fin.read()
                    print('\n\n _______________ Text Without Single Characters _______________\n\n' + textP.del_single_char(lines))
                except Exception as ex:
                    print('\n Exception Caught :', ex)
                finally:
                    fin.close()

            elif choice == 'c' or choice == 'C':
                try:
                    fin = open('input.txt', 'r')
                    file = open('input.txt', 'r')
                    lines = file.readlines()
                    text = fin.read()
                    print('\n\n _______________ Text Without Multiple Spaces _______________\n' + textP.sub_mul_space(lines, text))
                except Exception as ex:
                    print('\n Exception Caught :', ex)
                finally:
                    fin.close()
                    file.close()

            elif choice == 'd' or choice == 'D':
                try:
                    fin = open('input.txt', 'r')
                    lines = fin.read()
                    print('\n\n _______________ Text Converted to LowerCase _______________\n\n' + textP.convto_lower(lines))
                except Exception as ex:
                    print('\n Exception Caught :', ex)
                finally:
                    fin.close()

            elif choice == 'e' or choice == 'E':
                try:
                    fin = open('input.txt', 'r')
                    lines = fin.read()
                    print('\n\n _______________ Text Converted into LiteralForm _______________\n\n' + textP.convto_literal(lines))
                except Exception as ex:
                    print('\n Exception Caught :', ex)
                finally:
                    fin.close()

            elif choice == 'f' or choice == 'F' or choice == '' or choice == '\n':
                print("\n EXITING MENU....EXITED.\n")
                break

            else:
                print("\n Choice OUT OF RANGE!\n Please Choose within {a, b, c, d, e, f}.")



dc_obj = DriverCode()


def main():
    dc_obj.proc_func()


if __name__ == '__main__':
    main()
