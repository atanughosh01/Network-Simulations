# CSMA

SourceCode and detailed report on One, Non and P-persistent CSMA techniques

* You need to simulate the project according to the following rules.

    1. Change values of variables in ```const.py``` according to your wish. (Specially ```total_sender_number``` and ```total_receiver_number```).\
    Don't forget to modify the ```outfile_path``` also. Make sure that ```total_sender_number``` = ```total_receiver_number```.

    2. You need to create as many number of input files in ```src/textfiles/input/``` as the integer value you store in ```total_sender_number``` variable\
     in ```const.py```, if ```total_sender_number``` > number of input files, the prpgram will throw exceptions and desired results won't show up.

    3. Now make sure you're in the ```src``` folder and run ```python3 main.py``` in the terminal after deleting the ```src/textfiles/report.txt``` and\
     ```src/textfiles/analysis.txt``` files.

    4. Keep track of the live changes made on the newly generated ```analysis.txt``` and ```report.txt``` after choosing your desired CSMA\
     technique from the command line.

