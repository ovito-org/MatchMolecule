# Match Molecule
Match parts of molecules using query strings.

## Description / Examples
This modifier allows you to select sections of molecules using query strings. The query strings use a simplied form of [SMILES](https://en.wikipedia.org/wiki/Simplified_Molecular_Input_Line_Entry_System):

![Smile explanation image](https://upload.wikimedia.org/wikipedia/commons/0/00/SMILES.png)
> Original by Fdardel, slight edit by DMacks, CC BY-SA 3.0 <http://creativecommons.org/licenses/by-sa/3.0/>, via Wikimedia Commons

where molecules can be defined by strings.

### Selecting linear molecules
In the simplest form `HOH` can be used to define the water (`H-O-H`) molecule. 

### Adding side chains
To define more complex molecules one can use `()`. To select this submolecule,
``` 
  O
   \
     N - C - C -
   /
H-O
```
one might use this query string `ON(OH)CC`. Here `(OH)` denotes a side chain which branches off from the preceeding `N` atom. 

### Selecting multi-letter elements
To select this group of atoms,
```
- C - Fe -
  |   |
  H   O
      |
      H
```
you could write the following query `C(H)"Fe"(OH)`. Note, that multi-letter chemical elements need to be enclosed by `""`. An equivalent formulation would be `C(H)"Fe"OH`.

### Adding wildcards / placeholders
If you want to match multiple sub-molecules you can use the `?` wildcard character. `H?H` would match both, the `H-O-H` and the `H-N-H` molecules (and any other molecule where 2 H atoms are connected by a singular bridge atom).

### Creating additional bonds
This syntax can be limiting so you might need to manually add  bonds to your string. If you want to select this group atoms:
```
- C - N 
    /   \*
   C      C - C -
   \     /
    C - C
```
Here you could write `CNCCCCC`. This would select all atoms, however, you would be missing the bond tagged by the `*` in the picture. In such cases you can use numbers to tag atoms. Atoms with the same nummerical tag will be connected by bonds. This query string `CN1CCCC1C` would correctly select all atoms and bonds shown in the image. Here these two atoms (tagged 1) would be connected to form the `*` highlghted bond.
```
- C - N1
    /   \*
   C      C1 - C -
   \     /
    C - C
```

## Parameters 
- `query` / "Query": Query string used to select the atoms and bonds.
- `selectParticles` / "Select particles": Create a selection for the particles selected by the query string. 
- `selectBonds` / "Select bonds": Create a selection for the bonds defined by the query string. 

## Installation
- OVITO Pro [integrated Python interpreter](https://docs.ovito.org/python/introduction/installation.html#ovito-pro-integrated-interpreter):
  ```
  ovitos -m pip install --user git+https://github.com/ovito-org/MatchMolecule.git
  ``` 
  The `--user` option is recommended and [installs the package in the user's site directory](https://pip.pypa.io/en/stable/user_guide/#user-installs).

- Other Python interpreters or Conda environments:
  ```
  pip install git+https://github.com/ovito-org/MatchMolecule.git
  ```

## Technical information / dependencies
- Tested on OVITO version 3.10.6

## Contact
- Daniel Utt (utt@ovito.org)
