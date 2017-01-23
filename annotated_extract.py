#extract.py - script courtesy of James Lee, UC Digital Humanities/Digital Scholarship Center

#we begin with import statements that bring in the libraries we'll need
import os
import sys
import csv
import json
import re

#we start off by reading arguments from the command line. This program is executed by typing the following into a terminal:
#python extract.py WoS_data.bib extractedData.json
#python just tells the command line to use the python interpreter for this script. It doesn't count as an argument.
#extract.py is the 0th argument sent to Python. 
#WoS_data.bib is the 1st argument sent to Python and we're accessing it here with sys.argv[1] and assigning it to a variable called filename
filename = sys.argv[1]
#extractedData.json is the 2nd argument and we're accessing it here with sys.argv[2] and assigning it to a variable called writefilename
writefilename = sys.argv[2]
#so far, we just have the names of the files we want to work with. Next, we need to actually open them and assign them to objects that we can work with.
readfile = open(filename)
writefile = open(writefilename, 'w')

#we're declaring an empty array where we'll be storing data
data = []

#the 'with' statement is used to do something, usually repeatedly, and then free up any resources that were used in the operation
#reading files can take up a lot of memory, so this is a good way to make sure that memory is freed when we're done working with the file
#Here, we're openining three files. The 'rb' indicates we're reading them in binary mode. 
#The 'as' assigns the stream to an object that we can work with.
with open('plant_genera_new.csv', 'rb') as plant_terms:
	with open('genetic_tools.csv', 'rb') as genetic_terms:
		with open('countries.csv', 'rb') as countries:
                        #the () indicate a method. In this case, it means "I have an object called readfile that refers to a filestream. Perform the read() method on it and assign whatever that method returns to a variable called text.
			text =  readfile.read()

                        #the import csv statement above gives us access to reader functions that work on csv files
                        #each reader will work with a different csv file
			plant_reader = csv.reader(plant_terms)
			genetic_tool_reader = csv.reader(genetic_terms)
			country_reader = csv.reader(countries)

		        #empty arrays, one for each csv file	
			plant_terms = []
			tool_terms = []
			country_terms = []
                       
                       #now we need to take all the values from the csv file and put the into arrays so we can work with the values

                        #the plant_reader object knows how many rows are in its csv file. We're telling it to perform the following 
                        #instructions for each row in that csv file
			for row in plant_reader:
                                #the first row in the csv file contains headers which we don't want in the data. 
                                #the following says 'if the 0th value (the first cell) of the row is not equal to 'Genus', do the following'
				if row[0] != 'Genus':
                                        #the append() function takes our array, plant_terms and performs the append() function with the value of row
					plant_terms.append(row)
			for row in genetic_tool_reader:
				tool_terms.append(row)
			for row in country_reader:
				country_terms.append(row)
