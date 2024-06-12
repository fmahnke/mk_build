# Generate target names.

```
gup(path(top_build_dir(), 'arch/i386/all'))

objects = suffix(sources, '.o')
```

# Generate dependencies from gup data

```
objects = deps(path(top_build_dir(), 'arch/i386/all')).files_list('.o')
```

## TODO

### make process.run capture stderr

always capture this so tools are more silent. print it out if the process exits
with a failure code. see how the gup function already does this.
