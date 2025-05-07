
library(readxl)
library(lme4)
library(lmerTest)
library(sjPlot)
library(blme)
library(reshape2)
library(ggplot2)
library(DescTools)
library(emmeans)
library(tidyr)
library(dplyr)
library(gt)

# tutors_alignment_filename <- "C:/Users/Dorot/OneDrive/Documents/Research Data/linguistic_alignment_and_outcomes/full_data/by_tutor_metrics/alignment_summed_by_tutor_to_student_no_outcomes_num.xlsx"
# students_alignment_filename <- "C:/Users/Dorot/OneDrive/Documents/Research Data/linguistic_alignment_and_outcomes/full_data/by_tutor_metrics/alignment_summed_by_student_no_outcomes_to_tutor_num.xlsx"
# 
# tutors_alignment_filename_baseline <- "C:/Users/Dorot/OneDrive/Documents/Research Data/linguistic_alignment_and_outcomes/full_data/by_tutor_metrics_baseline/alignment_summed_by_tutor_to_student_no_outcomes_baseline.xlsx"
# students_alignment_filename_baseline <- "C:/Users/Dorot/OneDrive/Documents/Research Data/linguistic_alignment_and_outcomes/full_data/by_tutor_metrics_baseline/alignment_summed_by_student_no_outcomes_to_tutor_baseline.xlsx"


tutors_alignment_filename <- "C:/Users/Dorot/Emotive Computing Dropbox/Dorothea French/Linguistic_Alignment_and_Outcomes/data/ASR_full/by_tutor_metrics/alignment_summed_by_tutor_to_student_no_outcomes_snippet.xlsx"
students_alignment_filename <- "C:/Users/Dorot/Emotive Computing Dropbox/Dorothea French/Linguistic_Alignment_and_Outcomes/data/ASR_full/by_tutor_metrics/alignment_summed_by_student_to_tutor_no_outcomes_snippet.xlsx"

# tutors_alignment_filename_baseline <- "C:/Users/Dorot/Emotive Computing Dropbox/Dorothea French/Linguistic_Alignment_and_Outcomes/data/ASR_full/by_tutor_metrics_baseline/alignment_summed_by_tutor_to_student_no_outcomes_baseline.xlsx"
# students_alignment_filename_baseline <- "C:/Users/Dorot/Emotive Computing Dropbox/Dorothea French/Linguistic_Alignment_and_Outcomes/data/ASR_full/by_tutor_metrics_baseline/alignment_summed_by_student_no_outcomes_to_tutor_baseline.xlsx"



alignment_tutors_gold <- read_excel(tutors_alignment_filename)
alignment_tutors_gold$student_ID <- sapply(strsplit(sapply(strsplit(alignment_tutors_gold$partner_pair, ">"), `[`, 2), "_"), `[`, 2)

alignment_students_gold <- read_excel(students_alignment_filename)
alignment_students_gold$student_ID <- sapply(strsplit(sapply(strsplit(alignment_students_gold$partner_pair, "_"), `[`, 2), ">"), `[`, 1)

student_outcomes_filename <- "C:/Users/Dorot/OneDrive/Documents/Research Data/linguistic_alignment_and_outcomes/full_data/outcomes/Student_Achievement_Intercept_Slope_10_23_2024.csv"
outcomes <-read.csv(student_outcomes_filename)
outcomes <- outcomes %>% distinct(tutor, student_ID, .keep_all = TRUE)

alignment_comparison_all_students <- merge(alignment_students_gold, alignment_tutors_gold, by = c("tutor", "student_ID"), suffixes = c("_student", "_tutor"))

alignment_comparison_with_outcomes <- merge(alignment_comparison_all_students, outcomes,  by = c("tutor", "student_ID"), all.x = FALSE, all.y = FALSE)


alignment_comparison_without_outcomes <- anti_join(alignment_comparison_all_students, alignment_comparison_with_outcomes, by = c("tutor", "student_ID"))



(length(unique(alignment_comparison_all_students[["student_ID"]])))
(length(unique(alignment_comparison_with_outcomes[["student_ID"]])))
(length(unique(alignment_comparison_without_outcomes[["student_ID"]])))

((mean(alignment_comparison_all_students$num_utt_student)+ mean(alignment_comparison_all_students$num_utt_tutor))/2)

((mean(alignment_comparison_with_outcomes$num_utt_student) + mean(alignment_comparison_with_outcomes$num_utt_tutor))/2)

(mean(alignment_comparison_without_outcomes$num_utt_student) + mean(alignment_comparison_without_outcomes$num_utt_tutor))/2



