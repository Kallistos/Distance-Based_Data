#!/usr/bin/env python3

import sys
import os
import math
from scipy import stats
from typing import List, Dict, Tuple, Any
import copy
from statistics import stdev
import numpy as np

# Needed for temporary directory
import tempfile

# Needed to execute the R-scripts
import subprocess

# The constants
SEPARATION_SIGN = ","
ERROR_FILE_PREFIX = "all_error_"
PERFORMANCE_FILE_PREFIX = "all_perf_"
ML_PREFIXES = ["Predictions_", "PredictionsSVR_", "PredictionsForestRegressor_"]
ERROR_FILE_SUFIX = ".txt"
LOG_FILE_PREFIX = "out_"
LOG_FILE_SUFIX = ".log"
FILE_NAME_SEPARATOR = "_"
T_PARAMETER = [1, 2, 3]
CSV_SEPARATOR = ";"
PERCENT = "\\percent "
NEW_LINE = "\\\\"

BEST_FORMAT_PREFIX = "\\textbf{\\color{Green}"
BEST_FORMAT_SUFIX = "} "

SECOND_FORMAT_PREFIX = "{\\color{Blue}\\underline{"
SECOND_FORMAT_SUFIX = "}} "

CASE_STUDY_MAPPING = {"7z": "7z", "JavaGC": "JavaGC", "Polly": "Polly"}#, "BerkeleyDBC": "BDB-C", "Dune": "Dune",
                      #"Hipacc": "Hipacc", "VP9": "VP9"}

EXCLUDED_DIRECTORIES = ["SinglePlots"]  # , "VP9_disc", "JavaGC_disc", "Hipacc_disc", "Polly_disc"]
FIRST_COLUMN_FORMAT = "e"
OTHER_COLUMN_FORMAT = "abd"

TO_IGNORE_RQ1 = ["rand"]
TO_IGNORE_RQ2 = ["twise"]


def print_usage() -> None:
    """
    Prints the usage of the script.
    """
    print("Usage: <inputDirectory> <typesToAdd> <labelsOfTypes> <outputDir>")
    print("inputDirectory\t The directory containing all information for the subject systems.")
    print("typesToAdd\t A comma-separated list containing the types (e.g., uni, rand, semi)" +
          " that should be displayed in the table.")
    print("labelsOfTypes\t A comma-separated list containing the labels " +
          "(e.g., distribution-aware, random sampling, semi-random sampling) that should be shown on the header.")
    print("outputDir\t The .tex-file where the table should be written to.")


def round_error(number_as_float: float) -> float:
    """
    Rounds the error for the tables. Note that we keep only one decimal.

    :param number_as_float: the number to round as a float.
    :return: the number with only one decimal
    """
    return int(number_as_float * 10) / 10


def retrieve_all_relevant_directories(input_dir: str) -> List[str]:
    """
    Retrieves all relevant directories from the specified directory.

    :param input_dir: the input directory to search for further directories.
    :return: a list of strings, where each string represents the name of one subdirectory.
    """
    subfolders = [f.path for f in os.scandir(input_dir)
                  if f.is_dir() and f.name not in EXCLUDED_DIRECTORIES and "_norm" not in f.name
                  and f.name in CASE_STUDY_MAPPING.keys()]
    return subfolders


def compute_mean_error(file_path: str) -> Tuple[float, List[float]]:
    """
    Computes the mean error and returns a tuple containing the mean error and all values, respectively.

    :param file_path: the file path to the file containing all error values.
    :return: a tuple containing the mean error as a first argument and the list of all values as the second argument.
    """
    avg_error = 0
    all_values = []
    count = 0
    if not os.path.exists(file_path):
        return math.nan, all_values
    with open(file_path, 'r') as file:
        file.readline()
        for line in file:
            count += 1
            value = float(line.split(CSV_SEPARATOR)[1])
            avg_error += value
            all_values.append(value)
        avg_error /= count
    return avg_error, all_values


