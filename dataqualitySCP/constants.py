import joblib
import json
import keras
import os

from fuzzy_logic.mf import NormalMF
from fuzzy_logic.sugeno_fs import SugenoFuzzySystem
from fuzzy_logic.terms import Term
from fuzzy_logic.variables import FuzzyVariable, SugenoVariable, LinearSugenoFunction

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

DETECTION_MODELS_REL_PATH = "models/detection"
PREDICTION_MODELS_REL_PATH = "models/prediction"
SCALERS_REL_PATH = "norm_scales"
OUTPUTS_REL_PATH = "outputs"
PATH_TO_DATASETS = "data"

KEY_IRR = "IRR"
KEY_FLOW = "FLOW"
KEY_TAMB = "TAMB"
KEY_TIN = "TIN"
KEY_TOUT = "TOUT"

KEYS = [KEY_IRR, KEY_FLOW, KEY_TAMB, KEY_TIN, KEY_TOUT]
PREDICTION_KEYS = [KEY_IRR, KEY_FLOW, KEY_TIN, KEY_TOUT]
EVALUATION_KEYS = [KEY_IRR, KEY_FLOW]

with open(f"{ROOT_DIR}/{DETECTION_MODELS_REL_PATH}/principal_components.json") as file:
    PRINCIPAL_COMPONENTS = json.load(file)

with open(f'{ROOT_DIR}/{SCALERS_REL_PATH}/Min-Max scaler.json', 'r') as f:
    EVALUATION_SCALER = json.load(f)


PREDICTION_MODELS_NAME = ["irradiance_model.h5", "flow_model.h5", "tamb_model.h5", "tin_model.h5", "tout_model.h5"]
PREDICTION_MODELS = { key: keras.models.load_model(f'{ROOT_DIR}/{PREDICTION_MODELS_REL_PATH}/{name}') for key, name in zip(KEYS, PREDICTION_MODELS_NAME) } 

PREDICTION_SCALER = joblib.load(f'{ROOT_DIR}/{SCALERS_REL_PATH}/std_scaler.bin')

#----------------------------------------------------------------------------------------------------------------------------
# FIS NORMAL Flow
#----------------------------------------------------------------------------------------------------------------------------
def flow_normal_fis():

    # INPUT 1
    input1_1: FuzzyVariable = FuzzyVariable(
        'input1' ,-0.0389942196803568 , 1.06999465829934,
        Term('mf1', NormalMF(0.123104034266344, 0.826044542175984)),
        Term('mf2', NormalMF(0.346673985457923, 0.24206726222766)),
        Term('mf3', NormalMF(0.357415533253909, 0.233796517254717))
    )

    # INPUT 2
    input2_1: FuzzyVariable = FuzzyVariable(    
        'input2' ,-0.038994219680357, 1.06999465829934,
        Term('mf1', NormalMF(0.123104034266364, 0.826044542175993)),
        Term('mf2', NormalMF(0.346673985457041, 0.242067262227022)),
        Term('mf3', NormalMF(0.357415533254930, 0.233796517255332))
    )

    # INPUT 3
    input3_1: FuzzyVariable = FuzzyVariable(
        'input3' ,-0.0389942196803568 , 1.06999465829934,
        Term('mf1', NormalMF(0.123104034266344, 0.826044542175984)),
        Term('mf2', NormalMF(0.346673985457923, 0.24206726222766)),
        Term('mf3', NormalMF(0.357415533253909, 0.233796517254717))
    )

    # OUTPUT
    output_1: SugenoVariable = SugenoVariable(
        'output',                               # a*x                          b*y                         c*x               const
        LinearSugenoFunction('mf1', {input1_1: 0.305582604808673, input2_1: 0.305582605454873, input3_1: 0.305582604728885}, 0.0572243079404312),
        LinearSugenoFunction('mf2', {input1_1: 0.394565625277662, input2_1: 0.394565626011022, input3_1: 0.394565625164924}, -0.494107837643341),
        LinearSugenoFunction('mf3', {input1_1: 0.280726339208789, input2_1: 0.280726340782161, input3_1: 0.280726339242822}, 0.435292403598637)
    )

    # RULES
    mf_1: SugenoFuzzySystem = SugenoFuzzySystem([input1_1, input2_1, input3_1], [output_1])
    mf_1.rules.append(mf_1.parse_rule('if (input1 is mf1) and (input2 is mf1) and (input3 is mf1) then (output is mf1)'))
    mf_1.rules.append(mf_1.parse_rule('if (input1 is mf2) and (input2 is mf2) and (input3 is mf2) then (output is mf2)'))
    mf_1.rules.append(mf_1.parse_rule('if (input1 is mf3) and (input2 is mf3) and (input3 is mf3) then (output is mf3)'))

    return [input1_1, input2_1, input3_1], output_1, mf_1 

