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

all_config_path = "../../SupplementaryWebsite/MeasuredPerformanceValues/"
samples_path = "../../Results/"
start_rand = 1
end_rand = 100

file_name_prefix = "sampledConfigurations_"
file_name_strategies = ["twise",
                        "solverBased",
                        "henard",
                        "divDistBased",
                        "grammarBased",
                        "random"
                        ]
file_name_mids = ["_t1", "_t2", "_t3"]
file_name_suffix = ".csv"

features_in_study = {}
configurations_in_study = {}

t1_sampling_sets = {}
t2_sampling_sets = {}
t3_sampling_sets = {}

dict_dataframe = {}


# TODO fix it
def parse_valid_configurations_VP9(case_study):
    with open(all_config_path + case_study + '/measurements.csv', 'r') as f:
        lines = f.readlines()
    configurations = {}
    indexI = 0
    features = lines[0]
    features = list(map(str.strip, features.split(';')))
    for line in lines:
        line = line.split(';')
        config = ''
        for feature in features_in_study[case_study]:
            index = features.index(feature)
            line = list(map(str.strip, line))
            if len(line) < len(features):
                raise ValueError("In line " + str(indexI) + " is an error in VP9 measurements.csv")
            config += str(line[index])
        configurations[config] = indexI
        indexI += 1
    return configurations


def parse_valid_configurations(case_study):
    import xml.dom.minidom as xmlparse
    xmldoc = xmlparse.parse(all_config_path + case_study + '/measurements.xml')
    configurations_elems = xmldoc.getElementsByTagName('data')
    configurations = {}
    index = 0
    print(len(configurations_elems))
    for elem in configurations_elems:
        if elem.getAttribute('columname') != "Configuration" and elem.getAttribute('column') != 'Configuration':
            continue
        value = elem.firstChild.nodeValue
        value = value.split(',')
        values = list(map(str.strip, value))
        configuration = []
        configuration_binary = ""
        for value in values:
            if not value == '':
                configuration.append(value)
        for feature in features_in_study[case_study]:
            if feature in configuration:
                configuration_binary += '1'
            elif feature == 'root':
                configuration_binary += '1'
            else:
                configuration_binary += '0'

        # print(configuration_binary)
        configurations[configuration_binary] = index
        index += 1
    print(index)
    return configurations


def get_all_features(case_study):
    features = []
    line = ""
    with open(samples_path + case_study + '/' + case_study + '_1/' + file_name_prefix + file_name_strategies[0] + file_name_mids[0] + file_name_suffix) as f:
        line = f.readline()
    line = line.split(';')
    features = list(map(str.strip, line))
    features_in_study[case_study] = features


def get_sampling_indices(case_study, strategy):
    t1_sampling_sets[case_study][strategy] = []
    valid_configurations = configurations_in_study[case_study]
    for j in range(0, 3):
        for i in range(start_rand, end_rand + 1):
            sampling_set = []
            with open(samples_path + case_study + '/' + case_study + '_' + str(i) + '/' + file_name_prefix + strategy + file_name_mids[j] + file_name_suffix) as f:
                configurations_csv = f.readlines()
            features = configurations_csv[0]
            features = list(map(str.strip, features.split(';')))
            for line in configurations_csv[1:]:
                line = line.split(';')
                config = ''
                for feature in features_in_study[case_study]:
                    index = features.index(feature)
                    line = list(map(str.strip, line))
                    config += str(line[index])
                if config in valid_configurations:
                    sampling_set.append(valid_configurations[config])
                else:
                    raise ValueError('config is not in configurations set: ' + str(config) + "\n in case_study: " + case_study + " from strategy: " + strategy + " in seed: " + str(i) + file_name_mids[j])
            sampling_set.sort()
            if j == 0:
                t1_sampling_sets[case_study][strategy].append(sampling_set)
            elif j == 1:
                t2_sampling_sets[case_study][strategy].append(sampling_set)
            elif j == 2:
                t3_sampling_sets[case_study][strategy].append(sampling_set)
            else:
                raise NotImplementedError('there is no 4-wise sampling')