def read_twise_log_file(file_paths: List[str]) -> Dict[int, float]:
    """
    Reads in the t-wise log file.

    :param file_paths: the paths to the different t-wise files.
    :return: a dictionary which maps each run to the according error rate.
    """
    result = {}
    for filePath in file_paths:
        accuracy = -1
        current_t_parameter = -1
        with open(filePath, 'r') as file:
            analyze_learning = False
            for line in file:
                if ("command:" in line):
                    if "clean-sampling" in line:
                        result[current_t_parameter] = accuracy
                        analyze_learning = False
                        current_t_parameter = -1
                    elif "analyze-learning" in line:
                        analyze_learning = True
                    elif " twise " in line:
                        tmp = line.split(" ")
                        tmp = tmp[len(tmp) - 1].replace("\n", "")
                        current_t_parameter = int(tmp.split(":")[1])
                elif analyze_learning and CSV_SEPARATOR in line:
                    tmp = line.split(CSV_SEPARATOR)
                    current_accuracy = float(tmp[len(tmp) - 1])
                    if accuracy == -1 or current_accuracy < accuracy:
                        accuracy = current_accuracy
    return result


def add_new_line(list_of_strings: List[str]) -> List[str]:
    """
    Adds a new line to each of the strings (useful for writing into a file).

    :param list_of_strings: the list of strings to append a newline to.
    :return: a list of strings containing the newline character.
    """
    new_list = []
    for element in list_of_strings:
        new_list.append(element + "\n")
    return new_list


def gather_information(input_directories: List[str], types_to_add: List[str]) -> Tuple[Dict[Any, Any], Dict[Any, Any]]:
    """
    Gathers information from all files in the input_directories by only considering the sampling strategies given in
    types to add.

    :param input_directories: a list containing the directories to read the data from.
    :param types_to_add: the types of sampling strategies to investigate.
    :return: A tuple containing the average result in the first element as a dictionary; the second element contains
    a dictionary including all error rate values.
    """
    result = {}
    all_results = {}
    for inputDirectory in input_directories:
        case_study = os.path.basename(inputDirectory)
        result[case_study] = {}
        all_results[case_study] = {}
        for ml_algorithm in ML_PREFIXES:
            result[case_study][ml_algorithm] = {}
            all_results[case_study][ml_algorithm] = {}
            for type_to_add in types_to_add:
                result[case_study][ml_algorithm][type_to_add] = {}
                all_results[case_study][ml_algorithm][type_to_add] = {}
                for t in T_PARAMETER:
                    # The t-wise error rate has to be read from the .log-file
                    file_path = os.path.join(inputDirectory,
                                             ERROR_FILE_PREFIX + ml_algorithm + type_to_add + FILE_NAME_SEPARATOR +
                                             "t" + str(t) + ERROR_FILE_SUFIX)
                    avg_value, all_values = compute_mean_error(file_path)
                    result[case_study][ml_algorithm][type_to_add][t] = avg_value
                    all_results[case_study][ml_algorithm][type_to_add][t] = all_values
    return result, all_results


def create_ranking(type_information: Dict[str, Dict[str, Dict[str, Dict[str, float]]]],
                   all_information: Dict[str, Dict[str, Dict[str, Dict[str, float]]]],
                   types_to_add: List[str],
                   to_exclude=None) -> Dict[str, Any]:
    """
    Creates the ranking among the sampling strategies.

    :param type_information: Contains the information of each sampling strategy to rank.
    :param all_information: Contains the information of all runs of each sampling strategy to rank.
    :param types_to_add: The list of types to consider.
    :param to_exclude: Whether to exclude or not to exclude certain types.
    :return: The ranking for each sampling strategy of each case study.
    """
    result = {}
    for case_study in sorted(type_information.keys()):
        result[case_study] = {}
        for ml_algorithm in ML_PREFIXES:
            result[case_study][ml_algorithm] = {}
            for t in T_PARAMETER:
                error_list = []
                all_runs_list = []
                for type_to_add in types_to_add:
                    if to_exclude is not None and type_to_add in to_exclude:
                        error_list.append(math.nan)
                    else:
                        error_list.append(type_information[case_study][ml_algorithm][type_to_add][t])
                    all_runs_list.append(all_information[case_study][ml_algorithm][type_to_add][t])

                result[case_study][ml_algorithm][t] = rank_list(error_list, all_runs_list)
    return result


