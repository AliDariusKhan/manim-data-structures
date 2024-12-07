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
                old_arrows, old_circles, _ = get_bst(deepcopy(bst))
                right_rotate(subtree.right)
                transform_bst(scene, bst, old_arrows, old_circles)
            old_arrows, old_circles, _ = get_bst(deepcopy(bst))
            left_rotate(subtree, bst)
            transform_bst(scene, bst, old_arrows, old_circles)
    if subtree.balance == -2:
        if subtree.left.balance == 1:
            old_arrows, old_circles, _ = get_bst(deepcopy(bst))
            left_rotate(subtree.left)
            transform_bst(scene, bst, old_arrows, old_circles)
        old_arrows, old_circles, _ = get_bst(deepcopy(bst))
        right_rotate(subtree, bst)
        transform_bst(scene, bst, old_arrows, old_circles)

def left_rotate(old_root, bst=None):
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
    return new_root

def right_rotate(old_root, bst=None):
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
    return new_root

def transform_bst(scene, bst, old_arrows, old_circles):
    bst.update_balances()
    new_arrows, new_circles, _ = get_bst(bst)
    transforms = []
    for (old_nodes_and_groups, new_nodes_and_groups) in [(old_circles, new_circles), (old_arrows, new_arrows)]:
        for old_node, old_group in old_nodes_and_groups.items():
            search = [
                new_group for new_node, new_group in new_nodes_and_groups.items() 
                if new_node.key == old_node.key]
            if not search:
                continue
            new_group = search[0]
            transforms.append(Transform(old_group, new_group))

    scene.play(*transforms)
    scene.remove(*old_arrows.values(), *old_circles.values())