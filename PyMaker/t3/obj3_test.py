import sys

from . import t3_global
from . import obj3_read
from . import obj4_vecrep_calc
from . import pymaker_service

# When Import,
# SIDE EFFECT: make a test result file at t3_global.OBJ3_TEST_RESULT_FILENAME


filestrings = []
allfilelist = obj3_read.obj3_allfilelist()
for i in range(len(allfilelist)):
    questfile = allfilelist[i]
    quest = questfile.split(t3_global.OBJ3_TEST_FILENAME_PREFIX)[1]
    quest = quest[:-4].replace('-',' ')
    filestrings.append(quest)


def obj3_getanswer_upperdoc_urls(allfilelist_index):
    # input : int
    # output : string list
    _, a = obj3_read.obj3_readfile(allfilelist[allfilelist_index])
    return list(set([obj3_read.num2pydoc[k].split('#')[0] for k in a]))


def obj3_getanswer_alldoc_urls(allfilelist_index):
    # input : int
    # output : string list
    _, a = obj3_read.obj3_readfile(allfilelist[allfilelist_index])
    return list(set([obj3_read.num2pydoc[k] for k in a]))


with open(t3_global.OBJ3_TEST_RESULT_FILENAME, 'w') as resultfile:
    resultfile.write('obj3_test.py: test start\n')
    tps = []
    fps = []
    fns = []
    tns = []
    test_iter = 0
    if t3_global.OBJ3_TEST_UPPERDOC:
        for i in range(len(filestrings)):
            test_iter += 1
            fs = filestrings[i]
            answers = obj3_getanswer_upperdoc_urls(i)
            
            # ignore this iteration when there are no answer
            if len(answers) == 0:
                continue
            
            candidates = pymaker_service.evaluate_query(fs, upperdoc=True)
            candidates = ['/'.join(url.split('/')[4:]) for url in candidates]
            
            tp, fp, fn, tn = obj4_vecrep_calc.binary_classification_upperdoc(answers, candidates)
            tps.append(tp)
            fps.append(fp)
            fns.append(fn)
            tns.append(tn)

            resultfile.write('\nITERATION ' + str(test_iter) + '\tCORRECT ' + str(tp) + ' / ' + str(len(answers)) + '\t\tQuery: ' + fs + '\n')
            resultfile.write('CANDIDATES:\n')
            for can in candidates:
                resultfile.write('\t' + can + '\n')
            resultfile.write('ANSWERS:\n')
            for a in answers:
                resultfile.write('\t' + a + '\n')
            resultfile.write('true positive: ' + str(tp) + '\n')
            resultfile.write('false positive: ' + str(fp) + '\n')
            resultfile.write('false negative: ' + str(fn) + '\n')
            resultfile.write('true negative: ' + str(tn) + '\n')
            resultfile.flush()
            
    else:
        for i in range(len(filestrings)):
            test_iter += 1
            fs = filestrings[i]
            answers = obj3_getanswer_alldoc_urls(i)
            
            # ignore this iteration when there are no answer
            if len(answers) == 0:
                continue
            
            candidates = pymaker_service.evaluate_query(fs, upperdoc=False)
            candidates = ['/'.join(url.split('/')[4:]) for url in candidates]
            
            tp, fp, fn, tn = obj4_vecrep_calc.binary_classification_alldoc(answers, candidates)
            tps.append(tp)
            fps.append(fp)
            fns.append(fn)
            tns.append(tn)

            resultfile.write('\nITERATION ' + str(test_iter) + '\tCORRECT ' + str(tp) + ' / ' + str(len(answers)) + '\t\tQuery: ' + fs + '\n')
            resultfile.write('CANDIDATES:\n')
            for can in candidates:
                resultfile.write('\t' + can + '\n')
            resultfile.write('ANSWERS:\n')
            for a in answers:
                resultfile.write('\t' + a + '\n')
            resultfile.write('true positive: ' + str(tp) + '\n')
            resultfile.write('false positive: ' + str(fp) + '\n')
            resultfile.write('false negative: ' + str(fn) + '\n')
            resultfile.write('true negative: ' + str(tn) + '\n')
            resultfile.flush()

    precisions = [(tp/(tp + fp)) if (tp + fp != 0) else 0 for tp, fp in zip(tps, fps)]
    recalls = [(tp/(tp + fn)) if (tp + fn != 0) else 0 for tp, fn in zip(tps, fns)]
    accuracies = [((tp + tn)/(tp + fp + fn + tn)) if (tp + fp + fn + tn != 0) else 0 for tp, fp, fn, tn in zip(tps, fps, fns, tns)]
    average_precision = sum(precisions)/len(precisions)
    average_recall = sum(recalls)/len(recalls)
    average_accuracy = sum(accuracies)/len(accuracies)
    resultfile.write('\nAVERAGE RESULT\n')
    resultfile.write('Average Precision: ' + str(average_precision) + '\n')
    resultfile.write('Average Recall: ' + str(average_recall) + '\n')
    resultfile.write('Average Accuracy: ' + str(average_accuracy) + '\n')

    tpssum = sum(tps)
    fpssum = sum(fps)
    fnssum = sum(fns)
    tnssum = sum(tns)
    resultfile.write('\nTOTAL SUM RESULT\n')
    resultfile.write('True Positive Sum: ' + str(tpssum) + '\n')
    resultfile.write('False Positive Sum: ' + str(fpssum) + '\n')
    resultfile.write('False Negative Sum: ' + str(fnssum) + '\n')
    resultfile.write('True Negatie Sum: ' + str(tnssum) + '\n')
    resultfile.write('Precision from sum values: ' + str(tpssum / (tpssum + fpssum)) + '\n')
    resultfile.write('Recall from sum values: ' + str(tpssum / (tpssum + fnssum)) + '\n')
    resultfile.write('Accuracy from sum values: ' + str((tpssum + tnssum) / (tpssum + fpssum + fnssum + tnssum)) + '\n')
    
    resultfile.write('\nobj3_test.py: test finish\n')
    resultfile.flush()