import subprocess
import pandas as pd

subprocess.run("python run.py")

output = pd.read_csv("output/output.csv")
csm_target = 0.15
csm_perc = output.loc[1,"csm"] / output.loc[1, "pv_premium"]
curr_prem = output.loc[1, "premium_pp"]

x=0
guess_high = 10000
guess_low = 1

while abs(csm_perc - csm_target) > 0.00001:
    if csm_perc > csm_target:
        guess_high = curr_prem
        new_prem = (curr_prem + guess_low)/2
    else:
        guess_low = curr_prem
        new_prem = (curr_prem + guess_high)/2
    df = pd.read_csv("input/premium_target.csv")
    df.loc[0, 'Premium_Target'] = new_prem
    df.to_csv("input/premium_target.csv", index=False)
    subprocess.run("python run.py")
    output = pd.read_csv("output/output.csv")
    csm_perc = output.loc[1,"csm"] / output.loc[1, "pv_premium"]
    curr_prem = output.loc[1, "premium_pp"]
    x=x+1
    print("run", x, ", current premium:", curr_prem, ", current csm %:", csm_perc)