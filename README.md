#Python Workshop - January 2017

###Sean Crowe, Bill McMillin, and James Van Mil, UC Libraries
Example script by James Lee, Digital Humanities/Digital Scholarship Center - UC Libraries and UC English Department

##Scope and Purpose
We're going to go through the basic concepts of Python programming, using the script developed by James Lee, to extract key bibliographic data and match it with plant genera data, genetic data, and location data. We'll see how to apply this script to current data and how to modify it to work with other data sets.

##Setup
We'll be using Python 2.7
* Should be pre-installed in Mac and Linux
* For Windows, download from [Python.org/downloads](https://www.python.org/downloads/)

Test
* With text editor, open a file and type ```print 'hello world'``` and save it in your home directory as hello.py
* In the windows command prompt (cmd.exe) or Mac terminal, cd to your home directory and type ```python hello.py``` You should see the output of the program.

#Concepts

##Strings
* length  
```python  
len("Let's find the length of this string")
#>> 36
```
* find
```python
"Let's find a substring!".find("sub")
>> 13
# Returns '-1' if term not found
"Let's find a substring!".find("apple")
#>> -1
```
* concatenate  
```python  
"Hello " + "World"
#>> "Hello World"
```
* indexes 
```python
"Let's find a substring!".find("sub")
#>> 13
# Returns ERROR if term not found
"Let's find a substring!".find("apple")
#>> Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
   ValueError: substring not found
```
* regular expressions
```python
re.sub("a", "b", "I'm replacing all my a's with b's")
#>> "I'm replacing all my b's with b's"
```
##Variables
* assigning  
```python  
my_variable = "some string"
#>> "some string"
```
* passing to functions

##File I/O
* readers & writers
* sys.argv
 
##Functions
* parameters
* return value
