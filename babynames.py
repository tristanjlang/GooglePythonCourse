#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import sys
import re

"""Baby Names exercise

Define the extract_names() function below and change main()
to call it.

For writing regex, it's nice to include a copy of the target
text for inspiration.

Here's what the html looks like in the baby.html files:
...
<h3 align="center">Popularity in 1990</h3>
....
<tr align="right"><td>1</td><td>Michael</td><td>Jessica</td>
<tr align="right"><td>2</td><td>Christopher</td><td>Ashley</td>
<tr align="right"><td>3</td><td>Matthew</td><td>Brittany</td>
...

Suggested milestones for incremental development:
XX -Extract the year and print it
XX -Extract the names and rank numbers and just print them
XX -Get the names data into a dict and print it
XX -Build the [year, 'name rank', ... ] list and print it
XX -Fix main() to use the extract_names list
"""

def extract_names(filename):
    """
    Given a file name for baby.html, returns a list starting with the year string
    followed by the name-rank strings in alphabetical order.
    ['2006', 'Aaliyah 91', Aaron 57', 'Abagail 895', ' ...]
    """
    f = open(filename, 'rU')
    file_text = f.read()
    f.close()
    
    year = re.search(r'Popularity in \d\d\d\d', file_text)
    if year:
        year = year.group()[-4:]
    else:
        print 'ERROR: year not found in ' + filename
    
    html_rank_names = re.findall(r'<tr align="right"><td>\d+</td><td>\w+</td><td>\w+</td>', file_text)
    name_ranks = {}
    i = 0
    while i < len(html_rank_names):
        line = html_rank_names[i]
        first_tag = line.find('<td>')
        first_end_tag = line.find('</td>')
        rank = line[first_tag + 4 : first_end_tag]
        
        second_tag = first_end_tag + 9
        second_end_tag = line.find('</td>', second_tag)
        name1 = line[second_tag : second_end_tag]
        
        third_tag = second_end_tag + 9
        third_end_tag = len(line) - 5
        name2 = line[third_tag : third_end_tag]
        
        # if the names already are in the dict, skip them because they have a larger number than what is already in the dict
        if name1 not in name_ranks: name_ranks[name1] = rank
        if name2 not in name_ranks: name_ranks[name2] = rank
        i = i + 1
    
    year_name_ranks = []
    year_name_ranks.append(year)
    for name, rank in name_ranks.iteritems():
        year_name_ranks.append(name + ' ' + rank)
    year_name_ranks.sort()
    return year_name_ranks
    

def main():
  # This command-line parsing code is provided.
  # Make a list of command line arguments, omitting the [0] element
  # which is the script itself.
  args = sys.argv[1:]

  if not args:
    print 'usage: [--summaryfile] file [file ...]'
    sys.exit(1)

  # Notice the summary flag and remove it from args if it is present.
  summary = False
  if args[0] == '--summaryfile':
    summary = True
    del args[0]
  
  # +++your code here+++
  # For each filename, get the names, then either print the text output
  # or write it to a summary file
  if summary:
    # iterate through each item in args and write files
    for item in args:
      f = open(item + '.summary', 'w')
      file_text = f.write('\n'.join(extract_names(item)) + '\n')
      f.close()
  else:
    # iterate through each item in args and print to console
    for item in args:
      print '\n'.join(extract_names(item)) + '\n'
  
if __name__ == '__main__':
  main()
