# this could be seriously refactored
def gen_tree(depth, node):
    if depth == 0:
        return

    print('[] x = ' + str(node) + ' -> ', end='')
    print('0.2:(x\'=' + str(4*node + 1) + ') + 0.8:(x\'=' + str(4*node + 2) + ');')

    print('[] x = ' + str(node) + ' -> ', end='')
    print('0.2:(x\'=' + str(4*node + 3) + ') + 0.8:(x\'=' + str(4*node + 4) + ');')

    gen_tree(depth - 1, 4*node + 1)
    gen_tree(depth - 1, 4*node + 2)

    gen_tree(depth - 1, 4*node + 3)
    gen_tree(depth - 1, 4*node + 4)


def gen_sink(sources, value):
    for source in sources:
        print('[] x = ' + str(source) + ' -> 1:(x\'=' + str(value) + ');')

    # self loop
    print('[] x = ' + str(value) + ' -> 1:(x\'=' + str(value) + ');')

def gen_tree_wrapper(depth, node):
    print('mdp')
    print('module M1')

    n_nodes = 4**(depth+1) // 3 - 1
    print('x : [0..' + str(n_nodes) + '] init 0;')

    gen_tree(depth, node)
    # gen_sink(range(21, 51 + 1), n_nodes + 1)
    # gen_sink(range(52, 84 + 1), n_nodes + 2)
    gen_sink(range(5,5+4), n_nodes + 1)

    print('endmodule')

gen_tree_wrapper(2, 0)
