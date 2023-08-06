Agalma Tutorial
===============

This tutorial has two sections. The first describes an assembly run of the
Agalma transcriptome pipeline using a sample read data set. The second
describes a run of the phylogeny pipeline on a set of sample transcriptomes.

You can create a shell script that has just the commands you need to execute
from this document with the command:
`grep '^    ' TUTORIAL.md | sed -e 's/^    //' > tutorial.sh`.

Let's start by creating an organized directory hierarchy in your home directory
for storing Agalma data:

    mkdir -p agalma/data
    mkdir -p agalma/scratch
    mkdir -p agalma/reports

We'll also specify a path for a local Agalma database to store the catalog of data,
the diagnostics from our runs, and the sequences and homology calculated by Agalma:

    export AGALMA_DB=$PWD/agalma/data/agalma.sqlite

Agalma distinguishes between two types of storage locations:

1. a permanent location for raw data ("data") and the Agalma database file
   ("data/agalma.sqlite")
2. a temporary location for the intermediate files from analyses ("scratch")
   and reports ("reports")

In a production system, you would want to make sure that "data" is backed up,
but "scratch" and "reports" don't need to be backed up because their files are
typically only used over the course of a single analysis and can be
regenerated.

The 'testdata' command will unpack all of the sample data sets used in the
tutorials:

* 4 subsets of paired-end Illumina HiSeq reads from the siphonophore species:
  *Agalma elegans*, *Craseoa lathetica*, *Physalia physalis*, *Nanomia bijuga*
* 2 subsets of single-end Illumina GAIIx reads from two different specimens of
  the species *Nanomia bijuga*
* a public set of aa gene predictions for the species *Nematostella vectensis*

Let's run this command to download the sample data to the "data" directory:

    cd agalma/data
    agalma testdata

You should now see the test data files in the `data` directory.


Transcriptome
-------------

Now we'll create a catalog entry in the BioLite database for the *Agalma
elegans* data set:

    agalma catalog insert --paths SRX288285_1.fq SRX288285_2.fq --species "Agalma elegans" --ncbi_id 316166 --itis_id 51383

