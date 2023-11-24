from cashflower import variable
from input import assumption, main, runplan

@variable()
def duration(t):
    return t

## Read model point
@variable()
def age(t):
    return main.get("Age") + duration(t) - 1

@variable()
def pol_term():
    return main.get("Term")

@variable()
def premium_pp(t):
    return float(assumption["premium_target"].get_value("1", "Premium_Target"))

@variable()
def sum_assured_pp(t):
    return main.get("Sum_Assured")

# Read assumptions
@variable()
def mort_rate(t):
    if (t == 0) or (t > pol_term()):
        return 0
    return float(assumption["mortality"].get_value(str(int(age(t))), "Male"))

@variable()
def lapse_rate(t):
    if (t == 0) or (t > pol_term()):
        return 0
    return float(assumption["lapse"].get_value(str(t), "lapse"))

@variable()
def acq_exp_per_pol(t):
    if (t == 0) or (t > pol_term()):
        return 0
    return float(assumption["expense"].get_value(str(t), "Acq_Per_Pol"))

@variable()
def acq_perc_prem(t):
    if (t == 0) or (t > pol_term()):
        return 0
    return float(assumption["expense"].get_value(str(t), "Acq_Perc_Prem"))

@variable()
def maint_exp_per_pol(t):
    if (t == 0) or (t > pol_term()):
        return 0
    return float(assumption["expense"].get_value(str(t), "Maint_Per_Pol"))

@variable()
def maint_perc_prem(t):
    if (t == 0) or (t > pol_term()):
        return 0
    return float(assumption["expense"].get_value(str(t), "Maint_Perc_Prem"))

@variable()
def disc_rate(t):
    if (t == 0) or (t > pol_term()):
        return 0
    return float(assumption["discount_rate"].get_value(str(t), "Disc_Rate"))

@variable()
def prem_tax_rate(t):
    if (t == 0) or (t > pol_term()):
        return 0
    return float(assumption["prem_tax"].get_value(str(t), "Premium_Tax"))

@variable()
def ra_rate(t):
    if t > pol_term():
        return 0
    return float(assumption["risk_adj"].get_value(str(t), "Risk_Adj_Rate"))

@variable()
def ra_perc_prem(t):
    if t > pol_term():
        return 0
    return float(assumption["risk_adj"].get_value(str(t), "Perc_premium"))

@variable()
def ra_perc_av(t):
    if t > pol_term():
        return 0
    return float(assumption["risk_adj"].get_value(str(t), "Perc_AV"))

@variable()
def coc_rate(t):
    if (t == 0) or (t > pol_term()):
        return 0
    return float(assumption["risk_adj"].get_value(str(t), "Coc_Rate"))

# Read Product Features
@variable()
def comm_rate(t):
    if (t == 0) or (t > pol_term()):
        return 0
    return float(assumption["commission"].get_value(str(t), "Commission"))

@variable()
def surr_val_pp(t):
    if (t == 0) or (t > pol_term()):
        return 0
    return float(assumption["surr_value"].get_value(str(t), "Surr_Value"))

# Survivalship
@variable()
def pols_if(t):
    if t == 0:
        return 1
    return pols_if(t-1) * (1-mort_rate(t)) * (1-lapse_rate(t))

@variable()
def SA_if(t):
    return pols_if(t) * sum_assured_pp(t)

@variable()
def AV_if(t):
    return pols_if(t) * surr_val_pp(t)

@variable()
def pv_pol_if(t):
    if t > pol_term():
        return 0
    return (pols_if(t) + pv_pol_if(t+1)) / (1 + disc_rate(t))

# Per Policy Cashflow
@variable()
def comm_pp(t):
    return comm_rate(t) * premium_pp(t)

@variable()
def prem_tax_pp(t):
    return prem_tax_rate(t) * premium_pp(t)

@variable()
def claim_pp(t):
    return sum_assured_pp(t)

@variable()
def acq_exp_pp(t):
    return acq_exp_per_pol(t) + acq_perc_prem(t) * premium_pp(t)

@variable()
def maint_exp_pp(t):
    return maint_exp_per_pol(t) + maint_perc_prem(t) * premium_pp(t)

# Best Estimate Cashflow
@variable()
def be_premium(t):
    if (t == 0) or (t > pol_term()):
        return 0
    return premium_pp(t)*pols_if(t-1)

@variable()
def be_prem_tax(t):
    if (t == 0) or (t > pol_term()):
        return 0
    return prem_tax_pp(t)*pols_if(t-1)

