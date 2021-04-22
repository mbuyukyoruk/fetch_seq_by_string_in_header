#!/usr/bin/python

import argparse
import sys
import os
import subprocess
import re
import textwrap
import time

try:
    from Bio import SeqIO
except ImportError, e:
    print "SeqIO module is not installed! Please install SeqIO and try again."
    sys.exit()

try:
    import tqdm
except ImportError, e:
    print "tqdm module is not installed! Please install tqdm and try again."
    sys.exit()
parser = argparse.ArgumentParser(prog='python fetch_seq_by_string_in_header.py',
      formatter_class=argparse.RawDescriptionHelpFormatter,
      epilog=textwrap.dedent('''\

      	Author: Murat Buyukyoruk
      	Associated lab: Wiedenheft lab

        fetch_seq_by_string_in_header help:

This script is developed to fetch sequences from a multifasta file by performing string search in the header. 

SeqIO package from Bio is required to fetch flank sequences. Additionally, tqdm is required to provide a progress bar since some multifasta files can contain long and many sequences.
        

fetch_seq_by_string_in_header dependencies:
        Bio module and SeqIO available in this package          refer to https://biopython.org/wiki/Download
        tqdm                                                    refer to https://pypi.org/project/tqdm/
	        
Syntax:
    Method 1: Single search
    
        python fetch_seq_by_string_in_header.py -i demo.fasta -s 'vibrio sp.'
        
        OR

        python fetch_seq_by_string_in_header.py -i demo.fasta -s vibrio
 
    Method 2: List search
    
        python fetch_seq_by_string_in_header.py -i demo.fasta -l demo_list.txt    
        
Syntax Notes:

    Single search - If you are planning to search a single word you can type the word directly after the -s option. However, if your seach string have a space in it type your string in quotes (' or ").
    
    List search - List search provides you to seach multiple strings at once and asks you if you would like to write sequences in a single file or separately for each string searched.
    
Allowed string format examples for list search (see provided demo_list.txt): 

        Vibrio      (first letter uppercase)
        vibrio      (all lowercase)
        vibrio sp.  (all lowercase with space and (.) in string)
        vibrio sp   (all lowercase with space)
        vibrio_sp   (all lowercase with (_) instead of space)

Also applied for single search option except with string contain space. Type with quotation mark instead (i.e. 'vibrio sp.' or 'vibrio sp' or 'Vibrio sp' etc)	
	
WARNING: if you use the list search option and create a single output file, duplications in provided list will generated duplicated accession entries. (i.e. vibrio will also get vibrio sp and will generate duplicates if the list also contains vibrio sp). Use remove_dub_by_acc script to avoid any duplications for downsteam steps (link: https://github.com/WiedenheftLab/remove_dub_by_acc)	
	
Input Paramaters (REQUIRED):
----------------------------
	-i/--input		FASTA			Specify a multifasta file for input.

Methods:
----------------------------
	-s/--string		String			Specify a string to be searched in headers.

	-l/--list		List			Specify a name of list file that contains multiple strings in each row.

Basic Options:
--------------
	-h/--help		HELP			Shows this help text and exits the run.
	
      	'''))
parser.add_argument('-i', '--input', required=True, type=str, dest='filename',
                        help='Specify a original fasta file.\n')

parser.add_argument('-s', '--string', required=False, dest='string', default='None',
                        help='Specify a string (CAPS sensitive).\n')

parser.add_argument('-l', '--list', required=False, dest='list', default='None',
                        help='Specify a file that contain multiple string (CAPS sensitive).\n')

results = parser.parse_args()
filename = results.filename
search = results.string
list = results.list

if search == "None" and list == "None":
    print "Please specify a method. (-l for list of strings to be searched or -s to specify single string search.)"
    sys.exit()

if search != 'None':
    out = filename.split('.')[0] + "_" + search.replace(" ","_").replace(".","").capitalize() + "." + filename.split('.')[1]
    os.system('> ' + out)

    proc = subprocess.Popen("grep -c '>' " + filename, shell=True, stdout=subprocess.PIPE, )
    length = int(proc.communicate()[0].split('\n')[0])

    with tqdm.tqdm(range(length), desc = 'Fetching...' ) as pbar:
        for record in SeqIO.parse(filename, "fasta"):
            pbar.update()
            if search.lower() in record.description.lower() or search.lower().replace(" ","_") in record.description.lower() or search.lower().replace("_", " ") in record.description.lower():
                f = open(out, 'a')
                sys.stdout = f
                print '>' + record.description
                print re.sub("(.{60})", "\\1\n", str(record.seq), 0, re.DOTALL)

if list != 'None':
    timestr = time.strftime("%Y%m%d_%H%M%S")
    format = None
    while format != "single" or format != "multiple":
        format = raw_input(
            "Do you want a single outfile or multiple fasta files for each sting in the list?(Type 'single' or 'multiple')\n").lower()
        if format == "single" or format == "multiple":
            break
    name_list = []
    with open(list, 'rU') as file:
        for line in file:
            if len(line.split()) != 0:
                name = line.split('\n')[0]
                name_list.append(name)
		
    with tqdm.tqdm(range(len(name_list)), desc='Searching ') as pbar:
        for i in range(len(name_list)):
            search = name_list[i]
            pbar.update()

            if format == 'single':
                out = filename.split('.')[0] + "_search_with_" + list.split('.')[0] + "_" + timestr + "." + filename.split('.')[1]

            if format == 'multiple':
                out = filename.split('.')[0] + "_" + search.replace(" ","_").replace(".","").capitalize() + "." + filename.split('.')[1]
                os.system('> ' + out)

            proc = subprocess.Popen("grep -c '>' " + filename, shell=True, stdout=subprocess.PIPE, )
            length = int(proc.communicate()[0].split('\n')[0])

            for record in SeqIO.parse(filename, "fasta"):
                if search.lower() in record.description.lower() or search.lower().replace(" ","_") in record.description.lower() or search.lower().replace("_"," ") in record.description.lower():
                    f = open(out, 'a')
                    sys.stdout = f
                    print '>' + record.description
                    print re.sub("(.{60})", "\\1\n", str(record.seq), 0, re.DOTALL)
