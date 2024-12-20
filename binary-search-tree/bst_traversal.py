from manim import *
from get_bst import get_bst
from typing import Tuple, Dict, List, Optional
from bst import BST
def animate_tree_traversal(
    scene: Scene,
    bst: BST,
    key: int,
    old_scale: float,
    old_arrows: dict,
    old_circles: dict,
    trace_color: str = YELLOW,
    left: float = -7,
    width: float = 14,
    top: float = 4,
    height: float = 8
) -> Tuple[dict, dict, Group, List[int]]:
    key_node, path = bst.search(key)

    tracing_circle = Group(
        Circle(
            radius=old_scale*0.375, 
            color=YELLOW, 
            stroke_width=old_scale*3
        ).set_fill(BLACK, opacity=1),
        Text(str(key), font_size=old_scale*25),
        Text(str(key_node.balance), font_size=old_scale*20, fill_opacity=0).move_to(DOWN*old_scale*0.375)
    ).next_to(old_circles[path[0]], UP, buff=10)

    scene.add(*old_arrows.values(), *old_circles.values())
    scene.add(tracing_circle)
    
    for node in path:
        scene.play(tracing_circle.animate.next_to(old_circles[node], UP))
        scene.wait()

    return tracing_circle, key_node