def rank_list(list_to_rank: List[int], all_runs: List[Any]) -> List[int]:
    """
    Ranks the given list and returns the list with the ranking. Note that we also compare the best 2 strategies and
    perform a Mann-Whitney-U test to derive whether one is significantly better than the other strategy. If so, we
    rank them as first and second. If not, we rank them both as second.

    :param list_to_rank: the list to rank.
    :param all_runs: the list containing the error rate of each run.
    :return: a list of rankings of each sampling strategy.
    """
    # NaN receives the highest value in the comparison
    order = sorted(list_to_rank, key=lambda x: float('inf') if math.isnan(x) else x)

    ranking = list(list_to_rank)
    for i in range(0, len(list_to_rank)):
        ranking[i] = order.index(list_to_rank[i]) + 1

    # After creating the ranking, a t-test is performed on the best two runs.
    first_to_compare = all_runs[ranking.index(1)]

    # find the second rank (which can be 2 or a larger number)
    tmp_rank = list(ranking)
    tmp_rank.remove(1)
    reduced_ranking = sorted(list(set(tmp_rank)))
    second_to_compare = all_runs[ranking.index(reduced_ranking[reduced_ranking.index(min(reduced_ranking))])]

    # This only applies to t-wise
    # TODO: Remove the following lines since we now have multiple t-wise runs
    if len(first_to_compare) == 1:
        first_to_compare = first_to_compare * len(second_to_compare)
    elif len(second_to_compare) == 1:
        second_to_compare = second_to_compare * len(first_to_compare)

    _, pvalue = stats.mannwhitneyu(first_to_compare, second_to_compare)
    # stats.ttest_ind(first_to_compare, second_to_compare, equal_var=False)

    if pvalue > 0.05:
        ranking[ranking.index(1)] = 2

    return ranking


def lower_first_letter(string_to_convert: str) -> str:
    """
    Lowers the first letter.

    :param string_to_convert: the string to convert.
    :return: the converted string.
    """
    return string_to_convert[0].lower()


def compute_mean_value(types_to_add: List[str], all_information: Dict[str, Dict[str, Dict[str, Dict[str, float]]]],
                       to_exclude: List[str]) \
        -> Tuple[Dict[str, Dict[int, List[Any]]], Dict[str, Dict[int, List[int]]]]:
    """
    Computes the mean value of the given types and their ranking.

    :param types_to_add: the sampling strategies to consider.
    :param all_information: this dictionary contains all information from all runs.
    :param to_exclude: the sampling strategies to exclude.
    :return: a tuple where the first element is the mean value and the second contains all rankings.
    """
    means = {}
    count = {}
    type_results = {}
    mean_ranking = {}
    for ml_algorithm in ML_PREFIXES:
        means[ml_algorithm] = {}
        count[ml_algorithm] = {}
        type_results[ml_algorithm] = {}
        mean_ranking[ml_algorithm] = {}
        for t in T_PARAMETER:
            type_results[ml_algorithm][t] = []
            means[ml_algorithm][t] = []
            count[ml_algorithm][t] = []
            for i in range(0, len(types_to_add)):
                type_to_investigate = types_to_add[i]
                type_results[ml_algorithm][t].append([])
                means[ml_algorithm][t].append(0)
                count[ml_algorithm][t].append(0)
                for caseStudy in sorted(all_information):
                    for result in all_information[caseStudy][ml_algorithm][type_to_investigate][t]:
                        type_results[ml_algorithm][t][i].append(result)
                        means[ml_algorithm][t][i] += result
                        count[ml_algorithm][t][i] += 1
                means[ml_algorithm][t][i] /= count[ml_algorithm][t][i]

        # Remove the comparison to the random sampling strategy
        means_copy = copy.deepcopy(means)
        for t in T_PARAMETER:
            for i in range(0, len(types_to_add)):
                type_to_investigate = types_to_add[i]
                if to_exclude is not None and type_to_investigate in to_exclude:
                    means_copy[ml_algorithm][t][i] = math.nan

            mean_ranking[ml_algorithm][t] = rank_list(means_copy[ml_algorithm][t], type_results[ml_algorithm][t])
    return means, mean_ranking


