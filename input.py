import pandas as pd
from cashflower import Runplan, ModelPointSet, CSVReader


runplan = Runplan(data=pd.DataFrame({"version": [1]}))

#main = ModelPointSet(data=pd.read_csv("input/model_point.csv"))


data = pd.read_csv("input/model_point.csv", dtype={'Age': int})
main = ModelPointSet(data=data)




assumption = {
    "commission": CSVReader("input/commission.csv"),
    "discount_rate": CSVReader("input/discount_rate.csv"),
    "expense": CSVReader("input/expense.csv"),
    "lapse": CSVReader("input/lapse.csv"),
    "mortality": CSVReader("input/mortality.csv"),
    "prem_tax": CSVReader("input/prem_tax.csv"),
    "risk_adj": CSVReader("input/risk_adj.csv"),
    "surr_value": CSVReader("input/surr_value.csv")
}

