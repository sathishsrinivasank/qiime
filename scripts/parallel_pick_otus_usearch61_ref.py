#!/usr/bin/env python
# File created on 07 Jul 2012
from __future__ import division

__author__ = "Greg Caporaso"
__copyright__ = "Copyright 2011, The QIIME project"
__credits__ = ["Greg Caporaso"]
__license__ = "GPL"
__version__ = "1.6.0-dev"
__maintainer__ = "Greg Caporaso"
__email__ = "gregcaporaso@gmail.com"
__status__ = "Development"


from qiime.util import (parse_command_line_parameters,
                        get_options_lookup,
                        make_option)
from qiime.parallel.pick_otus import ParallelPickOtusUsearch61Ref


############################
# Script functionality

options_lookup = get_options_lookup()

script_info={}
script_info['brief_description']="""Parallel pick otus using usearch_ref"""
script_info['script_description']="""This script works like the pick_otus.py script, but is intended to make use of multicore/multiprocessor environments to perform analyses in parallel."""
script_info['script_usage']=[]
script_info['script_usage'].append(("""Example""","""Pick OTUs by searching $PWD/inseqs.fasta against $PWD/refseqs.fasta with reference-based usearch and write the output to the $PWD/usearch_ref_otus/ directory. This is a closed-reference OTU picking process. ALWAYS SPECIFY ABSOLUTE FILE PATHS (absolute path represented here as $PWD, but will generally look something like /home/ubuntu/my_analysis/).""","""%prog -i $PWD/seqs.fna -r $PWD/refseqs.fna -o $PWD/usearch_ref_otus/ --suppress_reference_chimera_detection"""))
script_info['output_description']=""""""

script_info['required_options'] = [\
    make_option('-i','--input_fasta_fp',action='store',\
           type='existing_filepath',help='full path to '+\
           'input_fasta_fp'),
           
    make_option('-o','--output_dir',action='store',\
           type='new_dirpath',help='path to store output files'),
          
    make_option('-r','--refseqs_fp',action='store',\
           type='existing_filepath',help='full path to '+\
           'reference collection')
]

script_info['optional_options'] = [\
         
    make_option('-s','--similarity',action='store',\
          type='float',help='Sequence similarity '+\
          'threshold [default: %default]',default=0.97),
        
 options_lookup['jobs_to_start'],
 options_lookup['retain_temp_files'],
 options_lookup['suppress_submit_jobs'],
 options_lookup['poll_directly'],
 options_lookup['cluster_jobs_fp'],
 options_lookup['suppress_polling'],
 options_lookup['job_prefix'],
 options_lookup['seconds_to_sleep']
]

script_info['version'] = __version__



def main():
    option_parser, opts, args = parse_command_line_parameters(**script_info)

    # create dict of command-line options
    params = eval(str(opts))
    
    parallel_runner = ParallelPickOtusUsearch61Ref(
                                        cluster_jobs_fp=opts.cluster_jobs_fp,
                                        jobs_to_start=opts.jobs_to_start,
                                        retain_temp_files=opts.retain_temp_files,
                                        suppress_polling=opts.suppress_polling,
                                        seconds_to_sleep=opts.seconds_to_sleep)
    parallel_runner(opts.input_fasta_fp,
                    opts.output_dir,
                    params,
                    job_prefix=opts.job_prefix,
                    poll_directly=opts.poll_directly,
                    suppress_submit_jobs=False)


if __name__ == "__main__":
    main()