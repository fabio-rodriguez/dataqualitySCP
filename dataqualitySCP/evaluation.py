import json
import matplotlib.pyplot as plt
import numpy as np

from constants import *

#----------------------------------------------------------------------------------------------------------------------------
# EVALUATE  fis		
#----------------------------------------------------------------------------------------------------------------------------
def is_faulty_sensor(mf_normal, fuzInputs_normal, mf_pos, fuzInputs_pos, mf_neg, fuzInputs_neg, realInputs, totalPCA):

    result_1 = calculate_fis(mf_normal, fuzInputs_normal, realInputs)    
    result_2 = calculate_fis(mf_pos, fuzInputs_pos, realInputs)
    result_3 = calculate_fis(mf_neg, fuzInputs_neg, realInputs)

    prob1= abs(list(result_1.values())[0] - totalPCA)
    prob2= abs(list(result_2.values())[0] - totalPCA)
    prob3= abs(list(result_3.values())[0] - totalPCA)
    
    return not min(prob1, prob2, prob3) == prob1


#----------------------------------------------------------------------------------------------------------------------------
# CALCULATE  fis		
#----------------------------------------------------------------------------------------------------------------------------
def calculate_fis(mf, fuzInputs, realInputs):
    return mf.calculate({fi: ri for fi, ri in zip(fuzInputs, realInputs)})


def evaluate(input, l2):
    
    ## Evaluate Irradiance
    inputs1, output1, rules1 = irr_normal_fis()
    inputs2, output2, rules2 = irr_pos_fis()
    inputs3, output3, rules3 = irr_neg_fis()

    normalized_input = normalize(input)  
    irr, flow, tamb, tin, tout, tjump = normalized_input
    xtotal, xnormal, xpos, xneg = apply_PCA(KEY_IRR, np.array([tamb, irr, tjump]))
    
    F_irr = is_faulty_sensor(rules1, inputs1, rules2, inputs2, rules3, inputs3, [xnormal, xpos, xneg], xtotal)

    ## Evaluate Flow
    inputs1, output1, rules1 = flow_normal_fis()
    inputs2, output2, rules2 = flow_pos_fis()
    inputs3, output3, rules3 = flow_neg_fis()
    
    xtotal, xnormal, xpos, xneg = apply_PCA(KEY_FLOW, np.array([tout, tjump, flow]))
    F_flow = is_faulty_sensor(rules1, inputs1, rules2, inputs2, rules3, inputs3, [xnormal, xpos, xneg], xtotal)

    return {KEY_IRR: F_irr, KEY_FLOW: F_flow, KEY_TAMB: None, KEY_TIN: None, KEY_TOUT: None}
    # l2.put({KEY_IRR: F_irr, KEY_FLOW: F_flow, KEY_TAMB: None, KEY_TIN: None, KEY_TOUT: None})


def normalize(input):
    
    with open(f'{ROOT_DIR}/{SCALERS_REL_PATH}/Min-Max scaler.json', 'r') as f:
        data = json.load(f)
    
    results = []
    for key in KEYS:
        minm, maxm = data[key]["MIN"], data[key]["MAX"]
        results.append((input[key]-minm)/(maxm - minm))

    Tjump = abs(input['TOUT']-input['TIN'])
    min_tjump, max_tjump = data["TH_JUMP"]["MIN"], data["TH_JUMP"]["MAX"]
    results.append((Tjump - min_tjump) / (max_tjump - min_tjump))

    return results


def apply_PCA(key, input):

    total = np.array(PRINCIPAL_COMPONENTS[key]["total"])
    normal = np.array(PRINCIPAL_COMPONENTS[key]["normal"])
    negative = np.array(PRINCIPAL_COMPONENTS[key]["negative"])
    positive = np.array(PRINCIPAL_COMPONENTS[key]["positive"])

    xtotal = np.dot(input, total)
    xnormal = np.dot(input, normal)
    xpos = np.dot(input, positive)
    xneg = np.dot(input, negative)

    return xtotal, xnormal, xpos, xneg


def test_evaluation():

    ii_1 = [] 
    jj_1 = []
    jj_2 = []
    jj_3 = []

    inputs1, output1, rules1 = flow_normal_fis()
    inputs2, output2, rules2 = flow_pos_fis()
    inputs3, output3, rules3 = flow_neg_fis()

    ts = np.loadtxt('Q_data_eval_Fneg.txt',usecols=[0,1,2,3,4,5,6])
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
        nn_1= list(result_1.values())
        jj_1.append(nn_1)

        result_2 = calculate_fis(rules2, inputs2, realInputs)  
        nn_2= list(result_2.values())
        jj_2.append(nn_2)

        result_3 = calculate_fis(rules3, inputs3, realInputs)  
        nn_3= list(result_3.values())
        jj_3.append(nn_3)

    plt.plot(ii_1, n4, 'g')
    plt.plot(ii_1, np.reshape(np.array(jj_1), (len(jj_1),)), 'b')
    plt.plot(ii_1, np.reshape(np.array(jj_2), (len(jj_2),)), 'r')
    plt.plot(ii_1, np.reshape(np.array(jj_3), (len(jj_3),)), 'y')
    plt.legend(loc = 'upper right')
    plt.ylabel( "Real and Estimated prototype" )
    plt.xlabel( "Samples" )
    plt.show()


if __name__ == "__main__":

    input = {KEY_IRR: 0, KEY_FLOW: 12.1342333333333, KEY_TAMB: 0, KEY_TIN: 84.06999999999998, KEY_TOUT: 86.5533333333333}

    irr, flow, tamb, tin, tout, tjump = normalize(input)
    print("normalized", [tout, tjump, flow])

    total    = np.array(PRINCIPAL_COMPONENTS[KEY_FLOW]["total"])
    normal   = np.array(PRINCIPAL_COMPONENTS[KEY_FLOW]["normal"])
    negative = np.array(PRINCIPAL_COMPONENTS[KEY_FLOW]["negative"])
    positive = np.array(PRINCIPAL_COMPONENTS[KEY_FLOW]["positive"])

    result = apply_PCA(KEY_FLOW, np.array([tout, tjump, flow]))
    print("PCA result", result)
    
    xtotal, xnormal, xpos, xneg = result
    inputs_normal, output_normal, rules_normal = flow_normal_fis()
    inputs_pos, output_pos, rules_pos = flow_pos_fis()
    inputs_neg, output_neg, rules_neg = flow_neg_fis()

    result_1 = calculate_fis(rules_normal, inputs_normal, [xnormal, xpos, xneg])    
    result_2 = calculate_fis(rules_pos, inputs_pos, [xnormal, xpos, xneg])    
    result_3 = calculate_fis(rules_neg, inputs_neg, [xnormal, xpos, xneg])    

    result_1 = list(result_1.values())[0]
    result_2 = list(result_2.values())[0]
    result_3 = list(result_3.values())[0]

    print("fis_result", result_1, result_2, result_3)

    F_flow = is_faulty_sensor(rules_normal, inputs_normal, rules_pos, inputs_pos, rules_neg, inputs_neg, [xnormal, xpos, xneg], xtotal)
    print("eval result", F_flow)

    # test_evaluation()

