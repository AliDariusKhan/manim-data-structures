from manim import *
from bst import BST
from get_bst import get_bst
from insert_bst import insert_bst
from rebalance_bst import rebalance_bst
from random import sample

SPEED_FACTOR = 10

class FastScene(Scene):
    default_speedinfo = {0: SPEED_FACTOR, 1: SPEED_FACTOR}

    def play(self, *animations, **play_kwargs):
        animation_group = AnimationGroup(*animations)

        speedinfo = play_kwargs.pop("speedinfo", self.default_speedinfo)

        super().play(ChangeSpeed(animation_group, speedinfo=speedinfo), **play_kwargs)

class DrawOneBST(Scene):
    """Draws one binary search tree of 30 random numbers"""
    def construct(self):
        arrows, circles, _ = get_bst(BST(sample(range(100), 30)))
        self.add(*arrows.values(), *circles.values())


class DrawManyBSTs(Scene):
    """Draws many binary search trees, transitioning between them"""
    def construct(self):
        arrows, circles, _ = get_bst(BST(sample(range(100), 30)))
        full_bst = Group(*arrows.values(), *circles.values())
        self.add(full_bst)
        self.wait()

        for i in range(30):
            arrows, circles, _ = get_bst(BST(sample(range(100), 30)))
            new_bst = Group(*arrows.values(), *circles.values())
            self.play(Transform(full_bst, new_bst))
            self.wait()

class InsertOneElement(Scene):
    """Inserts a random element to a random BST of size 30"""
    def construct(self):
        random_list = sample(range(100), 31)
        insert_bst(self, BST(random_list[:-1]), random_list[-1])


class InsertAllElements(Scene):
    """Builds a BST with a random list of elements"""
    def construct(self):
        random_list = sample(range(100), 3)
        bst = BST()
        for num in random_list:
            to_remove = insert_bst(self, bst, num)
            self.remove(*to_remove)

class InsertAllElementsAndRebalance(Scene):
    def construct(self):
        random_list = [4, 4]
        print(random_list)
        bst = BST()
        for num in random_list:
            insert_bst(self, bst, num)
            rebalance_bst(self, bst.root, bst)

class InsertAndDelete(Scene):
    def construct(self):
        bst = BST()
        print(bst.scale)
        bst.insert_and_animate(4, self)
        bst.insert_and_animate(5, self)

class InsertAndAnimate(Scene):
    def construct(self):
        random_list = sample(range(100), 4)
        # random_list = [44, 37, 47, 77, 68]
        random_list = [0, -3, -5, -6, -7]
        print(random_list)
        bst = BST()
        # for num in random_list:
        #     bst.insert_and_animate(num, self)
        bst.insert_and_animate(0, self)
        bst.insert_and_animate(1, self)
        bst.insert_and_animate(-1, self)
        bst.insert_and_animate(0.5, self)
        bst.delete_and_animate(1, self)
