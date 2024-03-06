import svgling
from nltk.tree import Tree

def generate_syntax_tree_image(tree_structure,  output_filepath='static/images/last_tree.svg'):
    # Parse the tree structure
    tree = Tree.fromstring(tree_structure)

    # Draw the tree with svgling
    tree_figure = svgling.draw_tree(tree)

    svg_output = tree_figure.get_svg()._repr_svg_()

    # Save the SVG content to a file
    with open(output_filepath, 'w') as svg_file:
        svg_file.write(svg_output)

# For testing
if __name__ == '__main__':
    filepath = "test_tree.svg"
    test_tree_structure = "(CP (C' (C \u2205) (TP (DP (D' (D \u2205) (NP (N' (N She))))) (T' (T [-PAST]) (ProgP (Prog' (Prog is)  (VP (V' (AdvP (Adv' (Adv probably))) (V' (V' (V having) (DP (D' (D a) (NP (N' (N snack)))))) (PP (P' (P without) (DP (D' (D \u2205) (NP (N' (N me)))))))) ) )))))))"

    generate_syntax_tree_image(test_tree_structure, filepath)
    print(f"Saved the SVG of the provided tree structure to {filepath}.")