vars_stu <- c( "syntax_student", "lexical_student")
alignment_comparison_all_students[vars_stu] <- DescTools::Winsorize(alignment_comparison_all_students[vars_stu], val = quantile(alignment_comparison_all_students[vars_stu], probs = c(0.0, 0.98), na.rm = T))
alignment_comparison_with_outcomes[vars_stu] <- DescTools::Winsorize(alignment_comparison_with_outcomes[vars_stu], val = quantile(alignment_comparison_with_outcomes[vars_stu], probs = c(0.0, 0.98), na.rm = T))
alignment_comparison_without_outcomes[vars_stu] <- DescTools::Winsorize(alignment_comparison_without_outcomes[vars_stu], val = quantile(alignment_comparison_without_outcomes[vars_stu], probs = c(0.0, 0.98), na.rm = T))
alignment_comparison_all_students["bert_semantic_student"] <- DescTools::Winsorize(alignment_comparison_all_students["bert_semantic_student"], val = quantile(alignment_comparison_all_students["bert_semantic_tutor"], probs = c(0.0, 0.99), na.rm = T))
alignment_comparison_with_outcomes["bert_semantic_student"] <- DescTools::Winsorize(alignment_comparison_with_outcomes["bert_semantic_student"], val = quantile(alignment_comparison_with_outcomes["bert_semantic_tutor"], probs = c(0.0, 0.99), na.rm = T))
alignment_comparison_without_outcomes["bert_semantic_student"] <- DescTools::Winsorize(alignment_comparison_without_outcomes["bert_semantic_student"], val = quantile(alignment_comparison_without_outcomes["bert_semantic_tutor"], probs = c(0.0, 0.99), na.rm = T))

vars_stu <- c( "syntax_student", "lexical_student", "bert_semantic_student")
tab_corr(alignment_comparison_all_students[vars_stu], triangle = "upper")
tab_corr(alignment_comparison_with_outcomes[vars_stu], triangle = "upper")
tab_corr(alignment_comparison_without_outcomes[vars_stu], triangle = "upper")


vars_tut <- c( "syntax_tutor", "lexical_tutor")
alignment_comparison_all_students[vars_tut] <- DescTools::Winsorize(alignment_comparison_all_students[vars_tut], val = quantile(alignment_comparison_all_students[vars_tut], probs = c(0.0, 0.98), na.rm = T))
alignment_comparison_with_outcomes[vars_tut] <- DescTools::Winsorize(alignment_comparison_with_outcomes[vars_tut], val = quantile(alignment_comparison_with_outcomes[vars_tut], probs = c(0.0, 0.98), na.rm = T))
alignment_comparison_without_outcomes[vars_tut] <- DescTools::Winsorize(alignment_comparison_without_outcomes[vars_tut], val = quantile(alignment_comparison_without_outcomes[vars_tut], probs = c(0.0, 0.98), na.rm = T))

alignment_comparison_all_students["bert_semantic_tutor"] <- DescTools::Winsorize(alignment_comparison_all_students["bert_semantic_tutor"], val = quantile(alignment_comparison_all_students["bert_semantic_tutor"], probs = c(0.0, 0.99), na.rm = T))
alignment_comparison_with_outcomes["bert_semantic_tutor"] <- DescTools::Winsorize(alignment_comparison_with_outcomes["bert_semantic_tutor"], val = quantile(alignment_comparison_with_outcomes["bert_semantic_tutor"], probs = c(0.0, 0.99), na.rm = T))
alignment_comparison_without_outcomes["bert_semantic_tutor"] <- DescTools::Winsorize(alignment_comparison_without_outcomes["bert_semantic_tutor"], val = quantile(alignment_comparison_without_outcomes["bert_semantic_tutor"], probs = c(0.0, 0.99), na.rm = T))

vars_tut <- c( "syntax_tutor", "lexical_tutor", "bert_semantic_tutor")
tab_corr(alignment_comparison_all_students[vars_tut], triangle = "lower")
tab_corr(alignment_comparison_with_outcomes[vars_tut], triangle = "lower")
tab_corr(alignment_comparison_without_outcomes[vars_tut], triangle = "lower")



cor(alignment_comparison_all_students$syntax_student, alignment_comparison_all_students$syntax_tutor)
cor(alignment_comparison_all_students$lexical_student, alignment_comparison_all_students$lexical_tutor)
cor(alignment_comparison_all_students$bert_semantic_student, alignment_comparison_all_students$bert_semantic_tutor)

cor(alignment_comparison_with_outcomes$syntax_student, alignment_comparison_with_outcomes$syntax_tutor)
cor(alignment_comparison_with_outcomes$lexical_student, alignment_comparison_with_outcomes$lexical_tutor)
cor(alignment_comparison_with_outcomes$bert_semantic_student, alignment_comparison_with_outcomes$bert_semantic_tutor)

