import sys
import os

EPSILON    = 'ε'
END_MARKER = '$'

# Lectura del archivo

def load_grammar(filepath):
    grammar      = {}
    start_symbol = None
    nt_order     = []

    if not os.path.exists(filepath):
        print(f"\nArchivo no encontrado: '{filepath}'\n")
        sys.exit(1)

    with open(filepath, 'r', encoding='utf-8') as f:
        for raw_line in f:
            line = raw_line.strip()

            if not line or line.startswith('#'):
                continue

            if line.upper().startswith('START'):
                parts = line.split()
                if len(parts) >= 2:
                    start_symbol = parts[1]
                continue

            if '->' not in line:
                print(f"Línea ignorada (formato inválido): '{line}'")
                continue

            left, right = line.split('->', 1)
            nt = left.strip()

            if nt not in grammar:
                grammar[nt] = []
                nt_order.append(nt)

            alternatives = right.split('|')
            for alt in alternatives:
                symbols = alt.strip().split()
                if not symbols:
                    continue
                symbols = [EPSILON if s.lower() in ('eps', 'epsilon', 'ε') else s
                           for s in symbols]
                grammar[nt].append(symbols)

    if start_symbol is None:
        start_symbol = nt_order[0] if nt_order else None
        print(f"No se encontró 'START'. Usando '{start_symbol}' como símbolo inicial.\n")

    # Reordenar: símbolo inicial primero
    ordered = {}
    if start_symbol in grammar:
        ordered[start_symbol] = grammar[start_symbol]
    for nt in nt_order:
        if nt != start_symbol:
            ordered[nt] = grammar[nt]

    return ordered, start_symbol

    # Utilidades

def is_terminal(symbol, non_terminals):
    return symbol not in non_terminals and symbol != EPSILON


def first_of_string(symbols, first, non_terminals):
    """FIRST de una secuencia de símbolos."""
    result = set()
    for symbol in symbols:
        if is_terminal(symbol, non_terminals):
            result.add(symbol)
            return result
        result.update(first[symbol] - {EPSILON})
        if EPSILON not in first[symbol]:
            return result
    result.add(EPSILON)
    return result

# FIRST

def compute_first(grammar):
    non_terminals = set(grammar.keys())
    first = {nt: set() for nt in non_terminals}

    changed = True
    while changed:
        changed = False
        for nt, productions in grammar.items():
            for production in productions:

                if production == [EPSILON]:
                    if EPSILON not in first[nt]:
                        first[nt].add(EPSILON)
                        changed = True
                    continue

                for symbol in production:
                    if is_terminal(symbol, non_terminals):
                        if symbol not in first[nt]:
                            first[nt].add(symbol)
                            changed = True
                        break
                    else:
                        before = len(first[nt])
                        first[nt].update(first[symbol] - {EPSILON})
                        if len(first[nt]) > before:
                            changed = True
                        if EPSILON not in first[symbol]:
                            break
                else:
                    if EPSILON not in first[nt]:
                        first[nt].add(EPSILON)
                        changed = True

    return first

# FOLLOW

def compute_follow(grammar, first, start_symbol):
    non_terminals = set(grammar.keys())
    follow = {nt: set() for nt in non_terminals}

    follow[start_symbol].add(END_MARKER)

    changed = True
    while changed:
        changed = False
        for nt, productions in grammar.items():
            for production in productions:
                for i, symbol in enumerate(production):
                    if symbol not in non_terminals:
                        continue

                    beta = production[i + 1:]

                    if beta:
                        first_beta = first_of_string(beta, first, non_terminals)

                        before = len(follow[symbol])
                        follow[symbol].update(first_beta - {EPSILON})
                        if len(follow[symbol]) > before:
                            changed = True

                        if EPSILON in first_beta:
                            before = len(follow[symbol])
                            follow[symbol].update(follow[nt])
                            if len(follow[symbol]) > before:
                                changed = True
                    else:
                        before = len(follow[symbol])
                        follow[symbol].update(follow[nt])
                        if len(follow[symbol]) > before:
                            changed = True

    return follow

# Detección de conflictos LL(1)

def check_ll1(grammar, first, follow):
    non_terminals = set(grammar.keys())
    conflicts = []

    for nt, productions in grammar.items():
        selection_sets = []
        for prod in productions:
            if prod == [EPSILON]:
                sel = follow[nt].copy()
            else:
                fs = first_of_string(prod, first, non_terminals)
                sel = fs - {EPSILON}
                if EPSILON in fs:
                    sel.update(follow[nt])
            selection_sets.append((prod, sel))

        for i in range(len(selection_sets)):
            for j in range(i + 1, len(selection_sets)):
                inter = selection_sets[i][1] & selection_sets[j][1]
                if inter:
                    conflicts.append((nt, selection_sets[i][0],
                                          selection_sets[j][0], inter))

    return conflicts


# Print

def fmt_set(s):
    items = sorted(s, key=lambda x: (x == '$', x == EPSILON, x))
    return "{ " + ", ".join(items) + " }"

def print_grammar(grammar):
    print("\nGramática cargada:")
    for nt, prods in grammar.items():
        rhs = "  |  ".join(" ".join(p) for p in prods)
        print(f"  {nt:<3}  →   {rhs}")
    print()

def print_results(grammar, first, follow):
    nts = list(grammar.keys())
    col = 32

    print(f"  {'No Terminal':<14} {'FIRST':<{col}} {'FOLLOW'}")
    print("  " + "─"*72)
    for nt in nts:
        f1 = fmt_set(first[nt])
        f2 = fmt_set(follow[nt])
        print(f"  {nt:<14} {f1:<{col}} {f2}")

def print_ll1_report(conflicts):
    if not conflicts:
        print("\nLa gramática ES LL(1) — sin conflictos.\n")
    else:
        print("\nLa gramática NO es LL(1) — conflictos detectados:\n")
        for nt, p1, p2, inter in conflicts:
            prod1 = " ".join(p1)
            prod2 = " ".join(p2)
            tokens = ", ".join(sorted(inter))
            print(f"     • {nt}: conflicto en {{ {tokens} }}")
            print(f"          {nt} → {prod1}")
            print(f"          {nt} → {prod2}\n")

# Main

def main():
    if len(sys.argv) >= 2:
        filepath = sys.argv[1]
    else:
        filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gramatica_clase.txt')

    grammar, start_symbol = load_grammar(filepath)

    print(f"Símbolo inicial: {start_symbol}")
    print_grammar(grammar)

    first  = compute_first(grammar)
    follow = compute_follow(grammar, first, start_symbol)

    print("Resultados:\n")
    print_results(grammar, first, follow)

    conflicts = check_ll1(grammar, first, follow)
    print_ll1_report(conflicts)


if __name__ == "__main__":
    main()
