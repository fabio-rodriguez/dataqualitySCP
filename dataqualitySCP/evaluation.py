from pprint import pprint
from typing import Tuple

from .constants import *

def evaluate_sensor(mf_normal, fuzInputs_normal, mf_pos, fuzInputs_pos, mf_neg, fuzInputs_neg, realInputs):

    result_1 = evaluate_fis(mf_normal, fuzInputs_normal, realInputs)    
    result_2 = evaluate_fis(mf_pos, fuzInputs_pos, realInputs)
    result_3 = evaluate_fis(mf_neg, fuzInputs_neg, realInputs)
    
    return min(result_1, result_2, result_3) == result_1




def evaluate_flow(mf_normal, fuzInputs_normal, mf_pos, fuzInputs_pos, mf_neg, fuzInputs_neg, realInputs):

    result_1 = evaluate_fis(mf_normal, fuzInputs_normal, realInputs)    
    result_2 = evaluate_fis(mf_pos, fuzInputs_pos, realInputs)
    result_3 = evaluate_fis(mf_neg, fuzInputs_neg, realInputs)
    
    return min(result_1, result_2, result_3) == result_1


#----------------------------------------------------------------------------------------------------------------------------
# EVALUATE  fis		
#----------------------------------------------------------------------------------------------------------------------------
def evaluate_fis(mf, fuzInputs, realInputs):
    return mf.calculate({fi: ri for fi, ri in zip(fuzInputs, realInputs)})

    
if __name__ == "__main__":

    #Fis component Input
    i1, i2, i3 = None, None, None

    ## Evaluate Flow
    inputs1, output1, rules1 = flow_normal_fis()
    inputs2, output2, rules2 = flow_pos_fis()
    inputs3, output3, rules3 = flow_neg_fis()
    evaluate_sensor(rules1, inputs1, rules2, inputs2, rules3, inputs3, [i1, i2, i3])

    ## Evaluate Irradiance
    inputs1, output1, rules1 = flow_normal_fis()
    inputs2, output2, rules2 = flow_pos_fis()
    inputs3, output3, rules3 = flow_neg_fis()
    evaluate_sensor(rules1, inputs1, rules2, inputs2, rules3, inputs3, [i1, i2, i3])


