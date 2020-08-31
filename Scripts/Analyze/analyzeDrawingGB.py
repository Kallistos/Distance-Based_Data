#!/usr/bin/env python3

case_studies = ["7z",
                "BerkeleyDBC",
                "Dune",
                "Hipacc",
                "JavaGC",
                "LLVM",
                "lrzip",
                "Polly",
                "VP9",
                "x264",
                ]

samples_path = "../../Results/"
start_rand = 1
end_rand = 100

file_name_prefix = "out_"
strategy = "grammarBased"

file_name_prefix = "out_"
file_name_mids = ["_t1", "_t2", "_t3"]
file_name_suffix = ".log"


def start():
    import pandas as pd
    data = {}
    for case_study in case_studies:
        data[case_study] = {}
        for file_name_mid in file_name_mids:
            invalid_configs = 0
            for i in range(start_rand, end_rand + 1):
                with open(samples_path + case_study + '/' + case_study + '_' + str(i) + "/" + file_name_prefix + strategy + file_name_mid + file_name_suffix, 'r') as f:
                    lines = f.readlines()
                for line in lines:
                    if "invalid number: " in line:
                        invalid_configs += 1
            data[case_study][file_name_mid] = invalid_configs / 100.0
    df = pd.DataFrame(data=data)
    print(df)


if __name__ == "__main__":
    start()
