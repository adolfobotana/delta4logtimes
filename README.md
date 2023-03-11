The software provided with modern JEOL NMR instruments allows managers to evaluate how the system has been used. Whether you need to bill different users or you want to evaluate how much instrument time is spent running certain experiments, JEOL Delta software can provide detailed information and summarize instrument time, and directly report how much to charge for each user, once a billing rate has been assigned.

But not all softwares provide such tools. For example, Delta 4.3.6, which has been released more than 16 years ago, still runs on a large number of JEOL legacy systems and it does not provide such tools. But it does provide a log of what the instrument has been doing, the console.log. This log contains a lot details about instrument actions, so how can we extract information about how much time has it employed in each experiment? We can use a script to extract the relevant lines. In this case I will show how to create such script in Python, which is a widely used scripting language in the scientific community, and programs like JEOL Jason can directly run Python scripts when needed. But you can create such script in any programming language you are comfortable with.

If we want to run a python script we first need to have python installed, and then in the (Windows) command line we type python scriptname.py. This will run the script called scriptname.py if it is located in the same folder where we call it from. We can easily call a script located in a different location or files called within the script located in other folder by just adding the full path.

The first thing that we need to do is to find lines that provide the information that we want to extract. In this case I am interested in how long did it take to run the experiments in a sample so I will focus on the lines containing 'Changer Loaded Sample', which indicate that the sample is being loaded, and the lines containing 'Processed file', which indicate that the experiment has finished running in automation and is being processed (note that this would not include experiments running outside automation, if we wanted those we could look instead for 'Upload complete for'). This action can be done with the following lines:

	with open("console.log", 'r') as read_obj:
		file = open("streamed.txt", "w")
		for line in read_obj:
			if ('Changer Loaded Sample' in line) or ("Processed file" in line):
				file.write(line)
		file.close()
		
Now we have a streamed.txt containing all lines with these strings, but there may be situations in which a sample has been loaded but no experiment was run due to some error such as failure to lock, etc., so we can remove those lines with two consecutive sample loadings:

	file = open("streamed.txt", "r")
	finalfile = file.readlines()
	file.close()
	file = open("streamed_final.txt", "w")

	for x in range(1, len(finalfile), 1):
		if ('Changer Loaded Sample' in finalfile[x-1]) and ('Changer Loaded Sample' not in finalfile[x]):
			file.write(finalfile[x-1].lstrip())
		
While we have this loop open, we can also remove those lines with multiple experiments, and just keep the line referring to the last experiment run in a sample:

	if ('Processed file' in finalfile[x-1]) and ('Changer Loaded Sample' in finalfile[x]):
		file.write(finalfile[x-1].lstrip())
		
Because of the way I have written the loop, I would still need outside the loop one last check:

	if ('Processed file' in finalfile[len(finalfile)-1]):
		file.write(finalfile[x].lstrip())
	file.close()			
	
And now we have a streamed_final.txt where every two lines I have the beggining time and end time of each sample, such as:

	28-OCT-2022 14:41:09 : ecx400 : INFO : Changer Loaded Sample
	28-OCT-2022 14:45:21 : Processed file AB_sample1_PROTON-1.jdf in 0.20563[s]
	
We could continue the script to calculate the sample time and add it to how much time the instrument was used by a user (denoted by the initials in the filename in this case). Alternatively, we could also load such file in a spreadsheet software (open it using space as delimiters) and easily work out the time employed in each sample using a formula where we evaluate if the line needs a time calculation (once every two lines) and we calculate it:

In this case we added one column to calculate the time employed in each sample. Adding all this times will give us information about how much the instrument is being used, which is key to apply for grants for new instruments. If we wanted to divide this by users we could add a few columns with some extra condition to check for user name, though it may be more useful to do so with a script, particularly if there are many users.

https://www.jeoljason.com/blog-nmr/
