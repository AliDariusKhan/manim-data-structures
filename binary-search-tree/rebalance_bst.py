from manim import *
from get_bst import get_bst
from copy import deepcopy

def rebalance_bst(scene: Scene, subtree, bst):
    if not subtree:
        return
    rebalance_bst(scene, subtree.left, bst)
    rebalance_bst(scene, subtree.right, bst)
    if subtree.balance == 2:
        if subtree.right.balance == -1:
            right_rotate(scene, subtree.right, bst)
        left_rotate(scene, subtree, bst)
    if subtree.balance == -2:
        if subtree.left.balance == 1:
            left_rotate(scene, subtree.left, bst)
        right_rotate(scene, subtree, bst)

def left_rotate(scene, old_root, bst=None):
    old_arrows, old_circles, _ = get_bst(bst)
    new_root = old_root.right
    old_root.right = new_root.left
    if old_root.right:
        old_root.right.parent = old_root
    new_root.left = old_root
    if old_root.parent:
        parent_to_root = 'left' if old_root.parent.left == old_root else 'right'
        setattr(old_root.parent, parent_to_root, new_root)
    else:
        bst.root = new_root
    new_root.parent = old_root.parent
    old_root.parent = new_root
    bst.update_balances()
    new_arrows, new_circles, _ = get_bst(bst)
    transforms = [Transform(old_circles[node], new_circles[node]) for node in old_circles.keys() if node in new_circles]
    transforms.extend([Transform(old_arrows[node], new_arrows[node]) for node in old_arrows.keys() if node in new_arrows and node != old_root])
    transforms.append(Transform(old_arrows[new_root].reverse_points(), new_arrows[old_root]))
    if old_root in old_arrows:
        transforms.append(Transform(old_arrows[old_root], new_arrows[new_root]))
    scene.play(*transforms)
    scene.remove(*old_arrows.values(), *old_circles.values())
    return new_root

def right_rotate(scene, old_root, bst=None):
    old_arrows, old_circles, _ = get_bst(bst)
    new_root = old_root.left
    old_root.left = new_root.right
    if old_root.left:
        old_root.left.parent = old_root
    new_root.right = old_root
    parent_to_root = None
    if old_root.parent:
        parent_to_root = 'left' if old_root.parent.left == old_root else 'right'
        setattr(old_root.parent, parent_to_root, new_root)
    else:
        bst.root = new_root
    new_root.parent = old_root.parent
    old_root.parent = new_root
    bst.update_balances()
    new_arrows, new_circles, _ = get_bst(bst)
    transforms = [Transform(old_circles[node], new_circles[node]) for node in old_circles.keys() if node in new_circles]
    transforms.extend([Transform(old_arrows[node], new_arrows[node]) for node in old_arrows.keys() if node in new_arrows and node != old_root])
    transforms.append(Transform(old_arrows[new_root].reverse_points(), new_arrows[old_root]))
    if old_root in old_arrows:
        transforms.append(Transform(old_arrows[old_root], new_arrows[new_root]))
    scene.play(*transforms)
    scene.remove(*old_arrows.values(), *old_circles.values())
    return new_root
