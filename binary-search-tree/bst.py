from copy import deepcopy
from manim import *

LEFT_STRING = 'left'
RIGHT_STRING = 'right'

class Node:
    """Simple class that represents a BST node"""
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.balance = 0

class BST:
    """Class that represents a full binary search tree"""
    def __init__(self):
        self.root = None
        self.arrows = None
        self.circles = None
        self.scale = None
    
    def insert(self, keys):
        """Inserts a list of keys into the BST recursively"""
        def insert_helper(node, key):
            if node is None:
                return Node(key)
            if key < node.key:
                node.left = insert_helper(node.left, key)
            else:
                node.right = insert_helper(node.right, key)
            return node

        for key in keys:
            self.root = insert_helper(self.root, key)

    def insert_and_animate(self, key, scene):
        if self.root is None:
            self.root = Node(key)
            self.arrows, self.circles, self.scale = get_bst(self, -7, 14, 4, 8, True)
            circle = deepcopy(self.circles).popitem()[1]
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
            scene.remove(circle, *self.arrows.values(), *self.circles.values())
            return
        
        def insert_helper(node, parent, direction, key, tracing_circle):
            if node is None:
                new_node = Node(key)
                setattr(parent, direction, new_node)
                new_arrows, new_circles, new_scale = get_bst(self, -7, 14, 4, 8, True)
                scene.play(
                    *[Transform(self.circles[node], new_circles[node]) for node in self.circles.keys() if node in new_circles],
                    *[Transform(self.arrows[node], new_arrows[node]) for node in self.arrows.keys() if node in new_arrows],
                    Transform(tracing_circle, new_circles[new_node]),
                )
                scene.play(FadeIn(new_arrows[new_node]))
                self.animate_balance_propagation(new_arrows[new_node], True, scene)
                scene.remove(
                    *self.arrows.values(), 
                    *self.circles.values(), 
                    tracing_circle, 
                    new_circles[new_node], 
                    new_arrows[new_node]
                    )
                
                self.arrows, self.circles, self.scale = new_arrows, new_circles, new_scale
                return True
            scene.play(tracing_circle.animate.next_to(self.circles[node], UP))
            parent_balance_change = False
            direction = LEFT_STRING if key < node.key else RIGHT_STRING
            balance_change = insert_helper(getattr(node, direction), node, direction, key, tracing_circle)
            new_balance = node.balance + (1 if direction == RIGHT_STRING else -1)
            if balance_change:
                self.animate_balance_change(node, scene, new_balance)
            if abs(node.balance) == 2:
                if (node.balance > 0) != (getattr(node, direction).balance > 0):
                    self.rotate(scene, getattr(node, direction), node, direction)
                node = self.rotate(scene, node, parent, RIGHT_STRING if direction == LEFT_STRING else LEFT_STRING)
            parent_balance_change = balance_change and abs(node.balance) == 1
            if parent:
                self.animate_balance_propagation(self.arrows[node], parent_balance_change, scene)
            return parent_balance_change
        
        tracing_circle = Group(
            Circle(
                radius=self.scale*0.375, 
                color=YELLOW, 
                stroke_width=self.scale*3
            )
            .set_fill(BLACK, opacity=1),
            Text(
                str(key), 
                font_size=self.scale*25),
            Text(
                str(0),
                font_size=self.scale*20,
                fill_opacity=0).move_to(DOWN*self.scale*0.375)
        ).next_to(self.circles[self.root], UP, buff=10)
        scene.add(*self.circles.values(), tracing_circle, *self.arrows.values())
        insert_helper(self.root, None, None, key, tracing_circle)

    def rotate(self, scene, old_root, parent, direction):
        other_direction = RIGHT_STRING if direction == LEFT_STRING else LEFT_STRING
        new_root = getattr(old_root, other_direction)
        setattr(old_root, other_direction, getattr(new_root, direction))
        setattr(new_root, direction, old_root)
        if parent:
            parent_to_root = LEFT_STRING if parent.left == old_root else RIGHT_STRING
            setattr(parent, parent_to_root, new_root)
        else:
            self.root = new_root
        new_arrows, new_circles, new_scale = get_bst(self)
        transforms = [Transform(self.circles[node], new_circles[node]) 
                    for node in self.circles.keys() 
                    if node in new_circles]
        transforms.extend([Transform(self.arrows[node], new_arrows[node]) 
                        for node in self.arrows.keys() 
                        if node in new_arrows and node != old_root])
        transforms.append(Transform(self.arrows[new_root].reverse_points(), new_arrows[old_root]))
        if old_root in self.arrows:
            transforms.append(Transform(self.arrows[old_root], new_arrows[new_root]))
        scene.play(*transforms)
        scene.remove(*self.arrows.values(), *self.circles.values())
        self.circles, self.arrows, self.scale = new_circles, new_arrows, new_scale
        if new_root.balance == 2 and old_root.balance == 2:
            self.animate_balance_change(old_root, scene, -1)
            self.animate_balance_change(new_root, scene, 0)
        elif old_root.balance == 2 and new_root.balance == 1:
            self.animate_balance_change(old_root, scene, 0)
            self.animate_balance_change(new_root, scene, 0)
        elif old_root.balance == 1 and new_root.balance == -1:
            self.animate_balance_change(old_root, scene, 0)
            self.animate_balance_change(new_root, scene, -2)
        elif old_root.balance == 1 and new_root.balance == 0:
            self.animate_balance_change(old_root, scene, 0)
            self.animate_balance_change(new_root, scene, -1)
        elif old_root.balance == 1 and new_root.balance == 1:
            self.animate_balance_change(old_root, scene, -1)
            self.animate_balance_change(new_root, scene, -1)
        elif new_root.balance == -2 and old_root.balance == -2:
            self.animate_balance_change(old_root, scene, 1)
            self.animate_balance_change(new_root, scene, 0)
        elif old_root.balance == -2 and new_root.balance == -1:
            self.animate_balance_change(old_root, scene, 0)
            self.animate_balance_change(new_root, scene, 0)
        elif old_root.balance == -1 and new_root.balance == 1:
            self.animate_balance_change(old_root, scene, 0)
            self.animate_balance_change(new_root, scene, 2)
        elif old_root.balance == -1 and new_root.balance == 0:
            self.animate_balance_change(old_root, scene, 0)
            self.animate_balance_change(new_root, scene, 1)
        else:
            self.animate_balance_change(old_root, scene, 1)
            self.animate_balance_change(new_root, scene, 1)    
        return new_root

    def animate_balance_propagation(self, arrow, balance_change, scene):
        for time_width in [0, 1]:
            scene.play(ShowPassingFlash(
                arrow.copy().set_stroke(width=20).reverse_points().set_color(GREEN if balance_change else RED),
                run_time=1,
                time_width=time_width
            ))
    
    def animate_balance_change(self, node, scene, new_balance):
        node.balance = new_balance
        scene.add(*self.circles.values(), *self.arrows.values())
        self.circles[node][2].set_value(str(node.balance))
        new_circle_mobject = Group(
            Circle(
                radius=self.scale*0.375, 
                color=BLUE, 
                stroke_width=self.scale*3
            )
            .set_fill(BLACK, opacity=1),
            Text(
                str(node.key), 
                font_size=self.scale*25),
            Text(
                str(node.balance),
                font_size=self.scale*20,
                fill_opacity=1).move_to(DOWN*self.scale*0.575)
        ).move_to(self.circles[node])
        scene.play(Transform(self.circles[node], new_circle_mobject))
        scene.remove(self.circles[node])
        scene.add(new_circle_mobject)
        self.circles[node] = new_circle_mobject

    def __init__(self, keys=None):
        self.root = None
        if keys:
            self.insert(keys)
    
    def search(self, key):
        """Returns a list of nodes containing the path from root to target node"""
        path = []
        def search_helper(node, key):
            if node is None:
                return None
            path.append(node)
            if key < node.key:
                return search_helper(node.left, key)
            elif key > node.key:
                return search_helper(node.right, key)
            else:
                return node
        
        return search_helper(self.root, key), path[:-1]

    def delete(self, key):
        """Deletes the node with the given key from the tree"""
        parent, temp, is_left_child = None, self.root, False
        while temp.key != key:
            parent = temp
            if key < temp.key:
                is_left_child = True
                temp = temp.left
            else:
                temp = temp.right
        
        if temp.left is None and temp.right is None:
            if parent is None:
                self.root = None
                return
            if is_left_child:
                parent.left = None
            else:
                parent.right = None
        
        elif temp.left is None or temp.right is None:
            if parent is None:
                self.root = temp.left 
    
    def update_balances(self):
        """Updates the balance of all nodes in the tree"""
        def update_balances_helper(node):
            if node is None:
                return -1
            left_depth = 1 + update_balances_helper(node.left)
            right_depth = 1 + update_balances_helper(node.right)
            node.balance = right_depth - left_depth
            return max(left_depth, right_depth)
        
        update_balances_helper(self.root)

