import glob
import os

import numpy as np
import pandas as pd
import align_prepare_transcripts

# import nltk
# nltk.download('punkt_tab')

def seperate_by_timing(dataframe_source, file_path, name, split_file):
    dataframe = dataframe_source.copy()
    # print(len(dataframe))
    differences = dataframe['start_time'] - dataframe['end_time'].shift(periods=1)
    dataframe["time_delta"] = np.around(differences, 4).tolist()
    gaps = differences >= 15
    dfs = [g for _, g in dataframe.groupby(gaps.cumsum())]
    index = 1
    if split_file == True:
        for df in dfs:
            df = df.drop('start_time', axis=1)
            df = df[["participant", "content"]]
            df.to_csv(file_path + name +'-' + str(index) + '.txt', sep='\t', index=False)
            index += 1
    else:
        to_concat = []
        for df in dfs:
            df = df.drop('start_time', axis=1)
            df = df[["participant", "content"]]
            # df.to_csv(file_path + name + '-' + str(index) + '.txt', sep='\t', index=False)
            if len(df["participant"].unique())>=2:
                df = pd.concat([df,pd.DataFrame({"participant": ["TO_DROP_NULL"], "content": ["TO_DROP_NULL"]})], ignore_index=True)
                to_concat.append(df)
            index += 1
        try:
            dataframe = pd.concat(to_concat)
            dataframe.to_csv(file_path + name + '-' + str(index) + '.txt', sep='\t', index=False)
        except:
            x=0

def create_baseline(dataframe_source, file_path, name, split_file):
    dataframe = dataframe_source.copy()
    differences = dataframe['start_time'] - dataframe['end_time'].shift(periods=1)
    dataframe["time_delta"] = np.around(differences, 4).tolist()
    gaps = differences >= 15
    grouped = dataframe.groupby('speaker_type')
    for type, group in grouped:
        indexes = group.index
        group = group.sample(frac=1, ignore_index=True)
        group = group.set_index(indexes)
        dataframe.update(group)
    dfs = [g for _, g in dataframe.groupby(gaps.cumsum())]
    index = 1
    if split_file == True:
        for df in dfs:
            df = df.drop('start_time', axis=1)
            df = df[["participant", "content"]]
            df.to_csv(file_path + name + '-' + str(index) + '.txt', sep='\t', index=False)
            index += 1
    else:
        to_concat = []
        for df in dfs:
            df = df.drop('start_time', axis=1)
            df = df[["participant", "content"]]
            # df.to_csv(file_path + name + '-' + str(index) + '.txt', sep='\t', index=False)
            if len(df["participant"].unique()) >= 2:
                df = pd.concat([df, pd.DataFrame({"participant": ["TO_DROP_NULL"], "content": ["TO_DROP_NULL"]})],
                               ignore_index=True)
                to_concat.append(df)
            index += 1
        try:
            dataframe = pd.concat(to_concat)
            dataframe.to_csv(file_path + name + '-' + str(index) + '.txt', sep='\t', index=False)
        except:
            x=0