Note in the above commands that we are specifying both the the 
[ITIS ID](http://www.itis.gov), 
which is 51383, and [NCBI ID](http://www.ncbi.nlm.nih.gov/taxonomy), which is 
316166, for this species. Specifying both ID's is highly recommended.

The catalog command automatically recognizes the Illumina CASAVA 1.8 header in
the data and assigns a catalog ID `HWI-ST625-73-C0JUVACXX-7`.

Before running a pipeline, you may want to adjust the number of threads and memory
to match your computer. System performance may lag if you allocate the 
full available memory to agalma. You should leave at least 2 GB unallocated. If,
for example, you have an 8-core machine with 24 GB of free memory, you could 
allocate all the processors and 20 GB of the memory by calling agalma with the
additional options -t and -m like this:

    agalma -t 8 -m 20G

By default, agalma will try to use all available cores on your system, and 90% of
the total physical memory.

Now run the QC and full transcriptome pipelines on the test data from the
scratch directory with:

    cd ../scratch
    agalma qc --id HWI-ST625-73-C0JUVACXX-7
    agalma transcriptome --id HWI-ST625-73-C0JUVACXX-7

To generate reports for the transcriptome run, use:

    agalma report --id HWI-ST625-73-C0JUVACXX-7 --outdir ../reports/HWI-ST625-73-C0JUVACXX-7
    agalma resources --id HWI-ST625-73-C0JUVACXX-7 --outdir ../reports/HWI-ST625-73-C0JUVACXX-7

You will now have a report with diagnostics for all of the transcriptome stages
run above located at:

* `agalma/reports/HWI-ST625-73-C0JUVACXX-7/index.html`

Another report with detailed resource utilization will be located at:

* `agalma/reports/HWI-ST625-73-C0JUVACXX-7/profile.html`


Phylogeny
---------

This analysis builds a species tree for 6 taxa using a small data subset,
and requires roughly 7 GB of RAM and 10 minutes of runtime on an
8-core Intel Xeon E5540 node.

First, we'll catalog our data:

    cd ../data
    agalma catalog insert --id SRX288285 --paths SRX288285_1.fq SRX288285_2.fq --species "Agalma elegans" --ncbi_id 316166
    agalma catalog insert --id SRX288432 --paths SRX288432_1.fq SRX288432_2.fq --species "Craseoa lathetica" --ncbi_id 316205
    agalma catalog insert --id SRX288431 --paths SRX288431_1.fq SRX288431_2.fq --species "Physalia physalis" --ncbi_id 168775
    agalma catalog insert --id SRX288430 --paths SRX288430_1.fq SRX288430_2.fq --species "Nanomia bijuga" --ncbi_id 168759
    agalma catalog insert --id JGI_NEMVEC --paths JGI_NEMVEC.fa --species "Nematostella vectensis" --ncbi_id 45351
    agalma catalog insert --id NCBI_HYDMAG --paths NCBI_HYDMAG.pfa --species "Hydra magnipapillata" --ncbi_id 6085

Each of the RNA-seq datasets needs to be assembled and translated:

    cd ../scratch
    agalma transcriptome --id SRX288285
    agalma transcriptome --id SRX288430
    agalma transcriptome --id SRX288431
    agalma transcriptome --id SRX288432

And the gene predictions for JGI_NEMVEC and NCBI_HYDMAG have to be imported and
anotated:

    agalma import --id JGI_NEMVEC
    agalma translate --id JGI_NEMVEC
    agalma annotate --id JGI_NEMVEC

    agalma import --id NCBI_HYDMAG --seq_type aa
    agalma annotate --id NCBI_HYDMAG

Note that NCBI_HYDMAG does not need to be translated, but we do have to specify
that it contains aa sequences with the `--seq_type aa` flag to `import`.

Now that you have loaded all of the data sets, call the `homologize` pipeline,
which will perform an all-by-all comparison of exemplar sequences for every
gene loaded by a previous `assemble` or `import` call. (If you have a project
where you would like to exclude some of the previous runs, you have to hide
those runs using `agalma diagnostics hide RUN_ID`.)

    agalma homologize --id PhylogenyTest

The option `--id PhylogenyTest` specifies the analysis ID, and will be used to
pass results through several commands below. This ID should be unique for each
phylogenetic analysis.

The `homologize` pipeline will write a collection of gene clusters back into
the Agalma database.

Now call this sequence of pipelines, inserting the analysis ID each time, to
build gene trees for each of the clusters, and finally to assemble a
supermatrix with a single concatenated sequence of genes for each taxon.

    agalma multalign --id PhylogenyTest
    agalma genetree --id PhylogenyTest
    agalma treeinform --id PhylogenyTest
    agalma homologize --id PhylogenyTest
    agalma multalign --id PhylogenyTest
    agalma genetree --id PhylogenyTest
    agalma treeprune --id PhylogenyTest
    agalma multalign --id PhylogenyTest
    agalma supermatrix --id PhylogenyTest
    agalma speciestree --id PhylogenyTest --outgroup Nematostella_vectensis

The first calls to `multalign` and `genetree` align and build gene trees based on the 
assemblies. `treeinform` then uses the gene trees to identify highly similar sets of 
sequences from the same species that are likely splice variants that were incorrectly 
assigned to different genes. After identifying these, `treeinform` updates the assemblies
to assign these splice variants to the same genes. This process essentially uses 
phylogenetic analyses across species to refine the assemblies within each species. The next 
calls to `homologize`, `multalign`, and `genetree` then regenerate update species trees 
based on the refined assemblies. `treeprune` identifies subtrees in the unrooted gene trees 
that have no more than one sequence per taxon, which are then treated as putative orthologs.
These subsets of sequences are then realigned with `multalign`, concatenated with 
`supermatrix`, and used to infer a preliminary species tree with `speciestree`.

Note that even though we are using the same commands multiple times in the analysis, 
each time Agalma is smart enough to use the output from the last command for the same 
`--id` as input. That saves a lot of book keeping for the user, and makes scripts more
portable.

To generate reports for the phylogeny run, use:

    agalma report --id PhylogenyTest --outdir ../reports/PhylogenyTest
    agalma resources --id PhylogenyTest --outdir ../reports/PhylogenyTest
    agalma phylogeny_report --id PhylogenyTest --outdir ../reports/PhylogenyTest

You will now have a report with diagnostics for all of the phylogeny stages run
above, including the supermatrix and the final tree, located at:

* `agalma/reports/PhylogenyTest/index.html`

Another report with detailed resource utilization will be located at:

* `agalma/reports/PhylogenyTest/profile.html`

A line graph showing the reduction in the number of genes at each stage will
be located at:

* `agalma/reports/PhylogenyTest/PhylogenyTest.pdf`

You can view a list of all the runs from this tutorial with the 'diagnostics'
command:

    agalma diagnostics list


Expression
----------

Agalma's expression pipeline maps reads against an assembly and estimates the
read count for each transcript in the assembly (at the gene and isoform level).
Multiple read files can be mapped against each assembly, accommodating multiple
treatments and replicates for each species. The read counts are exported as a
JSON file, that (following parsing) can then be analyzed using tools such as
[edgeR](http://www.bioconductor.org/packages/release/bioc/html/edgeR.html).  If
the assembly has also been included in a phylogenetic analysis, then gene trees
and a species tree can be exported along with the count data. This allows for
phylogenetic analysis of gene expression. For background information on this
type of analysis, read [Dunn et al.,
2013](http://icb.oxfordjournals.org/content/53/5/847).

This tutorial presents a minimal example of an expression analysis. An assembly
is imported, reads are mapped to the assembly, and count data (without gene
phylogenies) are exported.

We'll start by cataloging two single-end Illumina data sets for two different
individuals (specimen-1 and specimen-2), but in the same treatment (in this
case, the same tissue type: gastrozooids):

    cd ../data
    agalma catalog insert --id SRX033366 --paths SRX033366.fq --species "Nanomia bijuga" --ncbi_id 168759 --itis_id 51389 --treatment gastrozooids --individual specimen-1
    agalma catalog insert --id SRX036876 --paths SRX036876.fq --species "Nanomia bijuga" --ncbi_id 168759 --itis_id 51389 --treatment gastrozooids --individual specimen-2

Estimate their expression counts by running the `expression` pipeline for each
against the SRX288430 assembly for Nanomia (from the "Transcriptome" section
above):

    cd ../scratch
    agalma qc --id SRX033366
    agalma qc --id SRX036876
    agalma expression --id SRX033366 SRX288430
    agalma expression --id SRX036876 SRX288430

Individual reports can be generated for both of the `expression` runs:

    agalma report --id SRX033366 --outdir ../reports/SRX033366
    agalma report --id SRX036876 --outdir ../reports/SRX036876

Finally, bundle the expression count estimates into a
JSON file that can be imported into R for further analysis:

    IDS=$(agalma diagnostics runid -n transcriptome -i SRX288430)
    agalma export_expression --id PhylogenyTest --sequences $IDS >../reports/export.json

In this short example, the JSON file only includes the expression levels. If it
were run on assemblies following a full phylogenomic analysis, it would also
include the species tree and gene trees (with bootstrap values).

This JSON can be imported into R with the pckage
[agalmar](https://github.com/caseywdunn/agalmar) for further analysis.

