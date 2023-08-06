#! /usr/bin/env python

"""
A python version of caml-tex.

Known problems:
    - Trailing comments are not handled properly
        (anything after ;; is treated as output)
    - -n, -w arguments do nothing (need to understand what they did previously)
"""

import re
from optparse import OptionParser
from ocaml_eval import OCamlSession
from ocaml_writer import CamlTexFileWriter
import os

def read_options():
    """Parse options for the program. """
    parser = OptionParser()

    parser.add_option('-o', '--outfile', dest='outfile',
                      default="",
                      help='set the output .tex file')

    parser.add_option('-s', '--style', dest='style',
                        default='default',
                        help='set the pygments formatting style')

    parser.add_option('-p', '--prompt', action='store_true',
                        dest='prompt',
                        help=("set the prompt shown before each command. "
                            "If not set, no prompt is shown."))
    parser.add_option('-v', '--prompt-value', dest='promptvalue',
                        default='$',
                        help=("If -p is set, set the prompt value. "
                               "If -p is set and this value is not, the default "
                               "is used."))
    parser.add_option('-n', '--no-headers', default=False, action='store_true',
                            dest='no_headers',
                            help="If -h is set, the styling headers are not added to the file.\
                             For pre-processing ml files that will be embedded in other mlt files.")
    return parser.parse_args()

# Regular Expressions
DOC_START = r"\s*\\begin{document}\s*"
START_REGEX = r"\s*\\begin{caml_(example|example\*|eval)\s*}"
END_REGEX = r"\s*\\end{caml_(example|example\*|eval|listing)}\s*"
LISTING = r'\s*\\(begin|end){caml_listing}\s*'
ECHO_IN = r'\s*\\end{caml_example\*?}\s*'
ECHO_OUT = r'\s*\\end{caml_example}\s*'

class BadMLException(Exception):
    """
    Class to represent exceptions related
    to parsing ML from the .mlt file.
    """
    def __init__(self, message):
        self.message = message
        super(BadMLException, self).__init__()

    def __repr__(self):
        return "BadMLException: {}".format(self.message)

class BadTexException(Exception):
    """
    Class to represent exceptions related
    to parsing TeX from the .mlt file.
    """
    def __init__(self, message):
        self.message = message
        super(BadTexException, self).__init__()

    def __repr__(self):
        return "BadTexException: {}".format(self.message)

def extract_ml_statements(filepointer):
    """
    Extract ML statements from the filepointer.
    Assumed that an block starts here.
    """

    statements = []

    statement = ""

    while True:
        line = filepointer.readline()

        if line is None:
            raise BadTexException("Opened Caml Statement never closed.")

        elif re.match(END_REGEX, line):
            if len(statement) > 0:
                statements.append(statement)
            return statements, line

        statement += line

        if ";;" in line:
            statements.append(statement)

            statement = ""

def convert_to_tex(filename, outfilename, style='default', prompt=None, no_headers=False):
    """ Convert the MLT file at the path filename
        to a .tex file.
    """

    print "Starting OCaml..."
    # start up and wait for the shell to be ready
    ocaml = OCamlSession()

    print "Opening the output file..."
    # try to open the outfile as a relative path first
    try:
        if not prompt:
            writer = CamlTexFileWriter(os.getcwd() + '/' + outfilename, style=style)
        else:
            writer = CamlTexFileWriter(os.getcwd() + '/' + outfilename,
                                        prompt=prompt,
                                        style=style)
    except IOError:
        try:
            writer = CamlTexFileWriter(outfilename)
        except IOError as excep:
            print "Could not open output file: {}".format(excep)
            exit(1)

    # get the source file and the output file
    print "Opening the source file..."
    try:
        infile = open(filename, 'r')
    except IOError as excep:
        print "Input file error: {}".format(excep)
        exit(1)

    print "Reading the source file..."
    while True:

        line = infile.readline()

        # if we've hit end of line, get out of here
        if not line:
            infile.close()
            writer.close()
            return

        # case for ocaml statements that interact with the shell
        if re.match(START_REGEX, line):            
            ss, endline = extract_ml_statements(infile)

            echo_in = bool(re.match(ECHO_IN, endline))
            echo_out = bool(re.match(ECHO_OUT, endline))

            evals = [ocaml.evaluate(statement) for statement in ss]


            if echo_in and echo_out:
                writer.write_ocaml_with_evals(evals)
            elif echo_in and not echo_out:
                writer.write_ocaml_statements(ss)

        # case for ocaml listings, which do not interact with the shell
        elif re.match(LISTING, line):
            statements, _ = extract_ml_statements(infile)
            tex_statement = "".join(statements)
            writer.write_ocaml(tex_statement)

        # otherwise, this line is just .tex and should be echoed
        else:
            if re.search(DOC_START, line) and not no_headers:
                writer.write_styles()

            writer.write_tex(line)

def run():
    """
    Drive the whole program.
    """
    options, args = read_options()
    for arg in args:
        if options.outfile is "":
            out = arg + '.tex'
        else:
            out = options.outfile

        if not options.prompt and not options.style:
            convert_to_tex(arg, out)
        elif not options.prompt and options.style:
            convert_to_tex(arg, out, style=options.style, no_headers=options.no_headers)
        elif options.prompt and not options.style:
            convert_to_tex(arg, out, prompt=options.promptvalue, no_headers=options.no_headers)
        else:
            convert_to_tex(arg, out, style=options.style, prompt=options.promptvalue, no_headers=options.no_headers)