def get_bst(bst: BST, left=-7, width=14, top=4, height=8, extra_space_at_top=True):
    if bst.root is None:
        return {}, {}, 0
    
    relative_positions = {}

    def naively_assign(current_node: Node, current_pos: int):
        """Assigns relative column positions to each node, with no regard for overlap"""
        if current_node is None:
            return
        
        relative_positions[current_node] = current_pos
        naively_assign(current_node.left, current_pos-1)
        naively_assign(current_node.right, current_pos+1)
    

    naively_assign(bst.root, 0)

    def eliminate_overlap(current_node: Node):
        """Recursively shifts the tree to eliminate overlaps and enforce a minimum horizontal distance between nodes from the bottom up"""
        if current_node is None:
            return
        
        eliminate_overlap(current_node.left)
        eliminate_overlap(current_node.right)

        def compute_rightmost_or_leftmost(current_node: Node, depth: int, depth_dict: dict, rightmost: bool):
            """Calculates and stores either the rightmost or leftmost position in a given subtree for every depth level"""
            if current_node is None:
                return
            
            operator = max if rightmost else min
            if depth in depth_dict.keys():
                depth_dict[depth] = operator(depth_dict[depth], relative_positions[current_node])
            else:
                depth_dict[depth] = relative_positions[current_node]

            compute_rightmost_or_leftmost(current_node.left, depth+1, depth_dict, rightmost)
            compute_rightmost_or_leftmost(current_node.right, depth+1, depth_dict, rightmost)

        
        rightmost_in_left, leftmost_in_right = {}, {}
        compute_rightmost_or_leftmost(current_node.left, 0, rightmost_in_left, True)
        compute_rightmost_or_leftmost(current_node.right, 0, leftmost_in_right, False)

        overlap_given_depth = {
            depth: rightmost_in_left[depth] - leftmost_in_right[depth] 
            for depth in set(rightmost_in_left.keys()).intersection(leftmost_in_right.keys())
        }

        if len(overlap_given_depth) == 0:
            return

        amount_to_shift = max(overlap_given_depth.values()) / 2 + 1
        
        def shift_subtree(current_node: Node, amount_to_shift: int):
            """Shifts the entire subtree rooted at the given node to the right by some given amount (could be negative)"""
            if current_node is None:
                return
            
            relative_positions[current_node] += amount_to_shift
            shift_subtree(current_node.left, amount_to_shift)
            shift_subtree(current_node.right, amount_to_shift)
        

        shift_subtree(current_node.left, -amount_to_shift)
        shift_subtree(current_node.right, amount_to_shift)
    

    eliminate_overlap(bst.root)

    def get_depth(current_node: Node):
        """Returns the depth of the current subtree"""
        if current_node is None:
            return 0
        return 1 + max(get_depth(current_node.left), get_depth(current_node.right))


    num_cols = max(relative_positions.values()) - min(relative_positions.values()) + 1
    horiz_increment = width / (num_cols+1)
    vert_increment = height / (get_depth(bst.root)+1+extra_space_at_top)
    scale_factor = min(horiz_increment, vert_increment)
    radius = scale_factor * 0.375
    minimum_position = min(relative_positions.values())

    if extra_space_at_top:
        top -= vert_increment

    circles = {}

    def get_circles(current_node: Node, depth: int):
        """Converts the relative horizontal coordinates to circle objects in the canvas"""
        if current_node is None:
            return

        x_coord = left + (relative_positions[current_node] - minimum_position + 1)*horiz_increment
        y_coord = top - (depth+1)*vert_increment

        circles[current_node] = Group(
            Circle(radius=radius, color=BLUE, stroke_width=scale_factor*3).set_fill(BLACK, opacity=1),
            Text(str(current_node.key), font_size=scale_factor*25),
            Text(str(current_node.balance), font_size=scale_factor*20).move_to(DOWN*radius*1.5)
        ).move_to(RIGHT*x_coord + UP*y_coord)

        get_circles(current_node.left, depth+1)
        get_circles(current_node.right, depth+1)
    

    get_circles(bst.root, 0)

    arrows = {}

    def get_arrows(current_node: Node):
        """Creates arrow objects in the canvas mapping from circle center to circle center"""
        if current_node is None:
            return
        
        for child in [n for n in [current_node.left, current_node.right] if n is not None]:
            arrows[child] = Line(
                circles[current_node].get_center(), 
                circles[child].get_center(),
                buff=0,
                stroke_width=scale_factor*3,
                z_index=-10
            )
        
        get_arrows(current_node.left)
        get_arrows(current_node.right)
    

    get_arrows(bst.root)

    return arrows, circles, scale_factor
