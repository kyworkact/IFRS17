import sys
from cashflower import start
from settings import settings
import pandas as pd


if __name__ == "__main__":
    output = start(settings, sys.argv)
    output.to_csv("output/output.csv", index=False)