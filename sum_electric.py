""" Sum kWH used and group by month.
    Use terminal; first arg needs to be file path
    Will output a Excel file called electric_sum
    Use only complete months in CSV file.  
    Will look for "Startdate" in CSV file    

"""

import pandas as pd
import sys


def main():
    p = sys.argv[1]
    # p = "C:\cs_files\Python\csv\electric.csv"
    g = groupby_sum_kwh(p)
    write_to_excel(g)


def groupby_sum_kwh(p: str) -> dict:
    """ Read CSV file, sums kwH by month.  Returns -> dict"""
    try:
        df = pd.read_csv(p)
        # reads Startdate and changes from type obj -> datetime64
        df.Startdate = pd.to_datetime(df.Startdate, format='%Y/%m/%d')
        df.index = df.Startdate
        # groupby, t is a zip object
        t = df.groupby(pd.Grouper(freq='M')).Usage.sum()
        # k is a timestamp object. Set a dictionary to str of month and KwH sum
        d = {str(k)[:7]: round(v) for k, v in t.items()}
        return d

    except FileNotFoundError:
        print(f"file not found")
        return None


def write_to_excel(d: dict) -> None:
    df = pd.DataFrame(data=d, index=[0])
    df.T.to_excel('electric_sum.xlsx', index_label='Month', header=['Kwh'])


if __name__ == "__main__":
    main()
