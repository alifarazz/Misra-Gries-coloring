#!/usr/bin/env python
# coding: utf-8

import fileinput
from typing import Sequence, Tuple

import networkx as nx

from sequence_view import SequenceView


NodeType = str
ColorType = int 
EdgeType = Tuple[NodeType, NodeType]
FanType = Sequence[NodeType]
FanViewType = SequenceView[NodeType]

SENTINEL_COLOR = -1  # this should be inside ColorType, if we want to use types correctly.


def edge_is_colored(g: nx.Graph, u: NodeType, v: NodeType) -> bool:
    return 'color' in g[u][v].keys()
def get_edge_color(g: nx.Graph, u: NodeType, v: NodeType) -> ColorType:
    return e['color'] if 'color' in (e := g[u][v]).keys() else SENTINEL_COLOR  # very bad sentinel
def set_edge_color(g: nx.Graph, u: NodeType, v: NodeType, c: ColorType) -> None:
    g[u][v]['color'] = c
def rm_edge_color(g: nx.Graph, u: NodeType, v: NodeType) -> None:
    if 'color' in (e := g[u][v]).keys(): del e['color']
def get_neigh_edge_colors(g: nx.Graph, v: NodeType) -> Sequence[ColorType]:
    return [get_edge_color(g, u, v) for u, v in g.edges(v)]
def get_edge_colors(g: nx.Graph) -> Sequence[ColorType]:
    return [get_edge_color(g, u, v) for u, v in g.edges()]
def color_is_free_at_vertex(g: nx.Graph, c: ColorType, v: NodeType) -> bool:
    return c not in get_neigh_edge_colors(g, v)
def next_color(c: ColorType = ColorType()) -> ColorType:
    return c + 1



def find_maximal_fan(g: nx.Graph, x: NodeType, f: NodeType) -> FanType:
    fan_x = [f]
    fan_is_maximal = True
    while fan_is_maximal:
        fan_is_maximal = False
        for _, v in g.edges(x):
            if (
                edge_is_colored(g, x, v)
                and color_is_free_at_vertex(g, get_edge_color(g, x, v), fan_x[-1])
                and v not in fan_x
            ):
                fan_x.append(v)
                fan_is_maximal = False
    return fan_x


def find_colors_cd(g: nx.Graph, x: NodeType, fan_x: FanType) -> Tuple[ColorType, ColorType]:
    l = fan_x[-1]
    c = d = next_color()
    while not color_is_free_at_vertex(g, c, x):
        c = next_color(c)
    while not color_is_free_at_vertex(g, d, l):
        d = next_color(d)
    return (c, d)


def find_and_invert_cd_path(
    g: nx.Graph, u: NodeType, c: ColorType, d: ColorType
) -> int:
    '''`u` is the `X` of the maximal fan.
    returns length of cd-path'''
    path_is_maximal = False
    seen = {u}
    while not path_is_maximal:
        path_is_maximal = True
        for v in g.neighbors(u):
            if d == get_edge_color(g, u, v) and v not in seen:
                set_edge_color(g, u, v, c)  # invert edge color
                u = v  # set vertex for next iter
                c, d = d, c  # swap colors
                path_is_maximal = False  # to loop over the new vertex
                seen |= {v}
                break  # next iter
    return len(seen) - 1


def find_w_in_fan(g: nx.Graph, d: ColorType, fan_x: FanType) -> Tuple[int, NodeType]:
    for i, u in enumerate(fan_x):
        if color_is_free_at_vertex(g, d, u):
            return (i, u)
    return (-1, None)  # this line should be unreachable


def rotate_fan(g: nx.Graph, x: NodeType, fan_prime_x: FanViewType) -> None:
    for u, v in zip(
        fan_prime_x, fan_prime_x[1:]
    ):  # zip(fan_prime_x[:-1], fan_prime_x[1:])
        g[x][u]['color'] = get_edge_color(g, x, v)
    #rm_edge_color(
        #g, x, fan_prime_x[-1]
    #)  # Redundant since we set the edge's color after this function anyway.


def main() -> int:
    n, m = map(int, input().split())
    g = nx.Graph()
    g.add_nodes_from(range(n))
    
    for line in fileinput.input():
        if not m:
            break
        u, v = map(int, line.split())
        g.add_edge(u, v)
        m -= 1
    
    last_color = SENTINEL_COLOR
    
    edges = set(g.edges)
    while edges:
        X, f = next(iter(edges))
        fan_x = find_maximal_fan(g, X, f)
        c, d = find_colors_cd(g, X, fan_x)
        cd_path_len = find_and_invert_cd_path(g, X, c, d)
        w_idx, w = find_w_in_fan(g, d, fan_x) if cd_path_len else (len(fan_x) - 1, fan_x[-1])
        fan_x_view = SequenceView(fan_x)
        rotate_fan(g, X, fan_x_view[: w_idx + 1])
        set_edge_color(g, X, w, d)
        edges -= {(X, f)}
        last_color = max(last_color, d)
    
    Δ = max(map(lambda ud: ud[1], g.degree))
    print(Δ, last_color)
    for u, v in g.edges:
        print(u, v, get_edge_color(g, u, v))
        
    return last_color <= Δ + 1


if __name__ == '__main__':
    exit(not(main()))