def produce_lineplot_values(case_study):
    import pandas as pd
    sampling_strategies = ["t-wise", "solver-based", "randomized solver-based", "distance-based", "grammar-based", "random"]
    x_values_results = []
    x_values_t2_results = []
    x_values_t3_results = []
    y_values_results = []
    y_values_t2_results = []
    y_values_t3_results = []
    x_values = []
    x_values_t2 = []
    x_values_t3 = []
    number_all_configs = len(configurations_in_study[case_study])
    y_values = [0] * number_all_configs
    y_values_t2 = [0] * number_all_configs
    y_values_t3 = [0] * number_all_configs
    for strategy in file_name_strategies:
        strategy_name = sampling_strategies[file_name_strategies.index(strategy)]
        x_values = [strategy_name] * number_all_configs
        x_values_t2 = [strategy_name] * number_all_configs
        x_values_t3 = [strategy_name] * number_all_configs
        sampling_set = t1_sampling_sets[case_study][strategy]
        all_samples = []
        for index_set in sampling_set:
            all_samples = all_samples + index_set
        for idx in all_samples:
            y_values[idx] += 1
        for i in range(0, len(y_values)):
            y_values[i] = y_values[i] / float(len(all_samples))
        sampling_set = t2_sampling_sets[case_study][strategy]
        all_samples = []
        for index_set in sampling_set:
            all_samples = all_samples + index_set
        for idx in all_samples:
            y_values_t2[idx] += 1
        for i in range(0, len(y_values_t2)):
            y_values_t2[i] = y_values_t2[i] / float(len(all_samples))
        sampling_set = t3_sampling_sets[case_study][strategy]
        all_samples = []
        for index_set in sampling_set:
            all_samples = all_samples + index_set
        for idx in all_samples:
            y_values_t3[idx] += 1
        for i in range(0, len(y_values_t3)):
            y_values_t3[i] = y_values_t3[i] / float(len(all_samples))
        x_values_results += x_values
        x_values_t2_results += x_values_t2
        x_values_t3_results += x_values_t3
        y_values_results += y_values
        y_values_t2_results += y_values_t2
        y_values_t3_results += y_values_t3
    output_dir = 'plots/' + case_study
    mkdir_p(output_dir)
    df = pd.DataFrame({"x": x_values_results, "y": y_values_results})
    seaborn_vio_plot(df, output_dir + '/violin' + '_' + case_study + '_' + 't1.pdf', case_study)
    df = pd.DataFrame({"x": x_values_t2_results, "y": y_values_t2_results})
    seaborn_vio_plot(df, output_dir + '/violin' + '_' + case_study + '_' + 't2.pdf', case_study)
    df = pd.DataFrame({"x": x_values_t3_results, "y": y_values_t3_results})
    seaborn_vio_plot(df, output_dir + '/violin' + '_' + case_study + '_' + 't3.pdf', case_study)


def seaborn_vio_plot(df, name, case_study):
    import seaborn as sns
    import matplotlib.pyplot as plt
    from matplotlib import rcParams
    rcParams.update({'figure.autolayout': True})
    number_all_configs = len(configurations_in_study[case_study])
    y_line_value = 1.0 / number_all_configs
    font_size = 12
    # h, w = 28, 28
    sns.set(style="whitegrid")
    # plt.figure(figsize=(h, w))
    plt.figure()
    sns.violinplot(x="x", y="y", data=df, cut=0)
    locs, labels = plt.yticks()
    plt.setp(labels, fontsize=font_size)
    locs, labels = plt.xticks()
    plt.setp(labels, rotation=20, fontsize=font_size, ha='right')
    plt.xlabel("sampling strategy", fontsize=font_size + 2)
    line = plt.axhline(y=y_line_value, linestyle='--', linewidth=2, color='k', label='uniform baseline')
    plt.legend([line], ['uniform baseline'], bbox_to_anchor=(0., 1.02, 1., .102), loc='lower right', ncol=2, borderaxespad=0.)
    plt.ylabel("[%]", fontsize=font_size + 2)
    plt.ylim(0.0, 0.0016)
    plt.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))
    plt.savefig(name)
    plt.close()