def seperate_by_snippet(location, split_file):
    isExist = os.path.exists(location + "/convos_by_tutor/")
    if not isExist:
       os.makedirs(location + '/convos_by_tutor/')
       os.makedirs(location + '/baseline/')
       os.makedirs(location + '/processed/')
       os.makedirs(location + '/baseline_processed/')

    dataframe = pd.read_csv(location + 'raw/full_data_processed_tagged_roles.csv')
    dataframe['speaker_type'] = dataframe['speaker_tagged_role'].astype(str)
    dataframe['speaker_ID'] = dataframe['speaker_ID'].astype(str)
    dataframe['participant'] = dataframe[['speaker_tagged_role', 'speaker_ID']].agg('_'.join, axis=1)
    # dataframe['participant'] = dataframe['participant'].apply(lambda x: x if "tutor" in x else "student" if "student" in x else "other")
    dataframe = dataframe.rename(columns={'utterance': "content"})
    grouped = dataframe.groupby('session_ID')

    for sesh_id, group in grouped:
        print(sesh_id)
        group = group.drop('session_ID', axis=1)
        tutor_id = str(group['tutor_ID'].iloc[0])
        date = str(group['session_date'].iloc[0])
        time = str(group['session_time'].iloc[0])
        group = group.drop('tutor_ID', axis=1)
        group = group.drop('session_date', axis=1)
        group = group.drop('session_time', axis=1)
        group.reset_index(drop=True, inplace=True)


        name = tutor_id + ")(" + date.replace("/", "-") + ")(" + time.replace(":", "-") + ")(" + sesh_id
        print(name)

        seperate_by_timing(group, location + "convos_by_tutor/", name, split_file)
        create_baseline(group, location + "baseline/", name, split_file)

    prepped_df = align_prepare_transcripts.prepare_transcripts(input_files=location+"convos_by_tutor/", output_file_directory=location+ "processed/",
                                           run_spell_check=False, input_as_directory=True, minwords=1)

    files = glob.glob(location + "processed/*.txt")
    chunks = [files[x:x + 100] for x in range(0, len(files), 100)]
    for index, chunk in enumerate(chunks):
        print(index)
        save_path = location + "processed/" + str(index)
        isExist = os.path.exists(save_path)
        if not isExist:
            os.makedirs(save_path)
        for file in chunk:
            os.rename(file, file.replace('processed', 'processed/' + str(index)))

    prepped_df = align_prepare_transcripts.prepare_transcripts(input_files=location + "baseline/",
                                           output_file_directory=location + "baseline_processed/",
                                           run_spell_check=False, input_as_directory=True, minwords=1)
    files = glob.glob(location + "baseline_processed/*.txt")
    chunks = [files[x:x + 100] for x in range(0, len(files), 100)]
    for index, chunk in enumerate(chunks):
        print(index)
        save_path = location + "baseline_processed/" + str(index)
        isExist = os.path.exists(save_path)
        if not isExist:
            os.makedirs(save_path)
        for file in chunk:
            os.rename(file, file.replace('processed', 'processed/' + str(index)))




def tag_others(location):
    dataframe = pd.read_csv(location + 'raw/full_data_processed_once.csv')

    print("num utterances")
    print(len(dataframe))
    print(dataframe.columns)

    non_student_IDs = pd.read_excel(location + "raw/student_id_not_found_in_achievement_updated_jan28.xlsx")
    # print(len(non_student_IDs))
    non_student_IDs = non_student_IDs[non_student_IDs['speaker_type'] != 'student']
    non_student_IDs = non_student_IDs['student_ID'].unique().tolist()

    dataframe["speaker_tagged_role"] = dataframe.apply(
        lambda x: "other" if x["speaker_ID"] in non_student_IDs and x["speaker_ID"] != x["tutor_ID"] else x[
            "speaker_type"], axis=1)

    print(dataframe.head(25))

    dataframe.to_csv(location + 'raw/full_data_processed_tagged_roles.csv', index=False)


def from_raw(location, raw_filename):
    pd.set_option('display.max_columns', None)

    # dataframe = pd.read_excel(location + "raw/" + raw_filename)
    dataframe = pd.read_csv(location + 'raw/' + raw_filename)
    print(dataframe.columns)

    dataframe = dataframe[['tutor_ID', 'speaker_ID', 'speaker_type', 'start_time', 'end_time', 'utterance', 'asr_confidence', 'session_ID', 'session_date', 'session_time']]

    # print(dataframe.head())

    repeats = []

    # #clean ASR
    print(len(dataframe))
    for i in range(1, len(dataframe)):
        if (dataframe.loc[i].utterance == dataframe.loc[i - 1].utterance) and (dataframe.loc[i].speaker_ID == dataframe.loc[i - 1].speaker_ID):
            repeats = repeats + [i]
        if (i%10000) == 0:
            print(i)


    print(repeats)
    print("dropping")
    dataframe.drop(repeats, inplace=True)
    # dataframe.reset_index(drop=True, inplace=True)
    print(dataframe.head(15).to_excel(location + 'raw/data_head_for_review.xlsx'))
    print(len(dataframe))
    print(len(set(dataframe['session_ID'])))
    print(len(set(dataframe['tutor_ID'])))

    print("saving")
    dataframe.to_csv(location + 'raw/full_data_processed_once.csv', index=False)

location = "C:/Users/Dorot/Emotive Computing Dropbox/Dorothea French/Linguistic_Alignment_and_Outcomes/data/Human_data_new/"
# location = "/projects/dofr2963/align_out_2/data/ASR_full/"
# raw_filename = "hat-utterances_2023-08-01-to-2024-06-11.csv"
# print("loading from " + location + raw_filename)
# from_raw(location, raw_filename)
# print("tagging others")
# tag_others(location)
print("delineating by snippet")
seperate_by_snippet(location, False)
