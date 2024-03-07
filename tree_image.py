# tree_image.py
import sys
#sys.path.insert(0, '/Projects/svgling')
import svgling
#sys.path.remove('/Projects/svgling')
from nltk.tree import Tree

def generate_syntax_tree_image(tree_structure, tree_movement, output_filepath='static/images/last_tree.svg'):
    # Parse the tree structure
    tree = Tree.fromstring(tree_structure)

    # Draw the tree with svgling
    tree_figure = svgling.draw_tree(tree)

    # Apply movement arrows if provided
    if tree_movement:
        # Convert list of lists to tuple of tuples for movement_arrow function
        for move in tree_movement:
            # Convert each pair in the list to a tuple
            start, end = map(tuple, move)
            tree_figure.movement_arrow(start, end)

    svg_output = tree_figure.get_svg()._repr_svg_()

    # Save the SVG content to a file
    with open(output_filepath, 'w') as svg_file:
        svg_file.write(svg_output)

# For testing
if __name__ == '__main__':
    filepath = "test_tree.svg"
    test_tree_structure = "(CP (C' (C \u2205) (TP (DP (D' (D \u2205) (NP (N' (N She))))) (T' (T [-PAST]) (ProgP (Prog' (Prog is)  (VP (V' (AdvP (Adv' (Adv probably))) (V' (V' (V having) (DP (D' (D a) (NP (N' (N snack)))))) (PP (P' (P without) (DP (D' (D \u2205) (NP (N' (N me)))))))) ) )))))))"

    generate_syntax_tree_image(test_tree_structure, None, filepath)
    print(f"Saved the SVG of the provided tree structure to {filepath}.")

