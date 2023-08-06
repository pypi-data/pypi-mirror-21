# Installation

These are advanced instructions for installing a development version of Agalma
from the git repository. See the Quick Install section of the README for
instructions on how to install a release version using Docker or Anaconda
Python.

See [TUTORIAL](https://bitbucket.org/caseywdunn/agalma/src/master/TUTORIAL.md)
for an example of how to use Agalma with a sample dataset.

## Reference list of dependencies

Python modules:

* [biolite](https://bitbucket.org/caseywdunn/biolite) (the release version or
  development branch must match that of Agalma)
* all python dependencies for biolite

Third-party tools called from Agalma, which need to be in your PATH:

* [biolite-tools 0.4.0](https://bitbucket.org/caseywdunn/biolite)
* [Blast 2.5.0](http://blast.ncbi.nlm.nih.gov/)
* [Bowtie 1.1.2](http://bowtie-bio.sourceforge.net/)
* [Bowtie2 2.3.0](http://bowtie-bio.sourceforge.net/bowtie2/)
* [DETONATE 1.11](http://deweylab.biostat.wisc.edu/detonate/)
* [FastQC 0.11.5](http://www.bioinformatics.babraham.ac.uk/projects/fastqc/)
* [Gblocks 0.91b](http://molevol.cmima.csic.es/castresana/Gblocks.html)
* [MAFFT 7.305](http://mafft.cbrc.jp/alignment/software/)
* [mcl 14.137](http://micans.org/mcl)
* [GNU parallel 20160622](http://savannah.gnu.org/projects/parallel)
* [RAxML 8.2.9](http://sco.h-its.org/exelixis/web/software/raxml/)
* [RSEM 1.3.0](http://deweylab.biostat.wisc.edu/rsem/)
* [samtools 1.2](http://samtools.sourceforge.net/)
* [SRA Toolkit 2.8.0](http://trace.ncbi.nlm.nih.gov/Traces/sra/sra.cgi?view=std)
* [sqlite3](http://www.sqlite.org)
* [transdecoder 2.1.0](http://transdecoder.sourceforge.net/)
* [Trinity 2.3.2](http://trinityrnaseq.sourceforge.net/)  

## Installing dependencies for development

Installing a release version of Agalma using Anaconda Python will automatically
install all the needed dependencies listed above. For a development version,
you can simply install the latest Agalma release then remove it (leaving all
of the dependencies still installed):

    conda create -c dunnlab -n agalma-dev agalma
    conda remove -n agalma-dev agalma

Now you can activate the "agalma-dev" environment, which will contain all of
the dependencies:

    source activate agalma-dev

## Installing Agalma form the git repo

For development work, or to access more recent features that are available
in the development branch, you can install Agalma directly from the git
repository:

    git clone https://bitbucket.org/caseywdunn/agalma.git
    cd agalma
    python setup.py install

If you edit the code in the repository, or pull a new version, then run the
following to update the installation:

    python setup.py install

You can use the development version of Agalma by checking out the devel branch
and reinstalling:

    git checkout devel
    python setup.py install

## Generating a tarball from the git repo

First, regenerate the BLAST databases that are packaged with Agalma using the
scripts in the `dev` subdirectory:

    mkdir -p agalma/blastdb
    cd dev
    bash build-nt-rrna.sh
    bash build-swissprot.sh
    bash build-univec.sh

This will download a subset of the current GenBank (nt) database with only
titles containing "rrna", the current release of SwissProt, and the current
release of UniVec. The SwissProt database is parsed into a FASTA file that
includes the OG (Organelle) field in the description line.

The databases are packaged in their own download with:

    cd agalma
    zip -r ../agalma-blastdb-X.X.X.zip blastdb
    cd ..

Then create a source distribution for Agalma with `distutils`:

    python setup.py sdist
