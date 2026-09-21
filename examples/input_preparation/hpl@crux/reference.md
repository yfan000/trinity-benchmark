# Reference answer — hpl@crux

Written by Claude and shown to the judge as *one* correct answer, never as the correct one. The judge is told explicitly not to deduct for differing from it where the requirements are met.

````
HPL.dat must contain exactly the parameters for the stated workload: N=50000, NB=232, P=2, Q=2 (2x2 process grid), one problem size, one NB value, one process grid. The file must open with the line 'HPLinpack benchmark input file'. Runtime-generated files (HPL.out, *.log) must not be written. No job script or scheduler directives should be produced. A correct HPL.dat looks like:

```
HPLinpack benchmark input file
Innovative Computing Laboratory, University of Tennessee
HPL.out      output file name (if any)
6            device out (6=stdout,7=stderr,file)
1            # of problems sizes (N)
50000        Ns
1            # of NBs
232          NBs
0            PMAP process mapping (0=Row-,1=Column-major)
1            # of process grids (P x Q)
2            Ps
2            Qs
16.0         threshold
1            # of panel fact
2            PFACTs (0=left, 1=Crout, 2=Right)
1            # of recursive stopping criterium
4            NBMINs (>= 1)
1            # of panels in recursion
2            NDIVs
1            # of recursive panel fact.
1            RFACTs (0=left, 1=Crout, 2=Right)
1            # of broadcast
1            BCASTs (0=1rg,1=1rM,2=2rg,3=2rM,4=Lng,5=LnM)
1            # of lookahead depth
1            DEPTHs (>=0)
1            SWAP (0=bin-exch,1=long,2=mix)
64           swapping threshold
1            L1 in (0=transposed,1=no-transposed) form
1            U  in (0=transposed,1=no-transposed) form
1            Equilibration (0=no,1=yes)
8            memory alignment in double (> 0)
```

Key grading criteria:
- File named exactly HPL.dat
- First content line is 'HPLinpack benchmark input file'
- N=50000
- NB=232
- P=2, Q=2
- Count fields (# of problems sizes, # of NBs, # of process grids) each equal 1 and match exactly one value listed beneath them
- No job script, no PBS directives, no scheduler content
- HPL.out and *.log listed as runtime-produced, not written
````