def write_table_to_file(output_dir: str, labels_of_types: List[str], types_to_add: List[str],
                        type_information: Dict[str, Dict[str, Dict[str, Dict[int, float]]]],
                        ranking: Dict[str, Dict[str, Dict[str, List[int]]]], means=None, mean_ranking=None) -> None:
    """
    Writes a LaTeX-formatted table containing the results of the evaluation into a file.

    :param output_dir: the directory to write the table into.
    :param labels_of_types: a list of labels that should be used in the header of the table.
    :param types_to_add: the sampling strategies to consider.
    :param type_information: the mean error rates of each sampling strategy.
    :param ranking: the ranking of the sampling strategies.
    :param means: the mean values over all case studies.
    :param mean_ranking: the mean value ranking over all case studies.
    """
    for ml_algorithm in ML_PREFIXES:
        # Write to the specified file
        file = open(output_dir + "table" + ml_algorithm[0:len(ml_algorithm) - 1] + ".tex", 'w')

        columns = FIRST_COLUMN_FORMAT
        header = "\t\t"
        midrules = "\t\t"
        t_label_line = "\t\t"
        space_between_case_studies = "\t\t"
        # mean_separator = "\\midrule\\multicolumn{" + str(
        #    len(labels_of_types) * len(T_PARAMETER) + 1) + "}{c}{\\cellcolor{white}} \\\\[-0.1cm]\\midrule"

        for i in range(0, len(labels_of_types)):
            columns += OTHER_COLUMN_FORMAT[0:len(T_PARAMETER)]

            if len(T_PARAMETER) == 1:
                header += "&" + labels_of_types[i]
                midrules = "\\midrule"
            else:
                header += "& \\multicolumn{" + str(len(T_PARAMETER)) + "}{c}{" + labels_of_types[i] + "}"
                if i < len(labels_of_types) - 1 and "rand" in labels_of_types[i + 1]:
                    midrules += "\\cmidrule(lr{1.3em}){" + str(i * 3 + 2) + "-" + str(i * 3 + 4) + "} "
                else:
                    midrules += "\\cmidrule(lr){" + str(i * 3 + 2) + "-" + str(i * 3 + 4) + "} "
            for j in T_PARAMETER:
                t_label_line += "& $t=" + str(j) + "$"
                space_between_case_studies += "& "
        header += NEW_LINE
        t_label_line += NEW_LINE + "[0.1cm] "  # \\midrule"
        space_between_case_studies += NEW_LINE

        # Write the header of the table
        file.writelines(add_new_line(["\\begin{adjustbox}{angle=0}",
                                      "\t\\begin{tabular}{" + columns + "}",
                                      "\t\\toprule",
                                      header,
                                      midrules]))
        if len(T_PARAMETER) > 1:
            file.writelines(add_new_line([t_label_line,
                                          space_between_case_studies + "[-0.2cm]"]))

        # Write the results of every case study
        case_study_lines = []
        for case_study_directory in sorted(type_information.keys(), key=lower_first_letter):
            case_study_line = "\t\t"
            if case_study_directory in CASE_STUDY_MAPPING:
                case_study_line += CASE_STUDY_MAPPING[case_study_directory]
            else:
                case_study_line += case_study_directory

            for type_to_investigate in types_to_add:
                for t in T_PARAMETER:
                    if math.isnan(type_information[case_study_directory][ml_algorithm][type_to_investigate][t]):
                        result_to_print = "--"
                    else:
                        result_to_print = str(round_error(type_information[case_study_directory][ml_algorithm][type_to_investigate][t])) + \
                                          PERCENT

                    if ranking is None or ranking[case_study_directory][ml_algorithm][t][types_to_add.index(type_to_investigate)] > 1:
                        case_study_line += "&" + result_to_print
                    else:
                        case_study_line += "&" + BEST_FORMAT_PREFIX + \
                                           result_to_print + \
                                           BEST_FORMAT_SUFIX
            case_study_line += NEW_LINE
            case_study_lines.append(case_study_line)
            case_study_lines.append(space_between_case_studies + "[-0.3cm]")

        # Remove the last space, as it is not needed
        case_study_lines = case_study_lines[0:len(case_study_lines) - 1]

        if means is not None and mean_ranking is not None:
            # Add a line for the mean values and their ranking
            # caseStudyLines.append(meanSeparator)
            mean_line = "Mean "

            for type_to_investigate in types_to_add:
                for t in T_PARAMETER:
                    result_to_print = str(round_error(means[ml_algorithm][t][types_to_add.index(type_to_investigate)])) + PERCENT
                    if mean_ranking[ml_algorithm][t][types_to_add.index(type_to_investigate)] > 1:
                        mean_line += " & " + result_to_print
                    else:
                        mean_line += " & " + BEST_FORMAT_PREFIX + result_to_print + BEST_FORMAT_SUFIX
            mean_line += NEW_LINE
            case_study_lines.append(mean_line)

        file.writelines(add_new_line(case_study_lines))

        # Close all environments
        file.writelines(add_new_line(["\t\t\\bottomrule",
                                      "\t\\end{tabular}",
                                      "\\end{adjustbox}"]))

        file.close()


