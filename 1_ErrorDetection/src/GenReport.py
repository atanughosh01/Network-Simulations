# parses through the result-files to display accuracy report
import sys

while True:
    inp = input("\nEnter filename to generate report : ")
    try:
        with open("textfiles/" + inp, "r") as text_file:
            line_no, count1, count2 = 0, 0, 0
            for line in text_file:
                if line.startswith("NO "): count1 += 1
                elif line.startswith("ERROR "): count2 += 1
                line_no = count1 + count2
                accuracy = (count2/line_no)*100
                inaccuracy = (count1/line_no)*100
        print("\nNumber of total errors to test on = " + str(line_no))
        print("Number of errors skipped : " + str(count1))
        print("Number of errors caught : " + str(count2))
        print("Percentage accuracy of detecting error of this scheme = " + str(accuracy) + " %")
        print("Percentage inaccuracy of detecting error of this scheme = " + str(inaccuracy) + " %\n")
    except Exception as ex:
        print("[EXCEPTION 1] " + str(ex))
        continue
