# nolint start

install.packages("psych")
install.packages("tidyr")
install.packages("ggplot2")
install.packages("mice")
install.packages("tidyverse")

################################################
# DATA CLEANING:
#   Participants data will be exluded if:
#   1. Q1 != "I Agree" (Consent)
#   2. Any failed attention check (Q6_8) != 5 || Q4_3 != 3
#
#   ??? Posthoc outlier removal beyond 95th percentile ???
#
# MISSING DATA:
#   Incase of data loss or corruption -
#     Missing data will be imputed using Multiple Imputation
#     using the mice R package
################################################
library(psych)
data_in <- read.csv("generated_survey_data.csv")

# Describe raw data
describe(data_in)
View(data_in)

# Clean condition 1
raw_data <- dataIn[(dataIn$`Q1` == "I Agree"), ]

describe(raw_data)
View(raw_data)


# Clean condition 2
clean_data <- raw_data[(raw_data$`Q6_8` == 5 & raw_data$`Q4_3` == 3), ]

describe(clean_data)
View(clean_data)

################################################
# STATISTICAL ANALYSIS:
#   T-test
#     H1: AF(scenario) vs PD
#     H2: AF(scenario) vs PT
#
#   Multiple Regression:`Q1`
#     H3: PD = b0 + b1(AF) + b2(PT) + b3(AF*PT)
#     Exploratory: PA = b0 + b1(AF) + b2(PD) + b3(AF*PD)
#
# Q5 - Percieved Danger(PD)
# Q6 - Percieved Transparency (PT)
# Q? - Percieved Transparency (PT)
# Q7 - Percieved Agency (PA)
#
# Manipulation check
#
################################################
library(tidyverse)

# Calculate means for each survey per participant
survey_means <- clean_data %>%
  rowwise() %>%
  mutate(
    Q5_mean = mean(c(Q5_1, Q5_2, Q5_3, Q5_4, Q5_5, Q5_6, Q5_7, Q5_8, Q5_9, Q5_10, Q5_11, Q5_12), na.rm = FALSE),
    Q6_mean = mean(c(Q6_1, Q6_2, Q6_3, Q6_4, Q6_5, Q6_6, Q6_7, Q6_8, Q6_9, Q6_10, Q6_11), na.rm = FALSE),
    Q7_mean = mean(c(Q7_1, Q7_2, Q7_3, Q7_4, Q7_5), na.rm = FALSE)
  )

describe(survey_means)
View(survey_means)

# Run t-tests
t.test(Q5_mean ~ Scenario, data = survey_means)
t.test(Q6_mean ~ Scenario, data = survey_means)

# Run Multiple Regression
regression_model <- lm(Q7_mean ~ Q5_mean + Q6_mean + Q5_mean * Q6_mean, data = survey_means)

# Plot results
ggplot(survey_means, aes(x = Scenario, y = Q5_mean, fill = Scenario)) +
  geom_boxplot() +
  labs(x = "Scenario", y = "Q5 Mean")

ggplot(survey_means, aes(x = Scenario, y = Q6_mean, fill = Scenario)) +
  geom_boxplot() +
  labs(x = "Scenario", y = "Q6 Mean")

# nolint end
