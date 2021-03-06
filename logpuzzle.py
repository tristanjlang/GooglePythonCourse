#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import os
import re
import sys
import urllib

"""Logpuzzle exercise
Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""


def read_urls(filename):
    """Returns a list of the puzzle urls from the given log file,
    extracting the hostname from the filename itself.
    Screens out duplicate urls and returns the urls sorted into
    increasing order."""
    # +++your code here+++
    underbar = filename.find('_')
    if underbar != -1:
        server = filename[underbar + 1 : ]
    else:
        sys.stderr.write('ERROR: invalid filename\n')
        sys.exit(1)
    
    f = open(filename, 'rU')
    text = f.read()
    paths = re.findall(r'GET\s([/\~\w\d-]*puzzle[/\~\w\d\.-]*)\s', text)
    
    urls = []
    for path in paths:
        url = 'http://' + server + path
        special = is_special_sortable(url)
        if url not in urls and not special:
            urls.append(url)
        elif special not in urls:
            urls.append(special)
    
    if special:
        return [t[0] for t in sorted(urls, key = lambda t:t[1])]
    else:
        return sorted(urls)


def is_special_sortable(url):
    last_slash = url.rfind('/')
    filename = url[last_slash + 1 : ]
    match = re.search(r'-[\w]+-([\w]+)\.jpg', filename)
    if match:
        return (url, match.group(1))
    else:
        return False


def download_images(img_urls, dest_dir):
    """Given the urls already in the correct order, downloads
    each image into the given directory.
    Gives the images local filenames img0, img1, and so on.
    Creates an index.html in the directory
    with an img tag to show each local image file.
    Creates the directory if necessary.
    """
    # +++your code here+++
    if len(dest_dir) == 0:
        sys.stderr.write('ERROR: invalid destination directory\n')
        sys.exit(1)
    
    if len(img_urls) == 0:
        sys.stderr.write('ERROR: invalid image list\n')
        sys.exit(1)
    
    # dest_dir is subdirectory of pwd
    # set up absolute destination directory
    pwd = os.getcwd()
    if dest_dir[0] == '/':
        abs_dest_dir = pwd + dest_dir
    else:
        abs_dest_dir = pwd + '/' + dest_dir
    if abs_dest_dir[-1] != '/': abs_dest_dir += '/'
        
    # if the path doesn't exist, create it
    if not os.path.exists(abs_dest_dir):
        os.makedirs(abs_dest_dir)

    # download files
    count = 0
    for img in img_urls:
        print 'Retrieving... img' + str(count)
        urllib.urlretrieve(img, abs_dest_dir + 'img' + str(count))
        count += 1
    
    # create index.html that combines the images
    f = open(abs_dest_dir + 'index.html', 'w')
    f.write('<html>\n<body>\n')
    img_line = ''
    for i in range(0, count):
        img_line += '<img src="' + abs_dest_dir + 'img' + str(i) + '">'
    f.write(img_line + '\n</body>\n</html>\n')
    f.close()


def main():
  args = sys.argv[1:]

  if not args:
    print 'usage: [--todir dir] logfile '
    sys.exit(1)

  todir = ''
  if args[0] == '--todir':
    todir = args[1]
    del args[0:2]

  img_urls = read_urls(args[0])

  if todir:
    download_images(img_urls, todir)
  else:
    print '\n'.join(img_urls)

if __name__ == '__main__':
  main()
