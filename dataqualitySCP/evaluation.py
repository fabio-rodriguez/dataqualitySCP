import json
import matplotlib.pyplot as plt
import numpy as np

from constants import *


#----------------------------------------------------------------------------------------------------------------------------
# EVALUATE  fis		
#----------------------------------------------------------------------------------------------------------------------------
def evaluate_sensor(mf_normal, fuzInputs_normal, mf_pos, fuzInputs_pos, mf_neg, fuzInputs_neg, realInputs):

    result_1 = calculate_fis(mf_normal, fuzInputs_normal, realInputs)    
    result_2 = calculate_fis(mf_pos, fuzInputs_pos, realInputs)
    result_3 = calculate_fis(mf_neg, fuzInputs_neg, realInputs)
    
    return min(result_1, result_2, result_3) == result_1


#----------------------------------------------------------------------------------------------------------------------------
# CALCULATE  fis		
#----------------------------------------------------------------------------------------------------------------------------
def calculate_fis(mf, fuzInputs, realInputs):
    return mf.calculate({fi: ri for fi, ri in zip(fuzInputs, realInputs)})


def evaluate(input, l2):

    normalized_input = normalize(input)  

    irr, flow, tamb, tin, tout = [input[key] for key in KEYS]
    realInputs = [abs(tout - tin), irr, flow]

    ## Evaluate Irradiance
    inputs1, output1, rules1 = irr_normal_fis()
    inputs2, output2, rules2 = irr_pos_fis()
    inputs3, output3, rules3 = irr_neg_fis()
    
    print(rules1, inputs1, rules2, inputs2, rules3, inputs3)
    print(realInputs)
    F_irr = evaluate_sensor(rules1, inputs1, rules2, inputs2, rules3, inputs3, realInputs)

    ## Evaluate Flow
    inputs1, output1, rules1 = flow_normal_fis()
    inputs2, output2, rules2 = flow_pos_fis()
    inputs3, output3, rules3 = flow_neg_fis()
    F_flow = evaluate_sensor(rules1, inputs1, rules2, inputs2, rules3, inputs3, realInputs)

    return {KEY_IRR: F_irr, KEY_FLOW: F_flow, KEY_TAMB: None, KEY_TIN: None, KEY_TOUT: None}
    # l2.put({KEY_IRR: F_irr, KEY_FLOW: F_flow, KEY_TAMB: None, KEY_TIN: None, KEY_TOUT: None})


def normalize(input, path="./norm_scales"):
    
    with open(f'{path}/Min-Max scaler.json', 'r') as f:
        data = json.load(f)
    
    results = []
    for key in KEYS:
        minm, maxm = data[key]["MIN"], data[key]["MAX"]
        results.append((input[key]-minm)/(maxm - minm))

    #TODO Read TH_JUMP
    min_tjump, max_tjump = data["TH_JUMP"]["MIN"], data["TH_JUMP"]["MAX"]
    results.append(min_tjump, max_tjump)

    return results


def test_evaluation():

    ii_1 = [] 
    jj_1 = []
    jj_2 = []
    jj_3 = []

    inputs1, output1, rules1 = flow_normal_fis()
    inputs2, output2, rules2 = flow_pos_fis()
    inputs3, output3, rules3 = flow_neg_fis()

    ts = np.loadtxt('Q_data_eval_Fneg.txt',usecols=[0,1,2,3,4,5,6])
    #pprint(ts)
    n1 = ts[:,0:1]  # input1
    n2 = ts[:,1:2]  # input2
    n3 = ts[:,2:3]  # input3
    n4 = ts[:,3:4]  # out_real
    n5 = ts[:,4:5]  # out_FIS_Norm
    n6 = ts[:,5:6]  # out_FIS_Fpos
    n7 = ts[:,6:7]  # out_FIS_Fneg
    mm= len(n1)

    for i in range(mm):
        realInputs = [n1[i], n2[i], n3[i]]
        ii_1.append(i)
        result_1 = calculate_fis(rules1, inputs1, realInputs)  
        # result_1 = mf_1.calculate({input1_1: n1[i], input2_1: n2[i], input3_1: n3[i]})
        nn_1= list(result_1.values())
        jj_1.append(nn_1)

        # result_2 = mf_2.calculate({input1_2: n1[i], input2_2: n2[i], input3_2: n3[i]})
        result_2 = calculate_fis(rules2, inputs2, realInputs)  
        nn_2= list(result_2.values())
        jj_2.append(nn_2)

        # result_3 = mf_3.calculate({input1_3: n1[i], input2_3: n2[i], input3_3: n3[i]})
        result_3 = calculate_fis(rules3, inputs3, realInputs)  
        nn_3= list(result_3.values())
        jj_3.append(nn_3)

    plt.plot(ii_1, n4)
    plt.plot(ii_1, np.reshape(np.array(jj_1), (len(jj_1),)))
    plt.plot(ii_1, np.reshape(np.array(jj_2), (len(jj_2),)))
    plt.plot(ii_1, np.reshape(np.array(jj_3), (len(jj_3),)))
    plt.legend(loc = 'upper right')
    plt.ylabel( "Real and Estimated prototype" )
    plt.xlabel( "Samples" )
    plt.show()


if __name__ == "__main__":


    test_evaluation()
