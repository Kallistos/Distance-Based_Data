#!/usr/bin/env python3


case_studies = ["BerkeleyDBC",
                # "7z",
                # "Dune",
                # "Hipacc",
                # "JavaGC",
                # "LLVM",
                # "Polly",
                # "VP9",
                # "lrzip",
                # "x264",
                ]

all_config_path = "../../SupplementaryWebsite/MeasuredPerformanceValues/"
samples_path = "../../Results/"
start_rand = 1
end_rand = 100

file_name_prefix = "sampledConfigurations_"
file_name_strategies = ["grammarBased",
                        "divDistBased",
                        "henard",
                        "random",
                        "solverBased",
                        "twise"
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


def produce_median_indicies(case_study, strategy):
    import statistics
    sampling_sets_set = []
    sampling_sets_set.append(t1_sampling_sets[case_study][strategy])
    sampling_sets_set.append(t2_sampling_sets[case_study][strategy])
    sampling_sets_set.append(t3_sampling_sets[case_study][strategy])

    if len(sampling_sets_set[0]) != len(sampling_sets_set[1]) or len(sampling_sets_set[0]) != len(sampling_sets_set[2]) or len(sampling_sets_set[0]) < 1:
        raise ValueError('not all seeds got sample sets')
    for sampling_set, t_factor in zip(sampling_sets_set, ['t1', 't2', 't3']):
        length = len(sampling_set[0])
        length_val = len(configurations_in_study[case_study])
        steps = length_val / length
        print('length:', length, 'length val:', length_val, 'steps:', steps)
        for j in range(length):
            samples_idx = []
            for i in range(0, len(sampling_set)):
                if j >= len(sampling_set[i]):
                    raise ValueError("j is outside of the sampleset: " + str(j) + " set length: " + str(len(sampling_set[i])) + "\nstrategy: " + strategy + " t_factor: " + t_factor + " length: " + str(length) + " index I: " + str(i) + "case_study: " + case_study + "\n sampling set: " + str(sampling_set[i]))
                samples_idx.append(sampling_set[i][j])
            median_idx = statistics.median(samples_idx)
            lower = int(float(j) * steps)
            upper = int(float((j + 1)) * steps)
            if median_idx in range(lower, upper):
                median_idx = median_idx
            elif median_idx < lower:
                median_idx = lower
            else:
                median_idx = upper
            dict_dataframe[case_study]['x'].extend([int(median_idx)] * len(samples_idx))
            dict_dataframe[case_study]['z'].extend([int(median_idx)] * len(samples_idx))
            dict_dataframe[case_study]['y'].extend(samples_idx)
            dict_dataframe[case_study]['strategy'].extend([strategy] * len(samples_idx))
            dict_dataframe[case_study]['strategy'].extend([t_factor] * len(samples_idx))


def plot_dist_samples(case_study, strategy):
    # import pandas as pd
    import seaborn as sns
    # import numpy as np
    import matplotlib.pyplot as plt
    valid_configurations = configurations_in_study[case_study]
    sns.set(style="whitegrid")
    for i, sample_set in zip(range(1, 101), t1_sampling_sets[case_study][strategy]):
        expanded_sample_set = []
        for j in sample_set:
            expanded_sample_set.append(j)
            expanded_sample_set.append(j - len(valid_configurations))
            expanded_sample_set.append(j + len(valid_configurations))
        output_dir = 'plots/' + case_study + '/t1/' + strategy + '/' + strategy + '_' + str(i)
        mkdir_p(output_dir)
        plt.figure()
        sns.distplot(sample_set, hist=False, rug=True, rug_kws={'height': .5}, kde_kws={'cut': 0})
        plt.xlim(0, len(valid_configurations))
        plt.savefig(output_dir + '/dist.pdf', format='pdf', bbox_inches='tight')
        plt.close()
    # for i, sample_set in zip(range(1, 101), t2_sampling_sets[case_study][strategy]):
    #     expanded_sample_set = []
    #     for j in sample_set:
    #         expanded_sample_set.append(j)
    #         expanded_sample_set.append(j - len(valid_configurations))
    #         expanded_sample_set.append(j + len(valid_configurations))
    #     output_dir = 'plots/' + case_study + '/t2/' + strategy + '/' + strategy + '_' + str(i)
    #     mkdir_p(output_dir)
    #     plt.figure()
    #     sns.distplot(expanded_sample_set, hist=False, rug=True, rug_kws={'height': .5})
    #     plt.xlim(0, len(valid_configurations))
    #     plt.savefig(output_dir + '/dist.pdf', format='pdf', bbox_inches='tight')
    #     plt.close()
    # for i, sample_set in zip(range(1, 101), t3_sampling_sets[case_study][strategy]):
    #     output_dir = 'plots/' + case_study + '/t3/' + strategy + '/' + strategy + '_' + str(i)
    #     mkdir_p(output_dir)
    #     plt.figure()
    #     sns.distplot(sample_set, hist=False, rug=True, rug_kws={'height': .5})
    #     plt.xlim(0, len(valid_configurations))
    #     plt.savefig(output_dir + '/dist.pdf', format='pdf', bbox_inches='tight')
    #     plt.close()


def plot_dist_samples_combined():
    # import pandas as pd
    import seaborn as sns
    # import numpy as np
    import matplotlib.pyplot as plt
    for case_study in case_studies:
        valid_configurations = configurations_in_study[case_study]
        sns.set(style="whitegrid")
        for sample_sets in t1_sampling_sets[case_study]:
            for i in range(1, 11):
                plt.figure()
                output_dir = 'plots/' + case_study + '/t1/' + '/combined' + '_' + str(i)
                mkdir_p(output_dir)
                for strategy in file_name_strategies:
                    print(sample_sets)
                    sample_set = sample_sets[strategy]
                    expanded_sample_set = []
                    for j in sample_set:
                        expanded_sample_set.append(j)
                        expanded_sample_set.append(j - len(valid_configurations))
                        expanded_sample_set.append(j + len(valid_configurations))
                    sns.distplot(sample_set, hist=False, rug=True, rug_kws={'height': .5}, kde_kws={'cut': 0})
                plt.xlim(0, len(valid_configurations))
                plt.savefig(output_dir + '/dist.pdf', format='pdf', bbox_inches='tight')
                plt.close()


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


def seaborn_plot():
    import pandas as pd
    import seaborn as sns
    import numpy as np
    import matplotlib.pyplot as plt

    sns.set(style="whitegrid")
    for study in case_studies:
        xmax = int(dict_dataframe[study]['x'][-1] * 1.01)
        x = np.array(range(-10, xmax, 1))
        df = pd.DataFrame(data=dict_dataframe[study])
        df.to_csv('dataframe' + study + '.csv')
        chart = sns.distplot(df['y'], hue='strategy', col='t_factor', kind='line', markers=True, height=15, aspect=1)
        for ax in chart.axes.flat:
            # ax.set_xticklabels(ax.get_yticklabels(), rotation=30)
            ax.xaxis.grid(True)
            ax.plot(x, x, '-r', linewidth=2)
        plt.savefig('tmpTest' + study + '.pdf')


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
        for strategy in file_name_strategies:
            t1_sampling_sets[study] = {}
            t2_sampling_sets[study] = {}
            t3_sampling_sets[study] = {}

            t1_sampling_sets[study][strategy] = []
            t2_sampling_sets[study][strategy] = []
            t3_sampling_sets[study][strategy] = []
            get_sampling_indices(study, strategy)
            # plot_dist_samples(study, strategy)
            # produce_median_indicies(study, strategy)
    plot_dist_samples_combined()
    # seaborn_plot()


if __name__ == "__main__":
    start()
