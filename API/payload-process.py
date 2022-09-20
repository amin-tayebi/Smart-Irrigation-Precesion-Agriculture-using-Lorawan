import re
import sys

#separate lines based on "uplink_message"
pattern  = re.compile("uplink_message")

#create a csv file for output
sys.stdout = open("output.csv", "w")

# input file is 1.txt
for line in open("1.txt"):
    for match in re.finditer(pattern, line):
		
		#delete all list of words before "Moisture_percentage"
        alist = line.split('Moisture_percentage":')
        
        #from the remain string, take the 2 first chars 
        t = alist[-1][:2]
        
        #remove \n 
        print(t.replace('\n', ''))
        
        
        