cor(alignment_comparison_without_outcomes$syntax_student, alignment_comparison_without_outcomes$syntax_tutor)
cor(alignment_comparison_without_outcomes$lexical_student, alignment_comparison_without_outcomes$lexical_tutor)
cor(alignment_comparison_without_outcomes$bert_semantic_student, alignment_comparison_without_outcomes$bert_semantic_tutor)


hist(alignment_comparison_all_students$syntax_student, col=rgb(1, 0, 0, alpha=0.5), breaks = 40, main="Student Syntactic Alignment", xlab = "Bigram Tokenized Syntactic Alignment", xlim = c(0,.4), ylim = c(0,1000))
hist(alignment_comparison_without_outcomes$syntax_student, col=rgb(0, 1, 0, alpha=0.5),  breaks = 40,add=TRUE)
hist(alignment_comparison_with_outcomes$syntax_student, col=rgb(0, 0, 1, alpha=0.5),  breaks = 40,add=TRUE)
legend("topright", legend=c("All", "Sans Outcomes", "Outcomes"), fill=c(rgb(1, 0, 0, alpha=0.5), rgb(0, 1, 0, alpha=0.5), rgb(0, 0, 1, alpha=0.5)))

hist(alignment_comparison_all_students$syntax_tutor, col=rgb(1, 0, 0, alpha=0.5), breaks = 40, main="Tutor Syntactic Alignment", xlab = "Bigram Tokenized Syntactic Alignment", xlim = c(0,.4), ylim = c(0,1000))
hist(alignment_comparison_without_outcomes$syntax_tutor, col=rgb(0, 1, 0, alpha=0.5),  breaks = 40,add=TRUE)
hist(alignment_comparison_with_outcomes$syntax_tutor, col=rgb(0, 0, 1, alpha=0.5),  breaks = 20,add=TRUE)
legend("topright", legend=c("All", "Sans Outcomes", "Outcomes"), fill=c(rgb(1, 0, 0, alpha=0.5), rgb(0, 1, 0, alpha=0.5), rgb(0, 0, 1, alpha=0.5)))


hist(alignment_comparison_all_students$lexical_student, col=rgb(1, 0, 0, alpha=0.5), breaks = 40, main="Student Lexical Alignment", xlab = "Unigram Lemmatized Lexical Alignment", xlim = c(0,.4), ylim = c(0,1000))
hist(alignment_comparison_without_outcomes$lexical_student, col=rgb(0, 1, 0, alpha=0.5),  breaks = 40,add=TRUE)
hist(alignment_comparison_with_outcomes$lexical_student, col=rgb(0, 0, 1, alpha=0.5),  breaks = 40,add=TRUE)
legend("topright", legend=c("All", "Sans Outcomes", "Outcomes"), fill=c(rgb(1, 0, 0, alpha=0.5), rgb(0, 1, 0, alpha=0.5), rgb(0, 0, 1, alpha=0.5)))

hist(alignment_comparison_all_students$lexical_tutor, col=rgb(1, 0, 0, alpha=0.5), breaks = 40, main="Tutor Lexical Alignment", xlab = "Unigram Lemmatized Lexical Alignment", xlim = c(0,.4), ylim = c(0,1000))
hist(alignment_comparison_without_outcomes$lexical_tutor, col=rgb(0, 1, 0, alpha=0.5),  breaks = 40,add=TRUE)
hist(alignment_comparison_with_outcomes$lexical_tutor, col=rgb(0, 0, 1, alpha=0.5),  breaks = 20,add=TRUE)
legend("topright", legend=c("All", "Sans Outcomes", "Outcomes"), fill=c(rgb(1, 0, 0, alpha=0.5), rgb(0, 1, 0, alpha=0.5), rgb(0, 0, 1, alpha=0.5)))

hist(alignment_comparison_all_students$bert_semantic_student, col=rgb(1, 0, 0, alpha=0.5), breaks = 40, main="Student Semantic Alignment", xlab = "Cosine Semantic Alignment", xlim = c(0,.8), ylim = c(0,1000))
hist(alignment_comparison_without_outcomes$bert_semantic_student, col=rgb(0, 1, 0, alpha=0.5),  breaks = 40,add=TRUE)
hist(alignment_comparison_with_outcomes$bert_semantic_student, col=rgb(0, 0, 1, alpha=0.5),  breaks = 40,add=TRUE)
legend("topright", legend=c("All", "Sans Outcomes", "Outcomes"), fill=c(rgb(1, 0, 0, alpha=0.5), rgb(0, 1, 0, alpha=0.5), rgb(0, 0, 1, alpha=0.5)))