def export_for_r(output_file: str, data: Dict[str, Dict[str, Dict[str, Dict[int, Any]]]], ml_algorithm: str,
                 to_exclude: List[str] = None) -> None:
    """
    Exports the whole data for another R script. The R script is then concerned with executing the statistical tests.

    :param output_file: the file to write the data into.
    :param data: the data to export.
    :param to_exclude: the sampling strategies to exclude.
    """
    with open(output_file, 'w') as file:
        file.write("CaseStudy;Strategy;t;Result\n")
        for caseStudy in data:
            for type_to_add in data[caseStudy][ml_algorithm]:
                if to_exclude is not None and type_to_add in to_exclude:
                    continue
                for t in T_PARAMETER:
                    for result in data[caseStudy][ml_algorithm][type_to_add][t]:
                        file.write(caseStudy + ";" + type_to_add + ";" + str(t) + ";" +
                                   str(result) + "\n")


def read_in_from_r(input_file: str) -> Dict[int, Tuple[float, List[Tuple[str, float, float]]]]:
    """
    Reads in the data from R.

    :param input_file: the file to read the data in.
    :return: a dictionary containing the results of the evaluation.
    """
    result = {}
    kruskal_p_value = None
    dunn_test_values = []

    with open(input_file, 'r') as file:
        for line in file:
            if "t=" in line:
                if kruskal_p_value is not None:
                    result[t] = (kruskal_p_value, dunn_test_values)
                    dunn_test_values = []
                t = int(line.split("=")[1])
            elif CSV_SEPARATOR in line:
                dunn_result = line.split(";")
                if len(dunn_result) == 3:
                    dunn_test_values.append((dunn_result[0], float(dunn_result[1]), float(dunn_result[2])))
                else:
                    dunn_test_values.append((dunn_result[0], float(dunn_result[1])))
            elif "Kruskal_p" in line:
                kruskal_p_value = float(line.split("=")[1])

        if kruskal_p_value is not None:
            result[t] = (kruskal_p_value, dunn_test_values)

    return result


