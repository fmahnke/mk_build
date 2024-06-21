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

### 
