import numpy as np
import pytest
from ovito.io import import_file

from MatchMolecule import MatchMolecule


@pytest.fixture
def nylon_pipeline():
    return import_file("tiny_nylon.data", atom_style="full")


@pytest.fixture
def gw_pipeline():
    return import_file("1G9W.pdb")


def test_example_01(nylon_pipeline):
    nylon_pipeline.modifiers.append(MatchMolecule(query="OCO"))
    data = nylon_pipeline.compute()

    assert (
        np.count_nonzero(data.particles.selection)
        == data.attributes["MatchMolecule.Particles.Selection.Count"]
    )
    assert data.attributes["MatchMolecule.Particles.Selection.Count"] == 6

    assert (
        np.count_nonzero(data.particles.bonds.selection)
        == data.attributes["MatchMolecule.Bonds.Selection.Count"]
    )
    assert data.attributes["MatchMolecule.Bonds.Selection.Count"] == 4


def test_example_01_wildcard(nylon_pipeline):
    nylon_pipeline.modifiers.append(MatchMolecule(query="O?O"))
    data = nylon_pipeline.compute()

    assert (
        np.count_nonzero(data.particles.selection)
        == data.attributes["MatchMolecule.Particles.Selection.Count"]
    )
    assert data.attributes["MatchMolecule.Particles.Selection.Count"] == 6

    assert (
        np.count_nonzero(data.particles.bonds.selection)
        == data.attributes["MatchMolecule.Bonds.Selection.Count"]
    )
    assert data.attributes["MatchMolecule.Bonds.Selection.Count"] == 4


def test_example_01_only_bonds(nylon_pipeline):
    nylon_pipeline.modifiers.append(MatchMolecule(query="OCO", selectParticles=False))
    data = nylon_pipeline.compute()

    assert (
        np.count_nonzero(data.particles.selection)
        == data.attributes["MatchMolecule.Particles.Selection.Count"]
    )
    assert data.attributes["MatchMolecule.Particles.Selection.Count"] == 6

    assert "MatchMolecule.Bonds.Selection.Count" not in data.attributes


def test_example_01_only_particles(nylon_pipeline):
    nylon_pipeline.modifiers.append(MatchMolecule(query="OCO", selectBonds=False))
    data = nylon_pipeline.compute()

    assert "MatchMolecule.Particles.Selection.Count" not in data.attributes

    assert (
        np.count_nonzero(data.particles.bonds.selection)
        == data.attributes["MatchMolecule.Bonds.Selection.Count"]
    )
    assert data.attributes["MatchMolecule.Bonds.Selection.Count"] == 4


def test_example_02_01(gw_pipeline):
    gw_pipeline.modifiers.append(MatchMolecule(query="N1CCCC1"))
    data = gw_pipeline.compute()

    assert (
        np.count_nonzero(data.particles.selection)
        == data.attributes["MatchMolecule.Particles.Selection.Count"]
    )
    assert data.attributes["MatchMolecule.Particles.Selection.Count"] == 70

    assert (
        np.count_nonzero(data.particles.bonds.selection)
        == data.attributes["MatchMolecule.Bonds.Selection.Count"]
    )
    assert data.attributes["MatchMolecule.Bonds.Selection.Count"] == 70


def test_example_02_02(gw_pipeline):
    gw_pipeline.modifiers.append(MatchMolecule(query="CN(C)C"))
    data = gw_pipeline.compute()

    assert (
        np.count_nonzero(data.particles.selection)
        == data.attributes["MatchMolecule.Particles.Selection.Count"]
    )
    assert data.attributes["MatchMolecule.Particles.Selection.Count"] == 56

    assert (
        np.count_nonzero(data.particles.bonds.selection)
        == data.attributes["MatchMolecule.Bonds.Selection.Count"]
    )
    assert data.attributes["MatchMolecule.Bonds.Selection.Count"] == 42