#----------------------------------------------------------------------------------------------------------------------------
# FIS Fpos Flow
#----------------------------------------------------------------------------------------------------------------------------
def flow_pos_fis():
    # INPUT 1
    input1_2: FuzzyVariable = FuzzyVariable(
        'input1' ,-0.0741636748830084, 1.18315255286271,
        Term('mf1', NormalMF(0.122793688582051, 0.938751259430643)),
        Term('mf2', NormalMF(0.345871231868713, 0.355380630340831)),
        Term('mf3', NormalMF(0.357111298534827, 0.346652781409675))
    )

    # INPUT 2
    input2_2: FuzzyVariable = FuzzyVariable(    
        'input2' ,0.0741636748830081, 1.18315255286271,
        Term('mf1', NormalMF(0.122793688582081, 0.938751259430658)),
        Term('mf2', NormalMF(0.345871231868031, 0.355380630340425)),
        Term('mf3', NormalMF(0.357111298535255, 0.34665278141001))
    )

    # INPUT 3
    input3_2: FuzzyVariable = FuzzyVariable(
        'input3' ,0.0741636748830084 , 1.18315255286271,
        Term('mf1', NormalMF(0.122793688582051, 0.938751259430643)),
        Term('mf2', NormalMF(0.345871231868713, 0.355380630340831)),
        Term('mf3', NormalMF(0.357111298534827, 0.346652781409675))
    )

    # OUTPUT
    output_2: SugenoVariable = SugenoVariable(
        'output',                             # a*x                          b*y                         c*x               const
        LinearSugenoFunction('mf1', {input1_2: 0.305553405956061, input2_2: 0.305553405539167, input3_2: 0.305553405588825}, 0.0746249955460366),
        LinearSugenoFunction('mf2', {input1_2: 0.394512420544176, input2_2: 0.39451242148039 , input3_2: 0.394512420620508}, -0.485416636374415),
        LinearSugenoFunction('mf3', {input1_2: 0.281009591880382, input2_2: 0.281009592038608, input3_2: 0.281009591259266}, 0.439156345961127)
    )

    # RULES
    mf_2: SugenoFuzzySystem = SugenoFuzzySystem([input1_2, input2_2, input3_2], [output_2])
    mf_2.rules.append(mf_2.parse_rule('if (input1 is mf1) and (input2 is mf1) and (input3 is mf1) then (output is mf1)'))
    mf_2.rules.append(mf_2.parse_rule('if (input1 is mf2) and (input2 is mf2) and (input3 is mf2) then (output is mf2)'))
    mf_2.rules.append(mf_2.parse_rule('if (input1 is mf3) and (input2 is mf3) and (input3 is mf3) then (output is mf3)'))

    return [input1_2, input2_2, input3_2], output_2, mf_2 

#----------------------------------------------------------------------------------------------------------------------------
# FIS Fneg Flow
#----------------------------------------------------------------------------------------------------------------------------
def flow_neg_fis():

    # INPUT 1
    input1: FuzzyVariable = FuzzyVariable(
        'input1' ,-0.152152114243722, 1.18315255286271,
        Term('mf1', NormalMF(0.12137803525838, 0.709075050608713)),
        Term('mf2', NormalMF(0.341855501056847, 0.126296618322062)),
        Term('mf3', NormalMF(0.353514677689855, 0.117129489249006))
    )

    # INPUT 2
    input2: FuzzyVariable = FuzzyVariable(    
        'input2' ,-0.152152114243722, 1.18315255286271,
        Term('mf1', NormalMF(0.121378035258422, 0.709075050608732)),
        Term('mf2', NormalMF(0.341855501056336, 0.126296618321721)),
        Term('mf3', NormalMF(0.353514677690549, 0.117129489249557))
    )

    # INPUT 3
    input3: FuzzyVariable = FuzzyVariable(
        'input3' ,-0.152152114243722 , 1.18315255286271,
        Term('mf1', NormalMF(0.12137803525838, 0.709075050608713)),
        Term('mf2', NormalMF(0.341855501056847, 0.126296618322062)),
        Term('mf3', NormalMF(0.353514677689855, 0.117129489249006))
    )

    # OUTPUT
    output: SugenoVariable = SugenoVariable(
        'output',                             # a*x                          b*y                         c*x               const
        LinearSugenoFunction('mf1', {input1: 0.305673661633261, input2: 0.305673662639408, input3: 0.305673660719284}, 0.0398392881134347),
        LinearSugenoFunction('mf2', {input1: 0.39712286251359 , input2: 0.397122862987269, input3: 0.397122861840034}, -0.429986782416667),
        LinearSugenoFunction('mf3', {input1: 0.27782392824066 , input2: 0.277823928934528, input3: 0.277823928492705}, 0.358718610716059)
    )

    # RULES
    mf: SugenoFuzzySystem = SugenoFuzzySystem([input1, input2, input3], [output])
    mf.rules.append(mf.parse_rule('if (input1 is mf1) and (input2 is mf1) and (input3 is mf1) then (output is mf1)'))
    mf.rules.append(mf.parse_rule('if (input1 is mf2) and (input2 is mf2) and (input3 is mf2) then (output is mf2)'))
    mf.rules.append(mf.parse_rule('if (input1 is mf3) and (input2 is mf3) and (input3 is mf3) then (output is mf3)'))

    return [input1, input2, input3], output, mf