@variable()
def be_comm(t):
    if (t == 0) or (t > pol_term()):
        return 0
    return comm_pp(t)*pols_if(t-1)

@variable()
def be_acq_exp(t):
    if (t == 0) or (t > pol_term()):
        return 0
    return acq_exp_pp(t)*pols_if(t-1)

@variable()
def be_maint_exp(t):
    if (t == 0) or (t > pol_term()):
        return 0
    return maint_exp_pp(t)*pols_if(t-1)

@variable()
def be_claim(t):
    if t == 0:
        return 0
    return claim_pp(t)*pols_if(t-1)*mort_rate(t)

@variable()
def be_surr_val(t):
    if t == 0:
        return 0
    return surr_val_pp(t)*pols_if(t-1)*lapse_rate(t)

# Present Value of Cashflow
@variable()
def pv_premium(t):
    if t > pol_term():
        return 0
    return be_premium(t) + pv_premium(t+1) / (1 + disc_rate(t))

@variable()
def pv_prem_tax(t):
    if (t == 0) or (t > pol_term()):
        return 0
    return be_prem_tax(t) + pv_prem_tax(t+1) / (1 + disc_rate(t))

@variable()
def pv_comm(t):
    if t > pol_term():
        return 0
    return be_comm(t) + pv_comm(t+1) / (1 + disc_rate(t))

@variable()
def pv_acq_exp(t):
    if (t == 0) or (t > pol_term()):
        return 0
    return be_acq_exp(t) + pv_acq_exp(t+1) / (1 + disc_rate(t))

@variable()
def pv_maint_exp(t):
    if (t == 0) or (t > pol_term()):
        return 0
    return be_maint_exp(t) + pv_maint_exp(t+1) / (1 + disc_rate(t))

@variable()
def pv_claim(t):
    if t > pol_term():
        return 0
    return (be_claim(t) + pv_claim(t+1)) / (1 + disc_rate(t))

@variable()
def pv_surr_ben(t):
    if t > pol_term():
        return 0
    return (be_surr_val(t) + pv_surr_ben(t+1)) / (1 + disc_rate(t))

# PVFCF and Unwind
@variable()
def pv_cf(t):
    return pv_claim(t) + pv_prem_tax(t) + pv_comm(t) + pv_acq_exp(t) + pv_maint_exp(t) + pv_surr_ben(t) - pv_premium(t)

@variable()
def pv_cf_unwind(t):
    if t > pol_term():
        return 0
    return (pv_cf(t) + be_premium(t) - be_prem_tax(t) - be_comm(t)- be_acq_exp(t) - be_maint_exp(t)) * disc_rate(t)  

# Risk Adjustment
@variable()
def ra(t):
    if (t == 0) or (t > pol_term()):
        return 0
    return ra_rate(t-1) * SA_if(t-1) + ra_perc_prem(t-1) * be_premium(t) + ra_perc_av(t-1) * AV_if(t-1)

@variable()
def coc_ra(t):
    if (t == 0) or (t > pol_term()):
        return 0
    return ra(t) * coc_rate(t)

@variable()
def pv_coc_ra(t):
    if (t == 0) or (t > pol_term()):
        return 0
    return (coc_ra(t) + pv_coc_ra(t+1)) / (1 + disc_rate(t))

# CSM
@variable()
def csm(t): 
    if (t > pol_term()) or (t == 0):
        return 0
    elif t == 1:
        return -(pv_cf(t) + pv_coc_ra(t))
    return csm(t-1) + csm_unwind(t-1) - csm_alloc(t-1)

@variable()
def csm_unwind(t):
    if t > pol_term():
        return 0
    return csm(t) * disc_rate(t)

@variable()
def k_factor():
    return csm(1) / pv_pol_if(1)

@variable()
def csm_alloc(t):
    if t > pol_term():
        return 0
    return pols_if(t) * k_factor()

# Deferred Acqusition Expense
@variable()
def new_dac(t):
    if t > pol_term():
        return 0
    return be_comm(t) + be_acq_exp(t)

@variable()
def new_dac(t):
    if t > pol_term():
        return 0
    return be_comm(t) + be_acq_exp(t)

@variable()
def dac_unwind(t):
    if t > pol_term():
        return 0
    return new_dac(t) * disc_rate(t)

@variable()
def dac_alloc_fact(t):
    if (t == 0) or (t > pol_term()):
        return 0
    return dac_alloc_fact(t-1) + new_dac(t) / pv_pol_if(t)

@variable()
def dac_alloc(t):
    if t > pol_term():
        return 0
    return dac_alloc_fact(t) * pols_if(t)