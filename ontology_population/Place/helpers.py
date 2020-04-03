import pandas as pd

def write_csv(filename, col_names, cols):
    df = pd.DataFrame(cols)
    df = df.transpose()

    with open(filename, 'w', encoding='utf-8') as f:
            df.to_csv(f, header=col_names)
