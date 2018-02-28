# authorlist

Simplify the task of maintaining a long author list and corresponding affiliations.

## Input Files

All you need is two tab-delimited files containing the authors and affiliations.

**authors.tsv**

The first column contains the author names.
The author order in this file will determine the author order in the output.
The affiliation IDs listed in the second column have to match an ID in the affiliations file.
Multiple affiliations for an author can be indicated using a comma-delimited list (no spaces), as shown below.
Because of this, the only restriction on the affiliation IDs is that they cannot contain commas. 
You don't even need to use numbers; you could simply use acronyms that are easier to remember as the affiliation IDs.

```
Bruno M. Grande	mbb
Nicole Knoetze	mbb
Ryan D. Morin	gsc,mbb
```

**affiliations.tsv**

The first column contains an ID for each affiliation.
The second column contains the full affiliation name.
The order of the affiliations in this file doesn't matter.
Any affiliations that appear in this file but are not referenced in the authors file will be excluded from the output.

```
gsc	Canada's Michael Smith Genome Sciences Centre, British Columbia Cancer Agency, Vancouver, BC, Canada 
mbb	Department of Molecular Biology and Biochemistry, Simon Fraser University, Burnaby, BC, Canada 
```

## Example Usage

Generating the output is as simple as running the following command:

```
$ python authorlist.py -f markdown_github authors.tsv affiliations.tsv
Bruno M. Grande<sup>1</sup>, Nicole Knoetze<sup>1</sup>, Ryan D. Morin<sup>2,1</sup>

<sup>1</sup>Department of Molecular Biology and Biochemistry, Simon Fraser University, Burnaby, BC, Canada.
<sup>2</sup>Canada's Michael Smith Genome Sciences Centre, British Columbia Cancer Agency, Vancouver, BC, Canada.
```

The default format is pandoc-flavoured Markdown, which can be used in various places such as R Markdown documents.
Github-flavoured Markdown is also supported, as displayed below. 
Other formats can be easily implemented. 

## Example Output

Bruno M. Grande<sup>1</sup>, Nicole Knoetze<sup>1</sup>, Ryan D. Morin<sup>1,2</sup>

<sup>1</sup>Department of Molecular Biology and Biochemistry, Simon Fraser University, Burnaby, BC, Canada.
<sup>2</sup>Canada's Michael Smith Genome Sciences Centre, British Columbia Cancer Agency, Vancouver, BC, Canada.