def compute_standard_deviation(types_to_add: List[str],
                               all_information: Dict[str, Dict[str, Dict[int, List[float]]]]) \
        -> Dict[str, Dict[str, Dict[int, float]]]:
    """
    Computes the standard deviation of the sampling strategies.

    :param types_to_add: the sampling strategies to consider.
    :param all_information: the data of all runs.
    :return: the standard deviation of each sampling strategy, each size and each case study.
    """
    result = {}
    for caseStudy in all_information:
        result[caseStudy] = {}
        for type_to_investigate in types_to_add:
            result[caseStudy][type_to_investigate] = {}
            for t in T_PARAMETER:
                if len(all_information[caseStudy][type_to_investigate][t]) > 1:
                    result[caseStudy][type_to_investigate][t] = \
                        stdev(all_information[caseStudy][type_to_investigate][t])
                else:
                    result[caseStudy][type_to_investigate][t] = 0

    return result


def perform_r_test(all_information: Dict[str, Dict[str, Dict[int, List[float]]]], kruskal: bool = True,
                   to_exclude: List[str] = None) -> Dict[str, Dict[int, Tuple[float, List[Tuple[str, float, float]]]]]:
    """
    Performs the statistical tests to determine the ranking of the sampling strategies.

    :param all_information: all information of the sampling strategies on all case studies and all sample sizes.
    :param kruskal: whether to perform Kruskal-Wallis' test or Levene's test.
    :param to_exclude: the sampling strategies to exclude.
    :return: the result of the statistical evaluation.
    """
    if kruskal:
        approach = "kruskal"
    else:
        approach = "levene"
    dir_path = tempfile.mkdtemp()

    print("Path: " + dir_path)

    kruskal_results = {}
    for ml_algorithm in ML_PREFIXES:
        # Print data in file
        file = dir_path + os.sep + "in.csv"
        export_for_r(file, all_information, ml_algorithm, to_exclude)

        r_output_file = dir_path + os.sep + "out.csv"

        # Execute R script
        command = "Rscript"
        script_path = os.getcwd() + "/PerformKruskalWallis.R"

        arguments = [file, r_output_file, approach]

        cmd = [command, script_path] + arguments

        subprocess.check_call(cmd)

        # Read in results
        kruskal_results[ml_algorithm] = read_in_from_r(r_output_file)

    return kruskal_results


def search_for_tuple(item_to_search_for: str, tuples: List[Tuple[str, float]]) -> Tuple[str, float]:
    """
    Searches for the given item in the list of tuples.

    :param item_to_search_for: the item to search for.
    :param tuples: the tuples to search the item into.
    :return: the tuple if it was found; None otherwise.
    """
    for tuple_in_list in tuples:
        if tuple_in_list[0] == item_to_search_for:
            return tuple_in_list
    return None


def format_p_result(p_value: float, eff_size: float = None) -> List[str]:
    """
    Formats the given statistical test results and returns them in a list.

    :param p_value: the p value of the significance test.
    :param eff_size: the effect size (if included).
    :return: a list containing the formatted p value and the effect size (if included).
    """
    number = 0
    if p_value == 0:
        exponent = float("-inf")
    else:
        exponent = np.floor(np.log10(np.abs(p_value)))

    if 0 >= exponent >= -2:
        number = p_value * 10 ** abs(exponent)

    if exponent == 0:
        if number > 0.05:
            return [""]
        result = "$" + str(round_error(number)) + "$"
    elif exponent == -1:
        if number > 0.5:
            return [""]
        result = "$" + str(round_error(number / 10 ** abs(exponent))) + "$"
    elif exponent == -2:
        if number > 5:
            return [""]
        result = "$" + str(round(number / 10 ** abs(exponent), 2)) + "$"
    elif exponent > -10:
        result = "$10^{-0" + str(int(abs(exponent))) + "}$"
    elif p_value == 0:
        result = "$0$"
    else:
        result = "$10^{" + str(int(exponent)) + "}$"

    if eff_size is not None:
        result2 = " ($" + '{0:.2f}'.format(eff_size) + "$)"
        return [result, result2]

    return [result]


