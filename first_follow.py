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