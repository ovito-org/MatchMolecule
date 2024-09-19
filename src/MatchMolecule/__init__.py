#### Match Molecule ####
# Match parts of molecules using SMILES like query strings.

import networkx as nx
import numpy as np
from ovito.data import DataCollection
from ovito.pipeline import ModifierInterface
from traits.api import Bool, Str


class MatchMolecule(ModifierInterface):
    query = Str("", label="Query", ovito_invalidate_cache=False)
    selectParticles = Bool(True, label="Select particles", ovito_invalidate_cache=False)
    selectBonds = Bool(True, label="Select bonds", ovito_invalidate_cache=False)

    def tokenizer(self):
        tokens = []
        offset = 0
        for i in range(0, len(self.query)):
            idx = offset + i
            if idx >= len(self.query):
                break
            elif self.query[idx] == '"' or self.query[idx] == "'":
                j = 1
                while (
                    idx + j < len(self.query)
                    and self.query[idx + j] != '"'
                    and self.query[idx + j] != "'"
                ):
                    j += 1
                offset += j
                tokens.append(self.query[idx + 1 : idx + j])
            elif idx + 1 < len(self.query) and self.query[idx + 1].islower():
                j = 1
                while idx + j < len(self.query) and self.query[idx + j].islower():
                    j += 1
                offset += j - 1
                tokens.append(self.query[idx : idx + j])
            else:
                tokens.append(self.query[idx])
        return tokens

    def parseBranch(self, tokens, G, con, start=0, connect=-1):
        str_offset = 0
        for i in range(start, len(tokens)):
            idx = i + str_offset
            if idx >= len(tokens):
                return
            elif tokens[idx].isdigit():
                if tokens[idx] in con:
                    G.add_edge(connect, con[tokens[idx]])
                else:
                    con[tokens[idx]] = connect
            elif tokens[idx] == "(":
                str_offset += self.parseBranch(
                    tokens, G, con, start=idx + 1, connect=connect
                )
            elif tokens[idx] == ")":
                return i - start + 1 + str_offset
            else:
                G.add_node(len(G.nodes), tag=tokens[idx])
                if connect != -1:
                    G.add_edge(connect, len(G.nodes) - 1)
                connect = len(G.nodes) - 1

    def read_query(self, data_cache, frame):
        cache_key = f"query_{frame}"
        self.query.strip()
        if not (
            cache_key in data_cache.attributes
            and data_cache.attributes[cache_key] == self.query
        ):
            data_cache.attributes[f"matches_{frame}"] = None
            connections = {}
            G = nx.Graph()
            self.parseBranch(self.tokenizer(), G, connections)
            data_cache.attributes[cache_key] = self.query
            data_cache.attributes[cache_key + "_graph"] = G
            data_cache.attributes["matches"] = None
        return data_cache.attributes[cache_key + "_graph"]

    @staticmethod
    def parseStructure(data, data_cache, frame):
        cache_key = f"molecule_graph_{frame}"
        if cache_key not in data_cache.attributes:
            G = nx.Graph()
            pTypes = data.particles["Particle Type"]
            for i, (a, b) in enumerate(data.particles.bonds.topology):
                name_a = data.particles.particle_types.type_by_id(pTypes[a]).name
                name_b = data.particles.particle_types.type_by_id(pTypes[b]).name
                G.add_node(a, tag=name_a)
                G.add_node(b, tag=name_b)
                G.add_edge(a, b, idx=i)
                yield i / data.particles.bonds.count
            data_cache.attributes[cache_key] = G
        return data_cache.attributes[cache_key]

    @staticmethod
    def node_matcher(n1, n2):
        if n1["tag"] == "?" or n2["tag"] == "?":
            return True
        return n1["tag"] == n2["tag"]

    @staticmethod
    def getMatches(moleculeG, queryG, data_cache, frame):
        cache_key = f"matches_{frame}"
        if (
            cache_key not in data_cache.attributes
            or data_cache.attributes[cache_key] is None
        ):
            matcher = nx.algorithms.isomorphism.GraphMatcher(
                moleculeG, queryG, node_match=__class__.node_matcher
            )
            data_cache.attributes[cache_key] = set()
            for match in matcher.subgraph_monomorphisms_iter():
                data_cache.attributes[cache_key].add(frozenset(match.keys()))
        return data_cache.attributes[cache_key]

    def modify(
        self, data: DataCollection, frame: int, data_cache: DataCollection, **kwargs
    ):
        if not self.query:
            return
        moleculeG = yield from self.parseStructure(data, data_cache, frame)
        queryG = self.read_query(data_cache, frame)

        if self.selectParticles:
            selection = data.particles_.create_property("Selection")
        if self.selectBonds:
            bond_selection = data.particles_.bonds_.create_property("Selection")
            bond_selection[:] = 0
            topo = data.particles.bonds.topology

        for match in self.getMatches(moleculeG, queryG, data_cache, frame):
            match = list(match)
            if self.selectParticles:
                selection[match] = 1

            if self.selectBonds:
                bond_selection[...] = np.logical_or(
                    bond_selection,
                    np.logical_and(
                        np.isin(topo[:, 0], match), np.isin(topo[:, 1], match)
                    ),
                )

        data.attributes["MatchMolecule.Particles.Selection.Count"] = np.count_nonzero(
            selection
        )
        data.attributes["MatchMolecule.Bonds.Selection.Count"] = np.count_nonzero(
            bond_selection
        )