#recall that text contains the contents of readfile, our bibliographic data. We want to know the location of the first occurrence of the workd 'Journal' and we'll store it in a variable called firstindex 
firstindex = text.find('Journal')

                        #functions begin with 'def' because we're defining the function. 
                        #the function is called inner_extractor
                        #it accepts a paramter called 'start', so we'll call it with inner_extractor(num) where num is the location we want to assign to start
			def inner_extractor(start):
				#if the vallue of start equals -1, do the following. When searching for text, if it's not found, many functions return -1
                                if start == -1:
                                        #functions return values. In this case, it returns an array with blank text and the value -1
                                        #when the function returns a value, execution stops, so if this value is returned, nothing below it will be executed
					return ['', -1]
                                #within text (our bibliographic data), find the location of '{{', starting looking at the location 'start' and store the value in a variable called startindex
				startindex = text.find('{{', start)
                                #same thing as above, but this will tell us where the end of the entry is based on where it finds '}}'
				endindex = text.find('}}', start)
                                #return an array with two vallues: all of the text starting from startindex plus 2 characters all the way to endindex and the number of endindex
				return [text[startindex + 2 : endindex], endindex]
                                #that's it. The unindent means we're at the end of the function

                        #defining a function that takes a parameter called planttext
			def plant_inner_term_extractor(planttext):
                                #call the lower() function on planttext, making all characters lowercase, add a blank space at the beginning, and assign it to a variable called text_to_search
				text_to_search = ' ' + planttext.lower()
                                #declare a variable with an empty string called search_result
				search_result = ''

                                #plant_terms came from a csv file, so it has rows. For each row, do the following
				for row in plant_terms:	
					#first try to recognize genus
                                        #within text_to_search, perform the find function, looking for a blank space followed by the lowercase text of the first cell in the row followed by a blank space. Assign the results to a subsearch_result
					subsearch_result = text_to_search.find(' ' + row[0].lower() + ' ')
                                        #if nothing was found above, subsearch_result will contain -1, so do the following
					if subsearch_result != -1:
                                                #take the search_result, append the first cell of the row, then a blank space, then the second cell of the row, then a comma
						search_result = search_result + row[0] + ' ' + row[1] + ','
					#if there is no recognized genus, search in family
					if search_result == '':
                                                #look for the second cell of the row with a blank space on either end and assign results to subsearch_result
						subsearch_result = text_to_search.find(' ' + row[1] + ' ')
                                                #if subsearch_result is not equal to -1 (meaning we found something)
						if subsearch_result != -1:
                                                        #take the second cell of the row and append it to search_result
							search_result = search_result + row[1] + ','
				return search_result

			def tool_inner_term_extractor(tooltext):
				text_to_search = tooltext.lower()
				search_result = ''

				for row in tool_terms:
					subsearch_result = text_to_search.find(' ' +row[0].lower() + ' ')
					if subsearch_result != -1:
						search_result = search_result + row[0] + ','

				return search_result

			def country_inner_term_extractor(text):
				text_to_search = text.lower()
				search_result = ''

				for row in country_terms:
					subsearch_result = text_to_search.find(' ' +row[0].lower() + ' ')
					if subsearch_result != -1:
						search_result = search_result + row[0] + ','

				return search_result


			def extractor(textindex):
				index = textindex
                                #take the text (bib data), find 'Title' starting from the index and search as far as the length of text
                                #len() is a function that returns the number of characters in a string. When we find 'Title' or run out of text to search, store the index (-1 for not found) in a variable called title_index
				title_index = text.find('Title', index, len(text))
                                #take the number from the previous step and send it to the inner_extractor function. That function returns an array with a string (the title if found or an empty string if not) and a number of the ending index or -1 if not found. Take this array and store it in a variable called title
				title = inner_extractor(title_index)
				#the first (0th) element of the array is the title text, so take that and store it in a variable called title_text
                                title_text = title[0]
                                #the index is the second value from that array
				index = title[1]

                                #find in text the word 'Journal' starting at the index. Assign it to this variable
				journal_index = text.find('Journal ', index)
                                #send the index of the word 'Journal' to the inner_extractor function
				journal = inner_extractor(journal_index)
                                #take the first value in the array stored in the journal variable and assign it to journal_text
				journal_text = journal[0]
			        #assign the second value to index	
				index = journal[1]
       
                                #the same basic search process we used above is now repeated to pull out other bibliogrpahic data
				year_index = text.find('Year', index)
				year = inner_extractor(year_index)
				year_text = year[0]
				
				index = year[1]

				abstract_index = text.find('Abstract', index)
				abstract = inner_extractor(abstract_index)
				abstract_text = abstract[0]
				
				index = abstract[1]

				affiliation_index = text.find('Affiliation', index)
				affiliation = inner_extractor(affiliation_index)
				affiliation_text = affiliation[0]
				
				index = affiliation[1]

				keywords_index = text.find('Keywords', index)
				keywords = inner_extractor(keywords_index)
				keywords_text = keywords[0]
				
				index = keywords[1]

				keywords_plus_index = text.find('Keywords-Plus', index)
				keywords_plus = inner_extractor(keywords_plus_index)
				keywords_plus_text = keywords_plus[0]
				
				index = keywords_plus[1]

				funding_index = text.find('Funding-Acknowledgement', index)
				funding = inner_extractor(funding_index)
				funding_text = funding[0]
				
				index = funding[1]

				term_search_string = title_text + ' ' + abstract_text + ' ' +  keywords_text + ' ' + keywords_plus_text

				term_search_string = re.sub(r'[^\w\s]',' ',term_search_string) 
				#print term_search_string
				focal_species =  plant_inner_term_extractor(term_search_string)
				genetic_tool =  tool_inner_term_extractor(term_search_string)
				countries =  country_inner_term_extractor(term_search_string)

				author_coo_group = affiliation_text.split('.\n')
				authors_coo = ''
				for author in author_coo_group:
					text_to_search = author.lower()
					if text_to_search.find('reprint author') != -1:
						authors_coo = authors_coo + ' Reprint Author '
					for row in country_terms:
						if text_to_search.find(row[0].lower()) != -1:
							authors_coo = authors_coo + row[0] + ', '






				if title_text != '':
					data.append({ 'focal-species' : focal_species, 'focal-species-COO' : countries, 'year' : year_text, 'journal' : journal_text, 'genetic-tool' : genetic_tool, 'authors COO(in order)' : authors_coo, 'funding-organization' : funding_text})# \n {} \n {} \n {} \n {} \n {} \n {} \n \n'.format(focal_species, countries, year_text, journal_text, genetic_tool, authors_coo, funding_text))

				return index


			total_index = 0
			while total_index >= 0:
				total_index = extractor(total_index)
				print total_index

			json.dump(data, writefile, indent=4)


			readfile.close()
			writefile.close()
