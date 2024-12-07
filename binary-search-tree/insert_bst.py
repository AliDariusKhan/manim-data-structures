from manim import *
from bst import BST
from get_bst import get_bst
from copy import deepcopy

def insert_bst(scene: Scene, bst: BST, key: int, left=-7, width=14, top=4, height=8):
    """Inserts the given key to the BST and animates the process"""
    if bst.root is None:
        bst.insert([key])
        circle = get_bst(bst, left, width, top, height, True)[1].popitem()[1]
        circle[0].set_stroke(color=YELLOW)
        circle[2].set_opacity(0)
        circle.shift(UP*10)
        scene.add(circle)
        scene.play(
            circle.animate.shift(DOWN*10)
        )
        scene.play(
            circle[0].animate.set_stroke(color=BLUE),
            circle[2].animate.set_opacity(1)
        )
        return [circle]
        
    old_arrows, old_circles, old_scale = get_bst(bst, left, width, top, height, True)

    bst.insert([key])
    new_arrows, new_circles, new_scale = get_bst(bst, left, width, top, height, True)

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
    
    scene.play(
        *[Transform(old_circles[node], new_circles[node]) for node in old_circles.keys()],
        *[Transform(old_arrows[node], new_arrows[node]) for node in old_arrows.keys()],
        Transform(tracing_circle, new_circles[key_node]),
    )
    
    scene.play(FadeIn(new_arrows[key_node]))
    scene.wait()

    to_remove = [
        *old_arrows.values(), 
        *old_circles.values(), 
        tracing_circle, 
        new_circles[key_node], 
        new_arrows[key_node]
    ]

    return to_remove
