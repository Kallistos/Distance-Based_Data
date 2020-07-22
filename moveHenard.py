#!/usr/bin/env python3


if __name__ == "__main__":
    import os
    import re
    newFolder = "Results/"
    fileSet = set()

    for root, dirs, files in os.walk(newFolder):
        for fileName in files:
            if re.match(r"out_divDistBased_t1PredictionsFR.log", fileName):
                found_file = str(os.path.join(root[len(newFolder):], fileName))
                fileName = fileName.replace("FR", "ForestRegressor")
                new_found_file = str(os.path.join(root[len(newFolder):], fileName))
                os.rename(newFolder + found_file, newFolder + new_found_file)
            if re.match(r"out_grammarBased_t1PredictionsFR.log", fileName):
                found_file = str(os.path.join(root[len(newFolder):], fileName))
                fileName = fileName.replace("FR", "ForestRegressor")
                new_found_file = str(os.path.join(root[len(newFolder):], fileName))
                os.rename(newFolder + found_file, newFolder + new_found_file)
            if re.match(r"out_henard_t1PredictionsFR.log", fileName):
                found_file = str(os.path.join(root[len(newFolder):], fileName))
                fileName = fileName.replace("FR", "ForestRegressor")
                new_found_file = str(os.path.join(root[len(newFolder):], fileName))
                os.rename(newFolder + found_file, newFolder + new_found_file)
            if re.match(r"out_random_t1PredictionsFR.log", fileName):
                found_file = str(os.path.join(root[len(newFolder):], fileName))
                fileName = fileName.replace("FR", "ForestRegressor")
                new_found_file = str(os.path.join(root[len(newFolder):], fileName))
                os.rename(newFolder + found_file, newFolder + new_found_file)
            if re.match(r"out_solverBased_t1PredictionsFR.log", fileName):
                found_file = str(os.path.join(root[len(newFolder):], fileName))
                fileName = fileName.replace("FR", "ForestRegressor")
                new_found_file = str(os.path.join(root[len(newFolder):], fileName))
                os.rename(newFolder + found_file, newFolder + new_found_file)
            if re.match(r"out_twise_t1PredictionsFR.log", fileName):
                found_file = str(os.path.join(root[len(newFolder):], fileName))
                fileName = fileName.replace("FR", "ForestRegressor")
                new_found_file = str(os.path.join(root[len(newFolder):], fileName))
                os.rename(newFolder + found_file, newFolder + new_found_file)
            if re.match(r"out_divDistBased_t2PredictionsFR.log", fileName):
                found_file = str(os.path.join(root[len(newFolder):], fileName))
                fileName = fileName.replace("FR", "ForestRegressor")
                new_found_file = str(os.path.join(root[len(newFolder):], fileName))
                os.rename(newFolder + found_file, newFolder + new_found_file)
            if re.match(r"out_grammarBased_t2PredictionsFR.log", fileName):
                found_file = str(os.path.join(root[len(newFolder):], fileName))
                fileName = fileName.replace("FR", "ForestRegressor")
                new_found_file = str(os.path.join(root[len(newFolder):], fileName))
                os.rename(newFolder + found_file, newFolder + new_found_file)
            if re.match(r"out_henard_t2PredictionsFR.log", fileName):
                found_file = str(os.path.join(root[len(newFolder):], fileName))
                fileName = fileName.replace("FR", "ForestRegressor")
                new_found_file = str(os.path.join(root[len(newFolder):], fileName))
                os.rename(newFolder + found_file, newFolder + new_found_file)
            if re.match(r"out_random_t2PredictionsFR.log", fileName):
                found_file = str(os.path.join(root[len(newFolder):], fileName))
                fileName = fileName.replace("FR", "ForestRegressor")
                new_found_file = str(os.path.join(root[len(newFolder):], fileName))
                os.rename(newFolder + found_file, newFolder + new_found_file)
            if re.match(r"out_solverBased_t2PredictionsFR.log", fileName):
                found_file = str(os.path.join(root[len(newFolder):], fileName))
                fileName = fileName.replace("FR", "ForestRegressor")
                new_found_file = str(os.path.join(root[len(newFolder):], fileName))
                os.rename(newFolder + found_file, newFolder + new_found_file)
            if re.match(r"out_twise_t2PredictionsFR.log", fileName):
                found_file = str(os.path.join(root[len(newFolder):], fileName))
                fileName = fileName.replace("FR", "ForestRegressor")
                new_found_file = str(os.path.join(root[len(newFolder):], fileName))
                os.rename(newFolder + found_file, newFolder + new_found_file)
            if re.match(r"out_divDistBased_t3PredictionsFR.log", fileName):
                found_file = str(os.path.join(root[len(newFolder):], fileName))
                fileName = fileName.replace("FR", "ForestRegressor")
                new_found_file = str(os.path.join(root[len(newFolder):], fileName))
                os.rename(newFolder + found_file, newFolder + new_found_file)
            if re.match(r"out_grammarBased_t3PredictionsFR.log", fileName):
                found_file = str(os.path.join(root[len(newFolder):], fileName))
                fileName = fileName.replace("FR", "ForestRegressor")
                new_found_file = str(os.path.join(root[len(newFolder):], fileName))
                os.rename(newFolder + found_file, newFolder + new_found_file)
            if re.match(r"out_henard_t3PredictionsFR.log", fileName):
                found_file = str(os.path.join(root[len(newFolder):], fileName))
                fileName = fileName.replace("FR", "ForestRegressor")
                new_found_file = str(os.path.join(root[len(newFolder):], fileName))
                os.rename(newFolder + found_file, newFolder + new_found_file)
            if re.match(r"out_random_t3PredictionsFR.log", fileName):
                found_file = str(os.path.join(root[len(newFolder):], fileName))
                fileName = fileName.replace("FR", "ForestRegressor")
                new_found_file = str(os.path.join(root[len(newFolder):], fileName))
                os.rename(newFolder + found_file, newFolder + new_found_file)
            if re.match(r"out_solverBased_t3PredictionsFR.log", fileName):
                found_file = str(os.path.join(root[len(newFolder):], fileName))
                fileName = fileName.replace("FR", "ForestRegressor")
                new_found_file = str(os.path.join(root[len(newFolder):], fileName))
                os.rename(newFolder + found_file, newFolder + new_found_file)
            if re.match(r"out_twise_t3PredictionsFR.log", fileName):
                found_file = str(os.path.join(root[len(newFolder):], fileName))
                fileName = fileName.replace("FR", "ForestRegressor")
                new_found_file = str(os.path.join(root[len(newFolder):], fileName))
                os.rename(newFolder + found_file, newFolder + new_found_file)
