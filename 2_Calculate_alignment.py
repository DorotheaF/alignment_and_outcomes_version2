import os


def calculate_alignment(location):
    folders_gold = [x[0] for x in os.walk(location + "processed/")]
    folders_baseline =  [x[0] for x in os.walk(location + "baseline_processed/")]
    print(len(folders_gold))
    print(len(folders_baseline))
    print("before loop")
    i = 0

    # Initialize the analyzer
    analyzer = LinguisticAlignment(alignment_types=["fasttext", "bert", "lexsyn"])

    for folder in folders_gold[1:len(folders_gold)]:
        print("this is folder: " + folder)
        print("FOLDER NUMBER " + str(i))
        print("here")
        print(folder)
        os.makedirs(location + '/by_tutor_metrics/' + str(i))

        results = analyzer.analyze_folder(
            folder_path=location + "processed/",
            output_directory=location + "by_tutor_metrics/"+ str(i),
            lag=1  # Number of turns to lag (default: 1),
        )
        i += 1

    for folder in folders_baseline[1:len(folders_baseline)]:
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





#     invalid files might have too short student responses

#test

location = "C:/Users/Dorot/Emotive Computing Dropbox/Dorothea French/Linguistic_Alignment_and_Outcomes/data/sample_ASR_data_no_split/"