def generate_statistical_tests():
    from scipy.stats import uniform
    from skgof import ks_test, cvm_test
    import pandas as pd
    KS_data = {}
    KS_data['case_study'] = []
    CVM_data = {}
    CVM_data['case_study'] = []
    KS_VS_CVM_data = {}
    KS_VS_CVM_data['case_study'] = []
    for strategy in file_name_strategies:
        KS_data[strategy + 't1'] = []
        KS_data[strategy + 't2'] = []
        KS_data[strategy + 't3'] = []
        CVM_data[strategy + 't1'] = []
        CVM_data[strategy + 't2'] = []
        CVM_data[strategy + 't3'] = []
        KS_VS_CVM_data[strategy + 't1'] = []
        KS_VS_CVM_data[strategy + 't2'] = []
        KS_VS_CVM_data[strategy + 't3'] = []
    for case_study in case_studies:
        KS_data['case_study'].append(case_study)
        CVM_data['case_study'].append(case_study)
        KS_VS_CVM_data['case_study'].append(case_study)
        uniform_arr = uniform(0, len(configurations_in_study[case_study]))
        for strategy in file_name_strategies:
            sampling_set = t1_sampling_sets[case_study][strategy]
            t1_KS_positive = 0
            t1_CVM_positive = 0
            t1_KS_VS_CVM_negative = 0
            for index_set in sampling_set:
                if ks_test((index_set), uniform_arr).pvalue >= .05:
                    t1_KS_positive += 1
                    if cvm_test((index_set), uniform_arr).pvalue < .05:
                        t1_KS_VS_CVM_negative += 1
                elif cvm_test((index_set), uniform_arr).pvalue >= .05:
                    t1_KS_VS_CVM_negative += 1
                if cvm_test((index_set), uniform_arr).pvalue >= .05:
                    t1_CVM_positive += 1
            sampling_set = t2_sampling_sets[case_study][strategy]
            t2_KS_positive = 0
            t2_CVM_positive = 0
            t2_KS_VS_CVM_negative = 0
            for index_set in sampling_set:
                if ks_test((index_set), uniform_arr).pvalue >= .05:
                    t2_KS_positive += 1
                    if cvm_test((index_set), uniform_arr).pvalue < .05:
                        t2_KS_VS_CVM_negative += 1
                elif cvm_test((index_set), uniform_arr).pvalue >= .05:
                    t2_KS_VS_CVM_negative += 1
                if cvm_test((index_set), uniform_arr).pvalue >= .05:
                    t2_CVM_positive += 1
            sampling_set = t3_sampling_sets[case_study][strategy]
            t3_KS_positive = 0
            t3_CVM_positive = 0
            t3_KS_VS_CVM_negative = 0
            for index_set in sampling_set:
                if ks_test((index_set), uniform_arr).pvalue >= .05:
                    t3_KS_positive += 1
                    if cvm_test((index_set), uniform_arr).pvalue < .05:
                        t3_KS_VS_CVM_negative += 1
                elif cvm_test((index_set), uniform_arr).pvalue >= .05:
                    t3_KS_VS_CVM_negative += 1
                if cvm_test((index_set), uniform_arr).pvalue >= .05:
                    t3_CVM_positive += 1
            KS_data[strategy + 't1'].append(t1_KS_positive)
            KS_data[strategy + 't2'].append(t2_KS_positive)
            KS_data[strategy + 't3'].append(t3_KS_positive)
            CVM_data[strategy + 't1'].append(t1_CVM_positive)
            CVM_data[strategy + 't2'].append(t2_CVM_positive)
            CVM_data[strategy + 't3'].append(t3_CVM_positive)
            KS_VS_CVM_data[strategy + 't1'].append(t1_KS_VS_CVM_negative)
            KS_VS_CVM_data[strategy + 't2'].append(t2_KS_VS_CVM_negative)
            KS_VS_CVM_data[strategy + 't3'].append(t3_KS_VS_CVM_negative)
    KS_df = pd.DataFrame(data=KS_data)
    CVM_df = pd.DataFrame(data=CVM_data)
    KS_VS_CVM_df = pd.DataFrame(data=KS_VS_CVM_data)
    KS_df.to_csv('KS_results.csv', index=False)
    CVM_df.to_csv('CVM_results.csv', index=False)
    KS_VS_CVM_df.to_csv('KS_VS_CVM_results', index=False)


def mkdir_p(mypath):
    '''Creates a directory. equivalent to using mkdir -p on the command line'''

    from errno import EEXIST
    from os import makedirs, path

    try:
        makedirs(mypath)
    except OSError as exc:
        if exc.errno == EEXIST and path.isdir(mypath):
            pass
        else:
            raise


def start():

    for study in case_studies:
        dict_dataframe[study] = {}
        for t_factor in ['t1', 't2', 't3']:
            dict_dataframe[study] = {}
            dict_dataframe[study]['x'] = []
            dict_dataframe[study]['y'] = []
            dict_dataframe[study]['z'] = []
            dict_dataframe[study]['strategy'] = []
            dict_dataframe[study]['t_factor'] = []
        get_all_features(study)
        if study == "VP9":
            configurations = parse_valid_configurations_VP9(study)
        else:
            configurations = parse_valid_configurations(study)
        configurations_in_study[study] = configurations
        t1_sampling_sets[study] = {}
        t2_sampling_sets[study] = {}
        t3_sampling_sets[study] = {}
        for strategy in file_name_strategies:

            t1_sampling_sets[study][strategy] = []
            t2_sampling_sets[study][strategy] = []
            t3_sampling_sets[study][strategy] = []
            get_sampling_indices(study, strategy)
        produce_lineplot_values(study)
    # generate_statistical_tests()


if __name__ == "__main__":
    start()
