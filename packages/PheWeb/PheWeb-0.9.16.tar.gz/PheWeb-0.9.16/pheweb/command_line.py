#!/usr/bin/env python3
# -*- mode: python -*-

import sys
import os
import importlib
import functools
import math

if sys.version_info.major < 3:
    print("Sorry, PheWeb doesn't work on Python 2.  Please use Python 3 by installing it with `pip3 install pheweb`.")
    sys.exit(1)

# math.inf was introduced in python3.5
try: math.inf
except AttributeError: math.inf = float('inf')

if 'PHEWEB_DEBUG' in os.environ:
    # from <http://ipython.readthedocs.io/en/stable/interactive/reference.html#post-mortem-debugging>
    from IPython.core import ultratb
    sys.excepthook = ultratb.FormattedTB(mode='Verbose', color_scheme='Linux', call_pdb=1)

handlers = {}
for submodule in '''
 phenolist
 get_cpras
 merge_cpras
 download_rsids
 download_genes
 make_gene_aliases_trie
 add_rsids
 make_tries
 standardize_phenos
 make_manhattan
 make_qq
 make_matrix
 bgzip_phenos
 top_hits
 gather_pvalues_for_each_gene
 process_assoc_files
 make_wsgi
 top_loci
'''.split():
    def f(submodule, argv):
        module = importlib.import_module('.load.{}'.format(submodule), __package__)
        module.run(argv)
    handlers[submodule.replace('_', '-')] = functools.partial(f, submodule)

def serve_run(argv):
    from pheweb.serve import serverun
    serverun.run(argv)
handlers['serve'] = serve_run


def help():
    from pheweb import version
    print('''\
PheWeb {}

To see more information about a subcommand, run that command followed by `-h`.

Subcommands:

    pheweb phenolist
        prepare a list of phenotypes

    pheweb process-assoc-files
        once a phenolist has been prepared, load all data to be ready to run the server.

    pheweb serve
        host a webserver

    pheweb make-wsgi
        make wsgi.py, which can be used with gunicorn or other WSGI-compatible webservers.

    pheweb top-hits
        make top-hits.tsv, which contains variants that:
            - have a p-value < 10^-6
            - have a better p-value than every variant within 500kb in the same phenotype.

    pheweb top-loci
        make top-loci.tsv, which contains variants that:
            - have a p-value < 10^-6
            - have a better p-value than every variant within 500kb
            - have a better p-value than every variant within 1Mb in the same phenotype.
'''.format(version.version))


def main():
    subcommand = sys.argv[1] if len(sys.argv)>1 else ''
    if subcommand in ['', '-h', '--help']:
        help()
    elif subcommand not in handlers:
        print('Unknown subcommand {!r}'.format(subcommand))
        help()
    else:
        handlers[subcommand](sys.argv[2:])