#----------------------------------------------------------------------------------------------------------------------------
# FIS Fnormal Irradiance
#----------------------------------------------------------------------------------------------------------------------------
def irr_normal_fis():

    # INPUT 1 
    input1: FuzzyVariable = FuzzyVariable(
        'input1' ,0.218085791619847 , 1.12836951920858,
        Term('mf1', NormalMF(0.180431886015704, 0.818542814099084)),
        Term('mf2', NormalMF(0.190687177611429, 0.370018201546076)),
        Term('mf3', NormalMF(0.178150052299639, 0.591058277710598))
    )

    # INPUT 2
    input2: FuzzyVariable = FuzzyVariable(
        'input2' ,0.218085791619847, 1.12836951920858,
        Term('mf1', NormalMF(0.180431886015704, 0.818542814099084)),
        Term('mf2', NormalMF(0.19068717761143, 0.370018201546077)),
        Term('mf3', NormalMF(0.17815005229964, 0.591058277710599))
        )

    # INPUT 3
    input3: FuzzyVariable = FuzzyVariable(
        'input3' ,0.218085791619847 , 1.12836951920858, 
        Term('mf1', NormalMF(0.180431886015703, 0.818542814099085)),
        Term('mf2', NormalMF(0.190687177611429, 0.370018201546077)),
        Term('mf3', NormalMF(0.178150052299639, 0.591058277710598))
        
    )

    # OUTPUT 
    output: SugenoVariable = SugenoVariable(
        'output',                            # a*x                          b*y                         c*z               const
        LinearSugenoFunction('mf1', {input1: 0.191633377044807, input2: 0.191633376543859, input3: 0.191633384353581}, 0.3181624453073850),
        LinearSugenoFunction('mf2', {input1: 0.214053751983730, input2: 0.214053751886237, input3: 0.214053752261121}, 0.0839786914025338),
        LinearSugenoFunction('mf3', {input1: 0.198784881789136, input2: 0.198784881363252, input3: 0.198784885887324}, 0.1865431695010290)
    )

    # RULES
    mf: SugenoFuzzySystem = SugenoFuzzySystem([input1, input2, input3], [output])
    mf.rules.append(mf.parse_rule('if (input1 is mf1) and (input2 is mf1) and (input3 is mf1) then (output is mf1)'))
    mf.rules.append(mf.parse_rule('if (input1 is mf2) and (input2 is mf2) and (input3 is mf2) then (output is mf2)'))
    mf.rules.append(mf.parse_rule('if (input1 is mf3) and (input2 is mf3) and (input3 is mf3) then (output is mf3)'))

    return [input1, input2, input3], output, mf 