def write_test_results_to_file(output_file: str,
                               kruskal_result: Dict[str, Dict[int, Tuple[float, List[Tuple[str, float, float]]]]],
                               types_to_add: List[str], labels_of_types: List[str], to_exclude: List[str],
                               kruskal: bool) -> None:
    """
    Prints all the test results into to given file.

    :param output_file: the file to write the output into.
    :param kruskal_result: the results from the statistical tests.
    :param types_to_add: the sampling strategies to add.
    :param labels_of_types: the labels of the sampling strategies.
    :param to_exclude: the sampling strategies to exclude.
    :param kruskal: whether to perform the Kruskal-Wallis test of the Levene's test.
    """
    for ml_algorithm in ML_PREFIXES:
        if kruskal:
            test_description = "Kruskal-Wallis test"
            pairwise_test_description = "Mann-Whitney U test"
            test_table_file = output_file + "kruskalTable" + ml_algorithm[0:len(ml_algorithm) - 1] + ".tex"
            pairwise_test_table_file = output_file + "mwuTable" + ml_algorithm[0:len(ml_algorithm) - 1] + ".tex"
        else:
            test_description = "Levene's test"
            pairwise_test_description = "F-test"
            test_table_file = output_file + "leveneTable" + ml_algorithm[0:len(ml_algorithm) - 1] + ".tex"
            pairwise_test_table_file = output_file + "fTable" + ml_algorithm[0:len(ml_algorithm) - 1] + ".tex"

        # 1. Table: Table containing the p-value results from the Kruskal-Wallis test
        with open(test_table_file, 'w') as file:
            file.writelines(add_new_line(["\\begin{tabular}{l r}",
                                          "\\toprule",
                                          "\\multicolumn{2}{c}{\\texttt{" + test_description + "}}\\\\",
                                          "\\midrule",
                                          "& \\textit{p}-value " + NEW_LINE,
                                          "\\midrule"]))

            for t in kruskal_result[ml_algorithm].keys():
                file.writelines(add_new_line(["t=" + str(t) + " & " + format_p_result(
                    kruskal_result[ml_algorithm][t][0])[0] + NEW_LINE]))

            file.writelines(add_new_line(["\\bottomrule",
                                          "\\end{tabular}"]))

        # 2. Table: Table containing the dunn-test values for the pair-wise comparisons
        with open(pairwise_test_table_file, 'w') as file:
            columns = FIRST_COLUMN_FORMAT
            header = ""
            midrules = ""
            t_label_line = ""
            space_between_case_studies = ""
            # Remove all irrelevant columns
            remaining_labels = list(labels_of_types)
            remaining_types = list(types_to_add)
            for exclude in to_exclude:
                remaining_labels.remove(labels_of_types[types_to_add.index(exclude)])
                remaining_types.remove(exclude)

            column_counter = 1

            for i in range(0, len(remaining_labels)):
                column_counter += 3
                columns += OTHER_COLUMN_FORMAT

                header += "& \\multicolumn{3}{c}{" + remaining_labels[i] + "}"
                midrules += "\\cmidrule(lr){" + str(i * 3 + 2) + "-" + str(i * 3 + 4) + "} "
                for j in T_PARAMETER:
                    t_label_line += "& $t=" + str(j) + "$"
                    space_between_case_studies += "& "
            header += NEW_LINE
            t_label_line += NEW_LINE + "[0.1cm] "  # \\midrule"
            space_between_case_studies += NEW_LINE

            if kruskal:
                p_value_text = " [\\textit{p} value ($\hat{A}_{12}$)]}}\\\\"
            else:
                p_value_text = " (\\textit{p} value)}}\\\\"

            # Write the header of the table
            file.writelines(add_new_line(["\\begin{tabular}{" + columns + "}",
                                          "\\toprule",
                                          "\\multicolumn{" + str(
                                              column_counter) + "}{c}{\\normalfont{" + pairwise_test_description +
                                          p_value_text,
                                          "\\midrule",
                                          header,
                                          midrules,
                                          t_label_line,
                                          space_between_case_studies + "[-0.3cm]"]))

            # Write the p-values for all comparisons
            lines_to_write = []
            for i in range(0, len(remaining_types)):
                if kruskal:
                    line_to_write = ""
                    second_line_to_write = "\\multirow{-2}{*}{" + remaining_labels[i] + "}"
                else:
                    line_to_write = remaining_labels[i]
                    second_line_to_write = ""
                for j in range(0, len(remaining_types)):
                    if j == i:
                        line_to_write += " & \\multicolumn{3}{c}{\\cellcolor{white} \\noindent}"
                        second_line_to_write += "& \\multicolumn{3}{c}{\\cellcolor{white}}"
                    else:
                        # Search for the right comparison
                        for t in T_PARAMETER:
                            if len(kruskal_result[ml_algorithm][t][1]) == 0:
                                continue
                            comp_strats = [remaining_types[i], remaining_types[j]]
                            comp_string = comp_strats[0] + " - " + comp_strats[1]
                            t_result = search_for_tuple(comp_string, kruskal_result[ml_algorithm][t][1])

                            if len(t_result) == 3:
                                formated_result = format_p_result(t_result[1], t_result[2])
                                line_to_write += " & " + formated_result[0]
                                second_line_to_write += "& "
                                if len(formated_result) == 2:
                                    second_line_to_write += formated_result[1]
                            else:
                                line_to_write += " & " + format_p_result(t_result[1])[0]

                line_to_write += NEW_LINE
                second_line_to_write += NEW_LINE
                if kruskal:
                    lines_to_write.append(line_to_write + "[-0.1cm]")
                    lines_to_write.append(second_line_to_write)
                else:
                    lines_to_write.append(line_to_write)
                lines_to_write.append(space_between_case_studies + "[-0.3cm]")
            lines_to_write = lines_to_write[:len(lines_to_write) - 1]

            file.writelines(add_new_line(lines_to_write))

            file.writelines(["\\bottomrule",
                             "\\end{tabular}"])


