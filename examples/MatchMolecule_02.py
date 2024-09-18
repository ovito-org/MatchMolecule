from ovito.io import import_file

from MatchMolecule import MatchMolecule


def main():
    # Data import:
    pipeline = import_file("https://files.rcsb.org/download/1G9W.pdb")

    # Match Molecule:
    pipeline.modifiers.append(MatchMolecule(query="N1CCCC1"))

    # Compute result:
    data = pipeline.compute()

    print(f"{data.attributes['MatchMolecule.Particles.Selection.Count'] = }")
    print(f"{data.attributes['MatchMolecule.Bonds.Selection.Count'] = }")


if __name__ == "__main__":
    main()
