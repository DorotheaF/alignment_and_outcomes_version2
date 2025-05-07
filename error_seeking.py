import pandas as pd


def from_raw():
    pd.set_option('display.max_columns', None)

    # dataframe = pd.read_excel(location + "raw/" + raw_filename)
    dataframe = pd.read_csv("C:/Users/Dorot/Emotive Computing Dropbox/Dorothea French/Linguistic_Alignment_and_Outcomes/data/ASR_full/by_tutor_metrics/merged_all_alignment.csv")
    print(len(dataframe))
    print(dataframe.columns)

    dataframe_old = pd.read_csv("C:/Users/Dorot/OneDrive/Documents/Research Data/linguistic_alignment_and_outcomes/full_data/by_tutor_metrics/aggregated_alignment_2.csv")
    print(len(dataframe_old))
    print(dataframe_old.columns)

    mini_frame = dataframe[dataframe['condition_info'].str.contains("00a5b9cb-5b7a-4c7b-87df-98b3cbfb9fee")]
    mini_frame_old = dataframe_old[dataframe_old['condition_info'].str.contains("00a5b9cb-5b7a-4c7b-87df-98b3cbfb9fee")]

    mini_frame.to_csv("C:/Users/Dorot/Emotive Computing Dropbox/Dorothea French/Linguistic_Alignment_and_Outcomes/data/ASR_full/test_data/new.csv")
    mini_frame_old.to_csv("C:/Users/Dorot/Emotive Computing Dropbox/Dorothea French/Linguistic_Alignment_and_Outcomes/data/ASR_full/test_data/old.csv")



from_raw()



