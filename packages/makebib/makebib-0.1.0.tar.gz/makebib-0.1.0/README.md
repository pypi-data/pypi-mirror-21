# Makebib

A simple script to generate a local bib file from a central
database so that only items actually cited appear.

## Usage

```bash
$ makebib arg
```

where `arg` is either

- the basename of a TeX-file, in which case
  the script creates a bib file and populates it with items
  which are cited by the document and can be found in the
  central database. Then it runs (a python version) of bibtex
  on the texfile.

or

- `--list` which is followed by one of `cited`, `missing`, `all`, `cfg`
   and (in the first three cases) a TeX-file in which case the program prints
   out a list of
 
   - `cited`    citekeys which are cited in the TeX-file

   - `missing`  citekeys which are cited in the TeX-file but not present
                in the central database

   - `all`      all citekeys in the central database

   - `cfg`      configuration

or

- `--help` which prints out a short help message

## Configuration

The program reads its configuration from the files `/etc/makebib`,
`~/.makebib` or `.makebib` in the current directory. If either of
the files does not exist, it is skipped. Also, options specified
in later files override options specified in the previous files
(and defaults). The files follow a simple

```
    key = val
```

format with each line specifying a single case-insensitive option.
Spaces around `=` are ignored as is everything following a `#` sign.
Currently the only available option is `db` which specifies the
location of the central BibTeX database.
