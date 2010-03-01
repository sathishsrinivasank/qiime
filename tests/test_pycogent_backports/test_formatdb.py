#!/usr/bin/env python
# File created on 01 Mar 2010
from __future__ import division

__author__ = "Greg Caporaso"
__copyright__ = "Copyright 2010, The QIIME project"
__credits__ = ["Greg Caporaso"]
__license__ = "GPL"
__version__ = "1.0-dev"
__maintainer__ = "Greg Caporaso"
__email__ = "gregcaporaso@gmail.com"
__status__ = "Pre-release"
 
from os.path import exists
from cogent import LoadSeqs
from cogent.util.unit_test import TestCase, main
from cogent.app.util import get_tmp_filename
from cogent.util.misc import remove_files
from cogent.app.blast import blastn
from qiime.pycogent_backports.formatdb import build_blast_db_from_fasta_file

class FormatdbTests(TestCase):

    def setUp(self):
        """ """
        self.test_seq = test_seq
        
        self.in_aln1_fp =\
         get_tmp_filename(prefix='FormatDbTests',suffix='.fasta')
        self.in_aln1_file = open(self.in_aln1_fp,'w')
        self.in_aln1_file.write(in_aln1)
        self.in_aln1_file.close()
        self.in_aln1 = LoadSeqs(self.in_aln1_fp)
        
        self.files_to_remove = [self.in_aln1_fp]
    
    def tearDown(self):
        remove_files(self.files_to_remove)
    
    def test_build_blast_db_from_fasta_file(self):
        """build_blast_db_from_fasta_file works with open files as input
        """
        blast_db, db_files = \
         build_blast_db_from_fasta_file(open(self.in_aln1_fp),output_dir='/tmp/')
        self.assertTrue(blast_db.startswith('/tmp/BLAST_temp_db'))
        self.assertTrue(blast_db.endswith('.fasta'))
        expected_db_files = set([blast_db] + [blast_db + ext\
         for ext in ['.nhr','.nin','.nsq','.nsd','.nsi','.log']])
        self.assertEqual(set(db_files),expected_db_files)
        # result returned when blasting against new db
        self.assertEqual(\
            len(blastn(self.test_seq,blast_db=blast_db,e_value=0.0)),1)
        
        # Make sure all db_files exist
        for fp in db_files:
            self.assertTrue(exists(fp))
        
        # Remove all db_files exist   
        remove_files(db_files)
        
        # Make sure nothing weird happened in the remove
        for fp in db_files:
            self.assertFalse(exists(fp))

test_seq = """>s1 (11472384)
AGAGTTTGATCCTGGCTCAGATTGAACGCTGGCGGCATGCCTTACACATGCAAGTCGAACGGCAGCACGGGGGCAACCCTGGTGGCGAGTGGCGAACGGGTGAGTAATACATCGGAACGTGTCCTGTAGTGGGGGATAGCCCGGCGAAAGCCGGATTAATACCGCATACGCTCTACGGAGGAAAGGGGGGGATCTTAGGACCTCCCGCTACAGGGGCGGCCGATGGCAGATTAGCTAGTTGGTGGGGTAAAGGCCTACCAAGGCGACGATCTGTAGCTGGTCTGAGAGGACGACCAGCCACACTGGGACTGAGACACGGCCCAGACTCCTACGGGAGGCAGCAGTGGGGAATTTTGGACAATGGGGGCAACCCTGATCCAGCAATGCCGCGTGTGTGAAGAAGGCCTTCGGGTTGTAAAGCACTTTTGTCCGGAAAGAAAACGCCGTGGTTAATACCCGTGGCGGATGACGGTACCGGAAGAATAAGCACCGGCTAACTACGTGCCAGCAGCCGCGGTAATACGTAGGGTGCAAGCGTTAATCGGAATTACTGGGCGTAAAGCGTGCGCAGGCGGTCCGCTAAGACAGATGTGAAATCCCCGGGCTTAACCTGGGAACTGCATTTGTGACTGGCGGGCTAGAGTATGGCAGAGGGGGGTAGAATTCCACGTGTAGCAGTGAAATGCGTAGAGATGTGGAGGAATACCGATGGCGAAGGCAGCCCCCTGGGCCAATACTGACGCTCATGCACGAAAGCGTGGGGAGCAAACAGGATTAGATACCCTGGTAGTCCACGCCCTAAACGATGTCAACTAGTTGTCGGGTCTTCATTGACTTGGTAACGTAGCTAACGCGTGAAGTTGACCGCCTGGGGAGTACGGTCGCAAGATTAAAACTCAAAGGAATTGACGGGGACCCGCACAAGCGGTGGATGATGTGGATTAATTCGATGCAACGCGAAAAACCTTACCTACCCTTGACATGTATGGAATCCTGCTGAGAGGTGGGAGTGCCCGAAAGGGAGCCATAACACAGGTGCTGCATGGCTGTCGTCAGCTCGTGTCGTGAGATGTTGGGTTAAGTCCCGCAACGAGCGCAACCCTTGTCCCTAGTTGCTACGCAAGAGCACTCTAGGGAGACTGCCGGTGACAAACCGGAGGAAGGTGGGGATGACGTCAAGTCCTCATGGCCCTTATGGGTAGGGCTTCACACGTCATACAATGGTCGGAACAGAGGGTCGCCAACCCGCGAGGGGGAGCCAATCCCAGAAAACCGATCGTAGTCCGGATCGCACTCTGCAACTCGAGTGCGTGAAGCTGGAATCGCTAGTAATCGCGGATCAGCATGCCGCGGTGAATACGTTCCCGGGTCTTGTACACACCGCCCGTCACACCATGGGAGTGGGTTTTACCAGAAGTGGCTAGTCTAACCGCAAGGAGGACGGTCACCACGGTAGGATTCATGACTGGGGTGAAGTCGTAACAAGGTAGCCGTATCGGAAGGTGCGGCTGGATCACCTCCTTTCTCGAGCGAACGTGTCGAACGTTGAGCGCTCACGCTTATCGGCTGTGAAATTAGGACAGTAAGTCAGACAGACTGAGGGGTCTGTAGCTCAGTCGGTTAGAGCACCGTCTTGATAAGGCGGGGGTCGATGGTTCGAATCCATCCAGACCCACCATTGTCT
"""

