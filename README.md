# Image Browser

This project leads to the development of an image browser. Given a directory, display each picture in the directory as well as
in its subdirectories. 

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)

## Installation

### Prerequisites
Pre-requisites
* Python 3.9 or higher 

Required libraries: 
* opencv-python~=4.10.0.84

Necessary standard libraries include `os`, `argparse`, and `stat` 

### Installing

```
git clone https://github.com/patrick-jennewein/CMPSCI_5420_Project1
cd projectname
pip install -r requirements.txt
```

## Usage
The program can be run with `python main.py [-h] [-rows=numrows] [-cols=numcols] dir` in the terminal.

### Examples
* `python main.py dirA` will run the program, performing a DFS on the directory `dirA`
* `python main.py -rows=1000 dirA` will do the same, but with a size of 1000 pixels height, if possible
* `python main.py -cols=1000 dirA` will do the same, but with a size of 1000 pixels width, if possible
* `python main.py -rows=1000 -cols=1000 dirA` will do the same, but with a size of 1000 pixels width and/or 1000 pixels height, if possible
* `python main.py -h` will show the help dialogue
