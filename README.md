# fetch_seq_by_string_in_header

Author: Murat Buyukyoruk

Associated lab: Wiedenheft lab

# fetch_seq_by_string_in_header help:

This script is developed to fetch sequences from a multifasta file by performing string search in the header. 

SeqIO package from Bio is required to fetch flank sequences. Additionally, tqdm is required to provide a progress bar since some multifasta files can contain long and many sequences.
        

fetch_seq_by_string_in_header dependencies:

    Bio module and SeqIO available in this package          refer to https://biopython.org/wiki/Download
    tqdm                                                    refer to https://pypi.org/project/tqdm/
	        
Syntax:

  # Method 1: Single search
    
        python fetch_seq_by_string_in_header.py -i demo.fasta -s 'vibrio sp.'
        
        OR

        python fetch_seq_by_string_in_header.py -i demo.fasta -s vibrio
 
  # Method 2: List search
    
        python fetch_seq_by_string_in_header.py -i demo.fasta -l demo_list.txt    
        
# Syntax Notes:

    Single search - If you are planning to search a single word you can type the word directly after the -s option. However, if your seach string have a space in it type your string in quotes (' or ").
    
    List search - List search provides you to seach multiple strings at once and asks you if you would like to write sequences in a single file or separately for each string searched.
    
Allowed string format examples for list search (see provided demo_list.txt): 
----------------------------------------------------------------------------
        Vibrio        (first letter uppercase)
        vibrio        (all lowercase)
        vibrio sp.    (all lowercase with space and (.) in string)
        vibrio sp     (all lowercase with space)
        vibrio_sp     (all lowercase with (_) instead of space)

Also applied for single search option except with strings containing space. Type with quotation mark instead (i.e. 'vibrio sp.' or 'vibrio sp' or 'Vibrio sp' etc)	
	
WARNING: 
--------

If you use the list search option and create a single output file, duplications in provided list will generated duplicated accession entries. (i.e. vibrio will also get vibrio sp and will generate duplicates if the list also contains vibrio sp). Use remove_dub_by_acc script to avoid any duplications for downsteam steps (link: https://github.com/WiedenheftLab/remove_dub_by_acc)	
	
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
	
# Note:
Demo file is available to use with the basic command line provided in syntax section above.

    demo.fasta                      Includes 10 genome sequence
    demo_list.txt                   Includes show list of string to be searched in headers to fetch corresponding sequences.
