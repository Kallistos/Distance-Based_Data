#!/usr/bin/env python3


if __name__ == "__main__":
    import os
    import re
    newFolder = "Results/"
    fileSet = set()

    for root, dirs, files in os.walk(newFolder):
        for fileName in files:
            if re.match(r"out_divDistBased_t1PredictionsMLR.log", fileName):
                found_file = str(os.path.join(root[len(newFolder):], fileName))
                fileName = fileName.replace("MLR", "")
                new_found_file = str(os.path.join(root[len(newFolder):], fileName))
                os.rename(newFolder + found_file, newFolder + new_found_file + '_wrong_result')
            if re.match(r"out_grammarBased_t1PredictionsMLR.log", fileName):
                found_file = str(os.path.join(root[len(newFolder):], fileName))
                fileName = fileName.replace("MLR", "")
                new_found_file = str(os.path.join(root[len(newFolder):], fileName))
                os.rename(newFolder + found_file, newFolder + new_found_file + '_wrong_result')
            if re.match(r"out_henard_t1PredictionsMLR.log", fileName):
                found_file = str(os.path.join(root[len(newFolder):], fileName))
                fileName = fileName.replace("MLR", "")
                new_found_file = str(os.path.join(root[len(newFolder):], fileName))
                os.rename(newFolder + found_file, newFolder + new_found_file + '_wrong_result')
            if re.match(r"out_random_t1PredictionsMLR.log", fileName):
                found_file = str(os.path.join(root[len(newFolder):], fileName))
                fileName = fileName.replace("MLR", "")
                new_found_file = str(os.path.join(root[len(newFolder):], fileName))
                os.rename(newFolder + found_file, newFolder + new_found_file + '_wrong_result')
            if re.match(r"out_solverBased_t1PredictionsMLR.log", fileName):
                found_file = str(os.path.join(root[len(newFolder):], fileName))
                fileName = fileName.replace("MLR", "")
                new_found_file = str(os.path.join(root[len(newFolder):], fileName))
                os.rename(newFolder + found_file, newFolder + new_found_file + '_wrong_result')
            if re.match(r"out_twise_t1PredictionsMLR.log", fileName):
                found_file = str(os.path.join(root[len(newFolder):], fileName))
                fileName = fileName.replace("MLR", "")
                new_found_file = str(os.path.join(root[len(newFolder):], fileName))
                os.rename(newFolder + found_file, newFolder + new_found_file + '_wrong_result')
            if re.match(r"out_divDistBased_t2PredictionsMLR.log", fileName):
                found_file = str(os.path.join(root[len(newFolder):], fileName))
                fileName = fileName.replace("MLR", "")
                new_found_file = str(os.path.join(root[len(newFolder):], fileName))
                os.rename(newFolder + found_file, newFolder + new_found_file + '_wrong_result')
            if re.match(r"out_grammarBased_t2PredictionsMLR.log", fileName):
                found_file = str(os.path.join(root[len(newFolder):], fileName))
                fileName = fileName.replace("MLR", "")
                new_found_file = str(os.path.join(root[len(newFolder):], fileName))
                os.rename(newFolder + found_file, newFolder + new_found_file + '_wrong_result')
            if re.match(r"out_henard_t2PredictionsMLR.log", fileName):
                found_file = str(os.path.join(root[len(newFolder):], fileName))
                fileName = fileName.replace("MLR", "")
                new_found_file = str(os.path.join(root[len(newFolder):], fileName))
                os.rename(newFolder + found_file, newFolder + new_found_file + '_wrong_result')
            if re.match(r"out_random_t2PredictionsMLR.log", fileName):
                found_file = str(os.path.join(root[len(newFolder):], fileName))
                fileName = fileName.replace("MLR", "")
                new_found_file = str(os.path.join(root[len(newFolder):], fileName))
                os.rename(newFolder + found_file, newFolder + new_found_file + '_wrong_result')
            if re.match(r"out_solverBased_t2PredictionsMLR.log", fileName):
                found_file = str(os.path.join(root[len(newFolder):], fileName))
                fileName = fileName.replace("MLR", "")
                new_found_file = str(os.path.join(root[len(newFolder):], fileName))
                os.rename(newFolder + found_file, newFolder + new_found_file + '_wrong_result')
            if re.match(r"out_twise_t2PredictionsMLR.log", fileName):
                found_file = str(os.path.join(root[len(newFolder):], fileName))
                fileName = fileName.replace("MLR", "")
                new_found_file = str(os.path.join(root[len(newFolder):], fileName))
                os.rename(newFolder + found_file, newFolder + new_found_file + '_wrong_result')
            if re.match(r"out_divDistBased_t3PredictionsMLR.log", fileName):
                found_file = str(os.path.join(root[len(newFolder):], fileName))
                fileName = fileName.replace("MLR", "")
                new_found_file = str(os.path.join(root[len(newFolder):], fileName))
                os.rename(newFolder + found_file, newFolder + new_found_file + '_wrong_result')
            if re.match(r"out_grammarBased_t3PredictionsMLR.log", fileName):
                found_file = str(os.path.join(root[len(newFolder):], fileName))
                fileName = fileName.replace("MLR", "")
                new_found_file = str(os.path.join(root[len(newFolder):], fileName))
                os.rename(newFolder + found_file, newFolder + new_found_file + '_wrong_result')
            if re.match(r"out_henard_t3PredictionsMLR.log", fileName):
                found_file = str(os.path.join(root[len(newFolder):], fileName))
                fileName = fileName.replace("MLR", "")
                new_found_file = str(os.path.join(root[len(newFolder):], fileName))
                os.rename(newFolder + found_file, newFolder + new_found_file + '_wrong_result')
            if re.match(r"out_random_t3PredictionsMLR.log", fileName):
                found_file = str(os.path.join(root[len(newFolder):], fileName))
                fileName = fileName.replace("MLR", "")
                new_found_file = str(os.path.join(root[len(newFolder):], fileName))
                os.rename(newFolder + found_file, newFolder + new_found_file + '_wrong_result')
            if re.match(r"out_solverBased_t3PredictionsMLR.log", fileName):
                found_file = str(os.path.join(root[len(newFolder):], fileName))
                fileName = fileName.replace("MLR", "")
                new_found_file = str(os.path.join(root[len(newFolder):], fileName))
                os.rename(newFolder + found_file, newFolder + new_found_file + '_wrong_result')
            if re.match(r"out_twise_t3PredictionsMLR.log", fileName):
                found_file = str(os.path.join(root[len(newFolder):], fileName))
                fileName = fileName.replace("MLR", "")
                new_found_file = str(os.path.join(root[len(newFolder):], fileName))
                os.rename(newFolder + found_file, newFolder + new_found_file + '_wrong_result')
