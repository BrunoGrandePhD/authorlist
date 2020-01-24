#!/usr/bin/env python3

from argparse import ArgumentParser, FileType
from collections import OrderedDict


def main():
    args = parse_args()
    authors, metadata = parse_authors(args.authors)
    affiliations = parse_affiliations(args.affiliations)
    authors, affiliations = update_affiliations(authors, affiliations)
    output(authors, affiliations, metadata, args.output, args.format)


def parse_args():
    """Parse and validate command-line arguments"""
    # Retrieve possible output formats
    supported = [f[7:] for f in globals().keys() if f.startswith("output_")]
    # Configure parser
    parser = ArgumentParser()
    parser.add_argument("authors", type = FileType("r"))
    parser.add_argument("affiliations", type = FileType("r"))
    parser.add_argument("--output", "-t", type = FileType("w"), default = "-")
    parser.add_argument("--format", "-f", choices=supported,
                        default="markdown_pandoc")
    args = parser.parse_args()
    return args


def parse_authors(file):
    """Parse authors TSV file"""
    authors = OrderedDict()
    metadata = OrderedDict()
    for line in file:
        line_split = line.rstrip().split("\t")
        author, affiliations = line_split[0:2]
        mdata = line_split[2:]
        affiliations = affiliations.split(",")
        authors[author] = affiliations
        metadata[author] = mdata
    return authors, metadata


def parse_affiliations(file):
    """Parse author affiliations TSV file"""
    affiliations = OrderedDict()
    for line in file:
        uid, name = line.rstrip().rstrip(".").split("\t")
        affiliations[uid] = name
    return affiliations


def update_affiliations(authors, affiliations):
    """Arrange affiliations according to the author order"""
    counter = 1
    new_affiliations = OrderedDict()
    for author, affiliation_ids in authors.items():
        new_ids = []
        for affiliation_id in affiliation_ids:
            name = affiliations[affiliation_id]
            if name not in new_affiliations:
                new_id = str(counter)
                counter += 1
                new_affiliations[name] = new_id
            else:
                new_id = new_affiliations[name]
            new_ids.append(new_id)
        authors[author] = new_ids
    return authors, new_affiliations


def output(authors, affiliations, metadata, file, format):
    """Output author list and affiliations in specified format"""
    output_fn = globals()["output_" + format]
    output_fn(authors, affiliations, metadata, file)


def _output_general(authors, affiliations, file, lsup, rsup, affdel=";\n"):
    """Output author list and affiliations in Markdown format"""
    result = []
    for i, author_item in enumerate(authors.items()):
        author, affiliation_ids = author_item
        if i > 0:
            result.append(", ")
        result.append(author)
        result.append(lsup)
        for i, affiliation_id in enumerate(affiliation_ids):
            if i > 0:
                result.append(",")
            result.append(affiliation_id)
        result.append(rsup)
    result.append("\n\n")
    for i, affiliation_item in enumerate(affiliations.items()):
        affiliation, affiliation_id = affiliation_item
        result.append(lsup)
        result.append(affiliation_id)
        result.append(rsup)
        result.append(affiliation)
        result.append(affdel)
    result.append("\n")
    text = "".join(result)
    file.write(text)


def output_markdown_pandoc(authors, affiliations, metadata, file):
    """Output author list and affiliations in Markdown format"""
    _output_general(authors, affiliations, file, lsup="^", rsup="^")


def output_markdown_github(authors, affiliations, metadata, file):
    """Output author list and affiliations in Markdown format"""
    _output_general(authors, affiliations, file, lsup="<sup>", rsup="</sup>")


def output_tsv(authors, affiliations, metadata, file, list_sep="; "):
    """Output author list and affiliations in TSV format"""
    result = []
    affiliations = {v: k for k, v in affiliations.items()}
    for author_item in authors.items():
        author, affiliation_ids = author_item
        result.append(author)
        for i, affiliation_id in enumerate(affiliation_ids):
            if i == 0:
                result.append("\t")
            else:
                result.append(list_sep)
            result.append(affiliations[affiliation_id])
        for field in metadata[author]:
            result.append("\t")
            result.append(field)
        result.append("\n")
    text = "".join(result)
    file.write(text)


if __name__ == '__main__':
    main()
