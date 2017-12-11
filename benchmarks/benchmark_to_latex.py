import sys

# The expected name of the log file is `model_timestamp.log`

def parse_time(method, result):
    if method == 'VI':
        # sum of model construction and model checking times
        return float(result[0]) + float(result[1])
    else: # expecting heuristic method
        return float(result[0])


def parse_model_constants(model, result):
    # the order in result has to match the order of describe_parameters()
    # of the model in benchmark.py
    if model in ['zeroconf', 'consensus', 'branch-zeroconf']:
        return (2, 'N=' + result[0] + ';K=' + result[1])
    elif model == 'firewire':
        return (2, 'delay=' + result[0] + ';fast=' + result[1])
    elif model == 'coin4':
        return (1, 'K=' + result[0])
    else:
        return (0, '')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: ' + sys.argv[0] + ' model_timestamp.log',
                file=sys.stderr)
        sys.exit(1)

    # Parse model name
    log_name = sys.argv[1]
    model = log_name.split('/')[-1].split('_')[0]
    if model not in ['branch-zeroconf', 'zeroconf', 'firewire', 'leader6', 'wlan6', 'coin4']:
        print('Unrecognized model: ' + model + ' (if you created a new model please add it to this file).',
                file=sys.stderr)
        exit(1)

    # Read the file
    all_lines = None
    with open(log_name, 'r') as log:
        # this might be problematic if our logs grow big
        all_lines = log.read().split('\n')

    # Handle non-existing file problem
    if all_lines is None:
        print('File could not be opened or read', file=sys.stderr)
        exit(1)

    # select every second line, starting with the first (i.e. second in
    # non-zero indexing)
    result_lines = all_lines[1::2]

    # split the lines into columns
    result_lines_split = map(lambda l: list(map(lambda c: c.strip(), l.split('|'))),
            result_lines)

    # results : model_parameters -> method_ucb-const -> time
    results = {}
    all_model_constants = set() # i.e. N=5;K=4
    methods = set() # method names, e.g. MCTS-BRTDP_UCB=0.5

    # Process the lines into the results map
    for result in result_lines_split:
        method = result[0]
        ucb_const = result[1]
        full_method = method + '_UCB=' + ucb_const

        n_model_constants, model_constants = parse_model_constants(model, result[2:])
        time = parse_time(method, result[2 + n_model_constants:])

        if model_constants not in all_model_constants:
            results[model_constants] = {}
            all_model_constants.add(model_constants)

        if full_method not in methods:
            methods.add(full_method)

        results[model_constants][full_method] = str(time)


    # Create order on constants and methods
    all_model_constants_l = sorted(list(all_model_constants))
    methods_l = sorted(list(methods))
    n_methods_l = len(methods_l)

    # Latex table header
    print('\\begin{tabular}{ l ' + (' | c' * n_methods_l) +  '  }')

    print('{:<20}'.format(model), end=' & ')
    for mi in range(n_methods_l):
        method = methods_l[mi]
        end = ' & ' if mi < n_methods_l - 1 else ' \\\\ '
        print('{:^24}'.format(method.replace('_', '\\_')), end=end)
    print()

    # Results map into latex table rows
    for constants in all_model_constants_l:
        print('{:<20}'.format(constants), end=' & ')
        for mi in range(n_methods_l):
            method = methods_l[mi]
            end = ' & ' if mi < n_methods_l - 1 else ' \\\\ '

            # This is here to be used with wrong benchmark logs where
            # some method is said to use UCB when it in fact does not.
            # So in places where the record is missing we just print
            # an empty space -- the result is in some other column.
            #
            # if method not in results[constants]:
                # print('{:>24}'.format(''), end=end)
                # continue

            print('{:>24}'.format(results[constants][method]), end=end)
        print()

    # Latex table footer
    print('\\end{tabular}')