in_aln1 = """>a1
AAACCTTT----TTTTAAATTCCGAAGAGTTTGATCCTGGCTCAGATTGAACGCTGGCGGCATGCCTTACACATGCAAGTCGAACGGCAGCACGGGGGCAACCCTGGTGGCGAGTGGCGAACGGGTGAGTAATACATCGGAACGTGTCCTGTAGTGGGGGATAGCCCGGCGAAAGCCGGATTAATACCGCATACGCTCTACGGAGGAAAGGGGGGGATCTTAGGACCTCCCGCTACAGGGGCGGCCGATGGCAGATTAGCTAGTTGGTGGGGTAAAGGCCTACCAAGGCGACGATCTGTAGCTGGTCTGAGAGGACGACCAGCCACACTGGGACTGAGACACGGCCCAGACTCCTACGGGAGGCAGCAGTGGGGAATTTTGGACAATGGGGGCAACCCTGATCCAGCAATGCCGCGTGTGTGAAGAAGGCCTTC
>a2
AAACCTTT----TTTTAAATTCCGCAGAGTTTGATCCTGGCTCAGATTGAACGCTGGCGGCATGCCTTACACATGCAAGTCGAACGGCAGCACGGGGGCAACCCTGGTGGCGAGTGGCGAACGGGTGAGTAATACATCGGAACGTGTCCTGTAGTGGGGGATAGCCCGGCGAAAGCCGGATTAATACCGCATACGCTCTACGGAGGAAAGGGGGGGATCTTAGGACCTCCCGCTACAGGGGCGGCCGATGGCAGATTAGCTAGTTGGTGGGGTAAAGGCCTACCAAGGCGACGATCTGTAGCTGGTCTGAGAGGACGACCAGCCACACTGGGACTGAGACACGGCCCAGACTCCTACGGGAGGCAGCAGTGGGGAATTTTGGACAATGGGGGCAACCCTGATCCAGCAATGCCGCGTGTGTGAAGAAGGCCTTC
>a3
AAACCTTT----TTTTAAATTCCGGAGAGTTTGATCCTGGCTCAGATTGAACGCTGGCGGCATGCCTTACACATGCAAGTCGAACGGCAGCACGGGGGCAACCCTGGTGGCGAGTGGCGAACGGGTGAGTAATACATCGGAACGTGTCCTGTAGTGGGGGATAGCCCGGCGAAAGCCGGATTAATACCGCATACGCTCTACGGAGGAAAGGGGGGGATCTTAGGACCTCCCGCTACAGGGGCGGCCGATGGCAGATTAGCTAGTTGGTGGGGTAAAGGCCTACCAAGGCGACGATCTGTAGCTGGTCTGAGAGGACGACCAGCCACACTGGGACTGAGACACGGCCCAGACTCCTACGGGAGGCAGCAGTGGGGAATTTTGGACAATGGGGGCAACCCTGATCCAGCAATGCCGCGTGTGTGAAGAAGGCCTTC
>a4
AAACCTTT----TTTTAAATTCCGTAGAGTTTGATCCTGGCTCAGATTGAACGCTGGCGGCATGCCTTACACATGCAAGTCGAACGGCAGCACGGGGGCAACCCTGGTGGCGAGTGGCGAACGGGTGAGTAATACATCGGAACGTGTCCTGTAGTGGGGGATAGCCCGGCGAAAGCCGGATTAATACCGCATACGCTCTACGGAGGAAAGGGGGGGATCTTAGGACCTCCCGCTACAGGGGCGGCCGATGGCAGATTAGCTAGTTGGTGGGGTAAAGGCCTACCAAGGCGACGATCTGTAGCTGGTCTGAGAGGACGACCAGCCACACTGGGACTGAGACACGGCCCAGACTCCTACGGGAGGCAGCAGTGGGGAATTTTGGACAATGGGGGCAACCCTGATCCAGCAATGCCGCGTGTGTGAAGAAGGCCTTC
"""

if __name__ == "__main__":
    main()