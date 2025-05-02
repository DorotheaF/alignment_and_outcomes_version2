import os
import sys
from align_test.alignment import LinguisticAlignment


def calculate_alignment(location, token, start_folder, end_folder):
    folders_gold = [x[0] for x in os.walk(location + "processed/")]
    folders_baseline =  [x[0] for x in os.walk(location + "baseline_processed/")]
    print(len(folders_gold))
    print(len(folders_baseline))
    print("before loop")
    i = 0
    print("Start and end folders:")
    print(folders_gold[start_folder+1])
    print(folders_gold[end_folder])

    # Initialize the analyzer
    analyzer = LinguisticAlignment(alignment_types=["bert", "lexsyn"], #"fasttext",
                                   token = token)

    for folder in folders_gold[start_folder+1:end_folder+2]:
        print("this is folder: " + folder)
        print("FOLDER NUMBER " + str(i))
        print("here")
        print(folder)
        os.makedirs(location + '/by_tutor_metrics/' + str(i))

        results = analyzer.analyze_folder(
            folder_path=folder,
            output_directory=location + "by_tutor_metrics/"+ str(i),
            lag=1  # Number of turns to lag (default: 1),
        )
        i += 1
    i = 0
    for folder in folders_baseline[start_folder+1:end_folder+2]:
        print("this is baseline folder: " + folder)
        print("FOLDER NUMBER " + str(i))
        print("here")
        print(folder)
        os.makedirs(location + '/by_tutor_metrics_baseline/' + str(i))

        results = analyzer.analyze_folder(
            folder_path=folder,
            output_directory=location + "by_tutor_metrics_baseline/" + str(i),
            lag=1  # Number of turns to lag (default: 1),
        )

        i += 1



# location = "C:/Users/Dorot/Emotive Computing Dropbox/Dorothea French/Linguistic_Alignment_and_Outcomes/data/sample_ASR_data_no_split/"
location = "/projects/dofr2963/align_out_2/data/ASR_sample/"

token = sys.argv[sys.argv.index("--token") + 1]
print("token found")
start_folder = int(sys.argv[sys.argv.index("--start") + 1])
end_folder = int(sys.argv[sys.argv.index("--end") + 1])


calculate_alignment(location, token, start_folder, end_folder)