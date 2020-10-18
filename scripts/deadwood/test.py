import os
import utils
import time
import json
import math
import string

# ----------------------------------------------
# This script reads the json file with the merged
# data ("02_AllData.json") and the Data Structure
# Definition ("DSD.txt"), and creates a unified
# tabular view of all the data records.
# -----------------------------------------------

# Read the "ragged" data


data = utils.open_json('data/02_AllData.json')

new_series = ['Degree to which the legal framework(including customary law) guarantees women’s equal rights to land ownership and/or control(1=No evidence to 6=Highest levels of guarantees)',
              'Percentage of people with ownership or secure rights over agricultural land(out of total agricultural population), by sex',
              'Share of women among owners or rights-bearers of agricultural land',
              'Proportion of women who make their own informed decisions regarding contraceptive use (% of women aged 15-49 years)',
              'Proportion of women who make their own informed decisions regarding reproductive health care (% of women aged 15-49 years)',
              'Proportion of women who make their own informed decisions regarding sexual relations (% of women aged 15-49 years)',
              'Proportion of women who make their own informed decisions regarding sexual relations, contraceptive use and reproductive health care (% of women aged 15-49 years)',
              'Extent to which countries have laws and regulations that guarantee full and equal access to women and men aged 15 years and older to sexual and reproductive health care, information and education (% )',
              '(S.1.C.1) Extent to which countries have laws and regulations that guarantee full and equal access to women and men aged 15 years and older to sexual and reproductive health care, information and education: Component 1: Maternity Care (% )',
              '(S.4.C.10) Extent to which countries have laws and regulations that guarantee full and equal access to women and men aged 15 years and older to sexual and reproductive health care, information and education: Component 10: HIV Counselling and Test Services',
              '(S.4.C.11) Extent to which countries have laws and regulations that guarantee full and equal access to women and men aged 15 years and older to sexual and reproductive health care, information and education: Component 11: HIV Treatment and Care Services (% )',
              '(S.4.C.12) Extent to which countries have laws and regulations that guarantee full and equal access to women and men aged 15 years and older to sexual and reproductive health care, information and education: Component 12: HIV Confidentiality (% )',
              '(S.4.C.13) Extent to which countries have laws and regulations that guarantee full and equal access to women and men aged 15 years and older to sexual and reproductive health care, information and education: Component 13: HPV Vaccine (% )',
              '(S.1.C.2) Extent to which countries have laws and regulations that guarantee full and equal access to women and men aged 15 years and older to sexual and reproductive health care, information and education: Component 2: Life Saving Commodities (% )',
              '(S.1.C.3) Extent to which countries have laws and regulations that guarantee full and equal access to women and men aged 15 years and older to sexual and reproductive health care, information and education: Component 3: Abortion',
              '(S.1.C.4) Extent to which countries have laws and regulations that guarantee full and equal access to women and men aged 15 years and older to sexual and reproductive health care, information and education: Component 4: Post-Abortion Care (% )',
              '(S.2.C.5) Extent to which countries have laws and regulations that guarantee full and equal access to women and men aged 15 years and older to sexual and reproductive health care, information and education: Component 5: Contraceptive Services (% )',
              '(S.2.C.6) Extent to which countries have laws and regulations that guarantee full and equal access to women and men aged 15 years and older to sexual and reproductive health care, information and education: Component 6: Contraceptive Consent (% )',
              '(S.2.C.7) Extent to which countries have laws and regulations that guarantee full and equal access to women and men aged 15 years and older to sexual and reproductive health care, information and education: Component 7: Emergency Contraception (% )',
              '(S.3.C.8) Extent to which countries have laws and regulations that guarantee full and equal access to women and men aged 15 years and older to sexual and reproductive health care, information and education: Component 8: Sexuality Education Curriculum Laws (% )',
              '(S.3.C.9) Extent to which countries have laws and regulations that guarantee full and equal access to women and men aged 15 years and older to sexual and reproductive health care, information and education: Component 9: Sexuality Education Curriculum Topics (% )',
              '(S.1) Extent to which countries have laws and regulations that guarantee full and equal access to women and men aged 15 years and older to sexual and reproductive health care, information and education: Section 1: Maternity Care (% )',
              '(S.2) Extent to which countries have laws and regulations that guarantee full and equal access to women and men aged 15 years and older to sexual and reproductive health care, information and education: Section 2: Contraceptive and Family Planning (% )',
              '(S.3) Extent to which countries have laws and regulations that guarantee full and equal access to women and men aged 15 years and older to sexual and reproductive health care, information and education: Section 3: Sexuality Education (% )',
              '(S.4) Extent to which countries have laws and regulations that guarantee full and equal access to women and men aged 15 years and older to sexual and reproductive health care, information and education: Section 4: HIV and HPV (% )',
              'Cause-specific mortality rate(age-standardized). by leading causes of death',
              'Maternal mortality ratio - number of maternal deaths per 100, 000 live births',
              'Proportion of women of reproductive age(aged 15-49 years) who have their need for family planning satisfied with modern methods',
              'Share of Covid-19 death(percentage)',
              'Share of Covid-19 incidence(percentage)',
              'Number of deaths by neonatal causes of death, by sex',
              'Prevalence of overweight among children under 5',
              'Prevalence of stunting among children under 5',
              'Prevalence of wasting among children under 5',
              'Under-5 mortality rate, by sex',
              'Life expectancy at age 65 by sex and region',
              'Life expectancy at age 80 by sex and region',
              'Proportion of ever-partnered women and girls subjected to violence by a current or former intimate partner in a lifetime, by type of violence, by age (% )',
              'Countries with equal ownership rights to immovable property(1=Yes, 0=No)',
              'Countries with equal rights for children to inherit assets from parents(1=Yes, 0=No)',
              'Countries with equal inheritance rights for female and male surviving spouses(1=Yes, 0=No)',
              'Countries with law that grant spouses equal administrative authority over assets during marriage(1=Yes, 0=No)',
              'Countries with law that provide for the valuation of nonmonetary contributions(1=Yes, 0=No)',
              'Can a woman get a job in the same way as a man? (1=Yes, 0=No)',
              'Can a woman obtain a judgment of divorce in the same way as a man? (1=Yes, 0=No)',
              'Can a woman register a business in the same way as a man? (1=Yes, 0=No)',
              'Can a woman travel outside her home in the same way as a man? (1=Yes, 0=No)',
              'Do men and women have equal ownership rights to immovable property? (1=Yes, 0=No)',
              'Does the law mandate equal remuneration for work of equal value? (1=Yes, 0=No)',
              'Is the mandatory retirement age for men and women equal? (1=Yes, 0=No)',
              'Is there paid parental leave? (1=Yes, 0=No)',
              'WBL index',
              'Hours of time spent on unpaid domestic and care work, by sex and ethnicity',
              'Average hourly earnings of employed population aged 15 years or older, by years of schooling and ethnicity',
              'Percentage of currently married or in union women and men employed in the 12 months before the survey who worked for cash and in-kind payment',
              'Percentage of currently married or in union women and men employed in the 12 months before the survey who worked for cash only',
              'Percentage of currently married or in union women and men employed in the 12 months before the survey who worked for in-kind payment only',
              'Percentage of currently married or in union women and men employed in the 12 months before the survey who worked unpaid',
              'Proportion of women and men who disagree with the statement “it\'s perfectly acceptable for any woman in your family to have a paid job outside the home if she wants one”',
              'Does the law mandate equal remuneration for work of equal value(ILO convention 100)? (1=Yes, 0=No)',
              'Does the law prohibit discrimination in employment based on gender(ILO convention 111)? (1=Yes, 0=No)'
              ]

print(data[0])
check = []
for record in data:
    if record['SERIES_DESC'] in new_series:
        check.append(record['NARRATIVE_ID'])
        check = list(set(check))
    else:
        continue

print(check)
