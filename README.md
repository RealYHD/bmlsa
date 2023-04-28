[![Build Status](https://ci.reslate.systems/job/ydeng/job/bmlsa/job/master/badge/icon)](https://ci.reslate.systems/job/ydeng/job/bmlsa/job/master/)

# BMLSA

A Basic multi local sequence alignment tool using the Biopython implementation of the Smith-Waterman alignment algorithm. May be used as a python library, or as a full command line interface.

## Features

 - Aligns a CSV of short sequences locally to a given reference sequence
 - Outputs in a CSV with old and new positions
 - Selectable parameters for alignment
 - Compatible with broad-range of input CSV formats
 - Automatically align with all sequences in reference FASTA
 - All produced output is human readable!

 ## Install via `pip`

Just run `pip install --index-url https://git.reslate.systems/api/packages/ydeng/pypi/simple/ bmlsa` in a console that is capable of running `pip`!

## CLI Demo from Git Repo

Resources have been provided in this package for CI purposes, but you may use them to try out the program yourself!

1. Install the program
2. clone this repository
3. Change into the cloned repository directory
4. Run `bmlsa -I id -S sequence -B BLASTp tests/resources/SARS_CoV-2_genes.csv tests/resources/NC_045512_coding.fasta ./output/`

The results will show up in a `output` folder (which will be generated if it doesn't exist). Use `bmlsa -h` to see what each part of the above command does!

## More Information

For all live downloadable artifacts, build statuses, unit test results, and documentation, check out the continuous integration page for the [master branch](https://ci.reslate.systems/job/ydeng/job/bmlsa/job/master/) ([development branch](https://ci.reslate.systems/job/ydeng/job/bmlsa/job/develop/)).