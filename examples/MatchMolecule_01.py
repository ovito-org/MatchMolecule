from ovito.io import import_file

from MatchMolecule import MatchMolecule


def main():
    # Data import:
    pipeline = import_file(
        "https://gitlab.com/ovito-org/ovito-sample-data/-/raw/master/LAMMPS/tiny_nylon.data?ref_type=heads",
        atom_style="full",
    )

    # Match Molecule:
    pipeline.modifiers.append(MatchMolecule(query="OCO"))

    # Compute result:
    data = pipeline.compute()

    print(f"{data.attributes['MatchMolecule.Particles.Selection.Count'] = }")
    print(f"{data.attributes['MatchMolecule.Bonds.Selection.Count'] = }")


if __name__ == "__main__":
    main()
