#create new file based on console.log

with open(r"C:\Users\Botana\Desktop\carbometrics\console2.log", 'r') as read_obj:
    file = open("streamed.txt", "w")
    for line in read_obj:
        if ('Changer Loaded Sample' in line) or ("Processed file" in line):
            file.write(line)
    file.close()

file = open("streamed.txt", "r")

finalfile = file.readlines()
file.close()

file = open("streamed_final.txt", "w")

for x in range(1, len(finalfile), 1):
    if ('Changer Loaded Sample' in finalfile[x-1]) and ('Changer Loaded Sample' not in finalfile[x]):
        file.write(finalfile[x-1].lstrip())

    if ('Processed file' in finalfile[x-1]):
        file.write(finalfile[x-1].lstrip())
#print(len(finalfile))

if ('Processed file' in finalfile[len(finalfile)-1]):
    file.write(finalfile[x].lstrip())

file.close()