def main() -> None:
    """
    The main method of the script.
    """
    if len(sys.argv) != 5:
        print_usage()
        exit(-1)

    input_dir: str = sys.argv[1]
    output_directory: str = sys.argv[4]
    types_to_add: List[str] = sys.argv[2].split(SEPARATION_SIGN)
    labels_to_add: List[str] = sys.argv[3].split(SEPARATION_SIGN)

    # Some error handling for wrong input
    if len(types_to_add) != len(labels_to_add):
        print("<typesToAdd> and <labelsOfTypes> have to be of the same length.")
        exit(-1)

    if not os.path.exists(output_directory):
        print("The directory '" + output_directory + "' does not exist. Please create it.")
        exit(-1)

    if not os.path.exists(input_dir):
        print("The input directory '" + input_dir + "' does not exist.")
        exit(-1)

    relevant_directories = retrieve_all_relevant_directories(input_dir)

    avg_information, all_information = gather_information(relevant_directories, types_to_add)

    # Create the error rate table
    ranking = create_ranking(avg_information, all_information, types_to_add, TO_IGNORE_RQ1)

    means, mean_ranking = compute_mean_value(types_to_add, all_information, TO_IGNORE_RQ1)

    write_table_to_file(output_directory + os.path.sep, labels_to_add, types_to_add, avg_information,
                        ranking, means, mean_ranking)

    kruskal_result = perform_r_test(all_information, kruskal=True, to_exclude=[])
    write_test_results_to_file(output_directory + os.path.sep, kruskal_result, types_to_add, labels_to_add,
                               kruskal=True, to_exclude=[])

    levene_result = perform_r_test(all_information, kruskal=False, to_exclude=TO_IGNORE_RQ2)
    write_test_results_to_file(output_directory + os.path.sep, levene_result, types_to_add, labels_to_add,
                               kruskal=False, to_exclude=TO_IGNORE_RQ2)


if __name__ == "__main__":
    main()
