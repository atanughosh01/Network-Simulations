'''File Generator Module'''


PATH = "./textfiles/input/input"

file_no = int(input('Enter Number of Files : '))
msg = input('Enter text : ')

if len(msg) == 15 or len(msg) == 30 or len(msg) == 50:
    while file_no:
        with open(PATH + str(file_no) + '.txt', 'w', encoding='utf-8' ) as fptr: fptr.write(msg)
        file_no -= 1
    print('Done!')

else:
    consent = input("Not Desired Length. Still Want to Write? (y/N): ")
    if consent == 'y' or consent == 'Y':
        while file_no:
            with open(PATH + str(file_no) + '.txt', 'w', encoding='utf-8' ) as fptr: fptr.write(msg)
            file_no -= 1
        print('Done!')
    else: print('Nothing Written!')


# 50 => THIS IS THE RUNNING HEAD IN UP TO FIFTY CHARACTERS
# 30 => THE IRREGULAR MOVE CANNOT LOSE
# 15 => I'M ATANU GHOSH