#----------------------------------------------------------------------------------------------------------------------------
# FIS Fpos Irradiance
#----------------------------------------------------------------------------------------------------------------------------
def irr_pos_fis():

    # INPUT 1
    input1: FuzzyVariable = FuzzyVariable(
        'input1' ,0.366996589307713 , 1.27728031689645, 
        Term('mf1', NormalMF(0.180432019583753, 0.967453554760682)),
        Term('mf2', NormalMF(0.190687174313699, 0.518929014925389)),
        Term('mf3', NormalMF(0.178149940219674, 0.739969050438249))
        )

    #INPUT 2
    input2: FuzzyVariable = FuzzyVariable(
        'input2' ,0.366996589307713, 1.27728031689645,
        Term('mf1', NormalMF(0.180432019583753, 0.967453554760682)),
        Term('mf2', NormalMF(0.190687174313699, 0.518929014925389)),
        Term('mf3', NormalMF(0.178149940219674, 0.73996905043825))
        )

    #INPUT 3
    input3: FuzzyVariable = FuzzyVariable(
        'input3' ,0.366996589307713 , 1.27728031689645, 
        Term('mf1', NormalMF(0.180432019583753, 0.967453554760682)),
        Term('mf2', NormalMF(0.190687174313699, 0.518929014925389)),
        Term('mf3', NormalMF(0.178149940219673, 0.739969050438249))
    )

    # OUTPUT
    output: SugenoVariable = SugenoVariable(
        'output',                               # a*x                          b*y                         c*z               const
    LinearSugenoFunction('mf1', {input1: 0.191633360983205 , input2: 0.191633359430900, input3: 0.191633363152966}, 0.419299756040078),
    LinearSugenoFunction('mf2', {input1: 0.214053763879175 , input2: 0.214053763667291, input3: 0.214053764032021}, 0.175100040618918),
    LinearSugenoFunction('mf3', {input1: 0.198784643298306 , input2: 0.198784641210721, input3: 0.198784647383997}, 0.284486090094169)
    )

    # RULES
    mf: SugenoFuzzySystem = SugenoFuzzySystem([input1, input2, input3], [output])
    mf.rules.append(mf.parse_rule('if (input1 is mf1) and (input2 is mf1) and (input3 is mf1) then (output is mf1)'))
    mf.rules.append(mf.parse_rule('if (input1 is mf2) and (input2 is mf2) and (input3 is mf2) then (output is mf2)'))
    mf.rules.append(mf.parse_rule('if (input1 is mf3) and (input2 is mf3) and (input3 is mf3) then (output is mf3)'))

    return [input1, input2, input3], output, mf 

#----------------------------------------------------------------------------------------------------------------------------
# FIS Fneg Irradiance
#----------------------------------------------------------------------------------------------------------------------------
def irr_neg_fis():

    # INPUT 1
    input1: FuzzyVariable = FuzzyVariable(
        'input1' ,0.0691749939319808 ,  1.27728031689645,
        Term('mf1', NormalMF(0.180431833480804, 0.669632043658998)),
        Term('mf2', NormalMF(0.190687187899893, 0.221107408301358)),
        Term('mf3', NormalMF(0.178150093946139, 0.442147498026007))
    )

    # INPUT 2
    input2: FuzzyVariable = FuzzyVariable(
        'input2' ,0.0691749939319808 ,  1.27728031689645,
        Term('mf1', NormalMF(0.180431833480805, 0.669632043658998)),
        Term('mf2', NormalMF(0.190687187899893, 0.221107408301358)),
        Term('mf3', NormalMF(0.178150093946139, 0.442147498026007)) 
    )

    # INPUT 3
    input3: FuzzyVariable = FuzzyVariable(
        'input3' ,0.0691749939319808 ,  1.27728031689645,
        Term('mf1', NormalMF(0.180431833480804, 0.669632043658999)),
        Term('mf2', NormalMF(0.190687187899893, 0.221107408301358)),
        Term('mf3', NormalMF(0.178150093946139, 0.442147498026006)) 
    )

    # OUTPUT 
    output: SugenoVariable = SugenoVariable(
        'output',                                   # c*z                          b*y                         a*x                   const
    LinearSugenoFunction('mf1', {input1: 0.191633295138922, input2: 0.191633295446842, input3: 0.191633301975411}, 0.217025361283163),
    LinearSugenoFunction('mf2', {input1: 0.214053701803020, input2: 0.214053701620074, input3: 0.214053702020819}, -0.00714265027237051),
    LinearSugenoFunction('mf3', {input1: 0.198784830117647, input2: 0.198784829310161, input3: 0.198784834558033}, 0.08860079407109300)
    )

    # RULES
    mf: SugenoFuzzySystem = SugenoFuzzySystem([input1, input2, input3], [output])
    mf.rules.append(mf.parse_rule('if (input1 is mf1) and (input2 is mf1) and (input3 is mf1) then (output is mf1)'))
    mf.rules.append(mf.parse_rule('if (input1 is mf2) and (input2 is mf2) and (input3 is mf2) then (output is mf2)'))
    mf.rules.append(mf.parse_rule('if (input1 is mf3) and (input2 is mf3) and (input3 is mf3) then (output is mf3)'))

    return [input1, input2, input3], output, mf 


KEY_ANFIS = {
    KEY_IRR: {
        "normal" : irr_normal_fis(),
        "positive" : irr_pos_fis(),
        "normal" : irr_normal_fis(),
    },
    KEY_FLOW: {
        "normal" : flow_normal_fis(),
        "positive" : flow_pos_fis(),
        "normal" : flow_normal_fis(),
    }
}

