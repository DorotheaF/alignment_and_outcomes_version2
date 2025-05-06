import os
import pandas as pd



def consolidate_files(location):
    print("looking in folder " + location)
    folders = [x[0] for x in os.walk(location)]
    print(folders)
    folders = [s for s in folders if 'bert' not in s and 'fasttext' not in s and 'lexsyn' not in s]
    print(folders)
    print("before loop")
    i = 0
    dataframes = []
    for folder in folders[1:len(folders)]:
        # folder_frame = pd.read_csv(folder+'/merged-lag1-ngram2-noStan-noDups-sd3-n1.csv')
        folder_frame = pd.read_csv(folder+'/merged-lag1-ngram2-noStan-noDups.csv')
        bert_frame = pd.read_csv(folder+'/bert/semantic_alignment_bert-base-uncased_lag1.csv')
        folder_frame['bert_semantic'] = bert_frame['bert-base-uncased_cosine_similarity']
        folder_frame[['tutor_id', 'date', 'session_time', 'condition_info']] = folder_frame['source_file'].str.split(r'\)\(', expand=True, n=3)
        folder_frame['condition_info'] = folder_frame['condition_info'].apply(lambda x: x.rsplit("-",1)[0])
        transcript_df_groups = folder_frame.groupby('condition_info')
        for label, transcript in transcript_df_groups:
            transcript.reset_index(inplace=True)
            transcript['speaker'] = transcript['participant'].shift(-1)
            # transcript['speaker_id'] = transcript['speaker'].apply(lambda x: x.split("_")[1])
            split_indices = [-1] + transcript.index[transcript['participant'] == 'TO_DROP_NULL'].tolist() + [len(transcript)]
            print(split_indices)

            sub_frames = [transcript[split_indices[i] + 1:split_indices[i + 1]]
                          for i in range(len(split_indices) - 1)]

            for snippet_num, subframe in enumerate(sub_frames):
                subframe['condition_info'] = subframe['condition_info'].apply(lambda x: x + "_" + str(snippet_num))
                subframe = subframe[:-1]
                subframe.reset_index(drop=True, inplace=True)
                subframe.index += 1
                subframe['time'] = subframe.index
                sub_frames[snippet_num] = subframe
            print(len(sub_frames))

            reset_transcript = pd.concat(sub_frames)
            dataframes.append(reset_transcript)

    mega_dataframe = pd.concat(dataframes)
    mega_dataframe.rename(columns={
                                   # 'BERT_BERT-BASE-UNCASED_COSINE_SIMILARITY': 'bert_semantic',
                                   # 'lemma_fasttext-wiki-news-300_cosine_similarity': 'fasttext_semantic',
                                   'pos_tok2_cosine': 'syntax','lexical_lem1_cosine': 'lexical',
                                   'lexical_lem2_cosine': 'lexical_bigram',
                                   "content": "previous_utterance",
                                   "content2": "content",
                                   "participant": "prev_speaker"}, inplace=True)
    print(mega_dataframe.columns)
    mega_dataframe = mega_dataframe[["condition_info", "time", "speaker", "prev_speaker", "content", "previous_utterance", "utterance_length2", "lexical", "lexical_bigram", "syntax", "bert_semantic",  "tutor_id", "date", "session_time"]] #"fasttext_semantic",
    mega_dataframe.to_csv(location + "merged_all_alignment_incomplete.csv", index= False)
    print("saved to merged")




def sum_by_student_and_tutor(location, level="none"):
    alignment_full = pd.read_csv( location +  '/merged_all_alignment.csv')

    partner_pair_list = [["student", "tutor"]]
    for duo in partner_pair_list:
        duo.append(duo[0])
        for i in range(0, 2):
            speaker = duo[i+1]
            prev_speaker = duo[i]
            print("summing by" + speaker)
            alignment = alignment_full[alignment_full['speaker'].str.contains(speaker + '.*')]
            alignment.reset_index(drop=True, inplace=True)
            alignment = alignment[alignment['prev_speaker'].str.contains(prev_speaker + '.*')]
            alignment.reset_index(drop=True, inplace=True)
            alignment['partner_pair'] =  alignment[['speaker', 'prev_speaker']].agg('>'.join, axis=1)
            if level == "snippet":
                alignment['partner_pair'] = alignment[['partner_pair', 'condition_info']].agg('>'.join, axis=1)
            elif level == "transcript":
                alignment['partner_pair'] = alignment[['partner_pair', 'condition_info']].agg('>'.join, axis=1)
                alignment['partner_pair'] = alignment['partner_pair'].apply(lambda x: x.rsplit("_",1)[0])

            alignment = alignment[["partner_pair", "utterance_length2", "lexical", "lexical_bigram", "syntax", "bert_semantic",  "tutor_id"]] #"fasttext_semantic",
            print(alignment.columns)

            alignment[["utterance_length2", "lexical", "lexical_bigram", "syntax", "bert_semantic", "tutor_id"]] = alignment[  #"fasttext_semantic",
                ["utterance_length2", "lexical", "lexical_bigram", "syntax", "bert_semantic", "tutor_id"]].apply(pd.to_numeric)  #"fasttext_semantic",

            summed_rows = []
            group_by_pair = alignment.groupby('partner_pair')
            for pair, group in group_by_pair:
                row_sum = group.sum(numeric_only=True)/len(group)
                row_sum['partner_pair'] = pair
                row_sum['num_utt'] = len(group)
                summed_rows.append(row_sum)

            # print(summed_rows)
            summed_by_student_to_tutor = pd.concat(summed_rows, axis=1).T
            # summed_by_student_to_tutor.set_index('partner_pair', inplace=True)
            # summed_by_student_to_tutor = pd.DataFrame(summed_by_student_to_tutor)
            filename = location + '/alignment_summed_by_' + speaker  + '_to_' + prev_speaker +'_no_outcomes.xlsx'
            if level == "snippet":
                filename = filename.replace('.xlsx', '_snippet.xlsx')
            elif level == "transcript":
                filename = filename.replace('.xlsx', '_transcript.xlsx')

            summed_by_student_to_tutor.to_excel(filename)
            print("saved " + speaker + '_to_' + prev_speaker)



# location = "C:/Users/Dorot/Emotive Computing Dropbox/Dorothea French/Linguistic_Alignment_and_Outcomes/data/ASR_full/by_tutor_metrics/"
location = "/projects/dofr2963/align_out_2/data/ASR_full/by_tutor_metrics/"
consolidate_files(location)
location = "/projects/dofr2963/align_out_2/data/ASR_full/by_tutor_metrics_baseline/"
consolidate_files(location)
# sum_by_student_and_tutor(location)
# sum_by_student_and_tutor(location, "snippet")
# sum_by_student_and_tutor(location, "transcript")