hist(alignment_comparison_all_students$bert_semantic_tutor, col=rgb(1, 0, 0, alpha=0.5), breaks = 40, main="Tutor Semantic Alignment", xlab = "Cosine Semantic Alignment", xlim = c(0,.8), ylim = c(0,1000))
hist(alignment_comparison_without_outcomes$bert_semantic_tutor, col=rgb(0, 1, 0, alpha=0.5),  breaks = 40,add=TRUE)
hist(alignment_comparison_with_outcomes$bert_semantic_tutor, col=rgb(0, 0, 1, alpha=0.5),  breaks = 40,add=TRUE)
legend("topright", legend=c("All", "Sans Outcomes", "Outcomes"), fill=c(rgb(1, 0, 0, alpha=0.5), rgb(0, 1, 0, alpha=0.5), rgb(0, 0, 1, alpha=0.5)))

hist(alignment_comparison_all_students$num_utt_tutor, col=rgb(1, 0, 0, alpha=0.5), breaks = 200, main="Tutor Number Utterances")
hist(alignment_comparison_without_outcomes$num_utt_tutor, col=rgb(0, 1, 0, alpha=0.5),  breaks = 200,add=TRUE)
hist(alignment_comparison_with_outcomes$num_utt_tutor, col=rgb(0, 0, 1, alpha=0.5),  breaks = 200,add=TRUE)
legend("topright", legend=c("All", "Sans Outcomes", "Outcomes"), fill=c(rgb(1, 0, 0, alpha=0.5), rgb(0, 1, 0, alpha=0.5), rgb(0, 0, 1, alpha=0.5)))


hist(alignment_comparison_all_students$num_utt_tutor, col=rgb(1, 0, 0, alpha=0.5), breaks = 200, main="Tutor Number Utterances (zoom in)", xlim = c(0,500))
hist(alignment_comparison_without_outcomes$num_utt_tutor, col=rgb(0, 1, 0, alpha=0.5),  breaks = 200,add=TRUE)
hist(alignment_comparison_with_outcomes$num_utt_tutor, col=rgb(0, 0, 1, alpha=0.5),  breaks = 200,add=TRUE)
legend("topright", legend=c("All", "Sans Outcomes", "Outcomes"), fill=c(rgb(1, 0, 0, alpha=0.5), rgb(0, 1, 0, alpha=0.5), rgb(0, 0, 1, alpha=0.5)))


no_dup_id <- alignment_comparison_all_students %>% distinct( student_ID, .keep_all = TRUE)


tab_corr(no_dup_id[vars_tut], triangle = "lower")
tab_corr(no_dup_id[vars_stu], triangle = "upper")


library(data.table)
random_subset <- no_dup_id[sample(nrow(no_dup_id),1693),]


tab_corr(random_subset[vars_tut], triangle = "lower")
tab_corr(random_subset[vars_stu], triangle = "upper")
mean(random_subset$num_utts_student)

min_length_with_outcomes <- subset(alignment_comparison_with_outcomes, alignment_comparison_with_outcomes$num_utts_tutor >= 50)

plot(alignment_comparison_with_outcomes$syntax_student,alignment_comparison_with_outcomes$bert_semantic_student, xlim = c(0,.4), ylim= c(0,.7), main= "With Outcomes")
plot(alignment_comparison_all_students$syntax_student,alignment_comparison_all_students$bert_semantic_student, xlim = c(0,.4), ylim= c(0,.7), main= "All Pairs")
plot(alignment_comparison_without_outcomes$syntax_student,alignment_comparison_without_outcomes$bert_semantic_student, xlim = c(0,.4), ylim= c(0,.7), main= "Without Outcomes")
plot(min_length_with_outcomes$syntax_student,min_length_with_outcomes$bert_semantic_student, xlim = c(0,.4), ylim= c(0,.7), main= "With Outcomes and num utts >=50")

plot(alignment_comparison_with_outcomes$lexical_student,alignment_comparison_with_outcomes$bert_semantic_student, xlim = c(0,.4), ylim= c(0,.7), main= "With Outcomes")
plot(alignment_comparison_all_students$lexical_student,alignment_comparison_all_students$bert_semantic_student, xlim = c(0,.4), ylim= c(0,.7), main= "All Pairs")
plot(alignment_comparison_without_outcomes$lexical_student,alignment_comparison_without_outcomes$bert_semantic_student, xlim = c(0,.4), ylim= c(0,.7), main= "Without Outcomes")
plot(min_length_with_outcomes$lexical_student,min_length_with_outcomes$bert_semantic_student, xlim = c(0,.4), ylim= c(0,.7), main= "With Outcomes and num utts >=50")

plot(alignment_comparison_with_outcomes$lexical_student,alignment_comparison_with_outcomes$lexical_tutor, xlim = c(0,.4), ylim= c(0,.7), main= "With Outcomes")


