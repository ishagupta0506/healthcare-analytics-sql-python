# Hospital Patient Analytics — Query Results & Business Insights (Final)

**Database:** hospital.db | **Table:** hospital_patients | **Total Records:** 55,500  
**Tools:** Python · pandas · SQLite3 | **SQL Files:** queries.sql · advanced_queries.sql  
**Note:** This is a synthetic educational dataset. All observations are based strictly on the data contained within `hospital.db`. No causal claims or real-world comparisons are made unless explicitly supported by the data.

---

# PART 1 — Core Queries (queries.sql)

---

# Query 1: Total Patient Count

## Purpose
Counts the total number of patient records in the dataset to establish the baseline population size for all further analysis.

## SQL Query

```sql
SELECT COUNT(*) AS total_patients
FROM hospital_patients;
```

## Key Results

| total_patients |
|---|
| 55,500 |

## Business Insight
The dataset contains 55,500 patient records across 20 columns. This is the denominator used in all percentage-based calculations throughout this report. All subsequent analyses are scoped to this population.

## SQL Concepts Used
- `COUNT`
- `SELECT`

---

# Query 2: Billing Statistics (Average, Min, Max)

## Purpose
Summarizes the billing amount distribution across all patients to understand the financial spread across the dataset.

## SQL Query

```sql
SELECT
    ROUND(AVG(billing_amount), 2) AS avg_billing,
    ROUND(MIN(billing_amount), 2) AS min_billing,
    ROUND(MAX(billing_amount), 2) AS max_billing
FROM hospital_patients;
```

## Key Results

| avg_billing | min_billing | max_billing |
|---|---|---|
| $25,539.32 | -$2,008.49 | $52,764.28 |

## Business Insight
The average billing amount is $25,539.32. The minimum value of -$2,008.49 is a data quality flag — negative billing amounts are not logically valid in this context and should be investigated before any financial reporting. The cause of this negative value cannot be determined from the available data. The maximum billing of $52,764.28 represents the upper bound of the distribution in this dataset. The spread between minimum and maximum ($54,772.77) indicates high variability in billing across patients.

## SQL Concepts Used
- `AVG`, `MIN`, `MAX`
- `ROUND`

---

# Query 3: Average Length of Stay

## Purpose
Calculates how long patients stay in the hospital on average — a key operational metric for bed utilisation and resource planning.

## SQL Query

```sql
SELECT ROUND(AVG(length_of_stay), 1) AS avg_stay_days
FROM hospital_patients;
```

## Key Results

| avg_stay_days |
|---|
| 15.5 |

## Business Insight
The average length of stay across all 55,500 records is 15.5 days. This figure is derived directly from the `length_of_stay` column in the dataset. The dataset does not contain facility-type or care-setting metadata, so no comparison to external benchmarks can be made from this data alone. To explore the relationship between length of stay and billing, this metric can be cross-referenced with `billing_amount` using a JOIN or correlation analysis.

## SQL Concepts Used
- `AVG`, `ROUND`

---

# Query 4: Patients by Medical Condition

## Purpose
Breaks down the patient population by medical condition to identify the distribution of diagnoses in this dataset.

## SQL Query

```sql
SELECT medical_condition,
       COUNT(*) AS total_patients
FROM hospital_patients
GROUP BY medical_condition
ORDER BY total_patients DESC;
```

## Key Results

| medical_condition | total_patients |
|---|---|
| Arthritis | 9,308 |
| Diabetes | 9,304 |
| Hypertension | 9,245 |
| Obesity | 9,231 |
| Cancer | 9,227 |
| Asthma | 9,185 |

## Business Insight
All six conditions are distributed nearly equally, ranging from 9,185 (Asthma) to 9,308 (Arthritis) — a difference of only 123 patients across the full population. This near-uniform distribution across conditions is a characteristic of the dataset's structure. Arthritis is the most frequently recorded condition, though the margin is small. No conclusion about relative disease prevalence in any real population can be drawn from this distribution.

## SQL Concepts Used
- `COUNT`, `GROUP BY`, `ORDER BY`

---

# Query 5: Patients by Age Group

## Purpose
Segments patients into age bands to understand the demographic distribution of the dataset.

## SQL Query

```sql
SELECT age_group,
       COUNT(*) AS total_patients
FROM hospital_patients
GROUP BY age_group
ORDER BY age_group;
```

## Key Results

| age_group | total_patients |
|---|---|
| 0–18 | 888 |
| 19–35 | 13,644 |
| 36–60 | 20,598 |
| 60+ | 20,370 |

## Business Insight
Patients aged 36–60 and 60+ together account for 73.8% of all records. The 0–18 group represents only 1.6% of the dataset (888 patients). The dataset does not contain metadata describing the facility type or patient selection methodology, so the reason for this age distribution cannot be determined from the data alone. What the data shows is that the vast majority of records belong to adult patients aged 36 and above.

## SQL Concepts Used
- `COUNT`, `GROUP BY`, `ORDER BY`

---

# Query 6: Patients by Admission Type

## Purpose
Analyzes how patients enter the hospital across three admission categories to understand the operational demand mix in the dataset.

## SQL Query

```sql
SELECT admission_type,
       COUNT(*) AS total_patients
FROM hospital_patients
GROUP BY admission_type
ORDER BY total_patients DESC;
```

## Key Results

| admission_type | total_patients |
|---|---|
| Elective | 18,655 |
| Urgent | 18,576 |
| Emergency | 18,269 |

## Business Insight
The three admission types — Elective, Urgent, and Emergency — are distributed almost equally at approximately 33% each (18,655 / 18,576 / 18,269). The difference between the highest and lowest group is 386 patients. This near-equal split is a structural characteristic of this dataset. No comparison to admission distributions in external datasets is made here, as this dataset does not contain information about how records were sampled.

## SQL Concepts Used
- `COUNT`, `GROUP BY`, `ORDER BY`

---

# Query 7: Patients by Gender

## Purpose
Examines the gender distribution of patients to assess demographic balance within the dataset.

## SQL Query

```sql
SELECT gender,
       COUNT(*) AS total_patients
FROM hospital_patients
GROUP BY gender
ORDER BY total_patients DESC;
```

## Key Results

| gender | total_patients |
|---|---|
| Male | 27,774 |
| Female | 27,726 |

## Business Insight
The dataset contains 27,774 male and 27,726 female patients — a difference of 48 records (0.09%). The gender distribution is effectively balanced. This means any gender-based segmentation analysis will have comparable sample sizes for both groups, which supports reliable group-level comparisons within this dataset.

## SQL Concepts Used
- `COUNT`, `GROUP BY`, `ORDER BY`

---

# Query 8: Patients by Year

## Purpose
Tracks admission volume across years to identify year-level patterns in the dataset.

## SQL Query

```sql
SELECT admission_year,
       COUNT(*) AS total_patients
FROM hospital_patients
GROUP BY admission_year
ORDER BY admission_year;
```

## Key Results

| admission_year | total_patients |
|---|---|
| 2019 | 7,387 |
| 2020 | 11,285 |
| 2021 | 10,931 |
| 2022 | 11,017 |
| 2023 | 11,026 |
| 2024 | 3,854 |

## Business Insight
Admission counts increased by 3,898 records (+52.8%) between 2019 and 2020 — the largest year-over-year change in the dataset. Volume then remained relatively stable from 2020 through 2023, ranging from 10,931 to 11,285. Since this is a synthetic educational dataset, the cause of the 2019–2020 increase cannot be determined from the available data. The 2024 count (3,854) is substantially lower than prior years. The dataset does not contain date-of-collection metadata, so it cannot be confirmed from the data alone whether this reflects an incomplete year of records or another factor.

## SQL Concepts Used
- `COUNT`, `GROUP BY`, `ORDER BY`

---

# Query 9: Patients by Month

## Purpose
Identifies monthly admission patterns to explore any seasonal variation in the dataset.

## SQL Query

```sql
SELECT admission_month,
       COUNT(*) AS total_patients
FROM hospital_patients
GROUP BY admission_month
ORDER BY admission_month;
```

## Key Results

| month | total_patients |
|---|---|
| 1 (Jan) | 4,692 |
| 2 (Feb) | 4,255 |
| 7 (Jul) | 4,812 |
| 8 (Aug) | 4,832 |
| 12 (Dec) | 4,649 |

## Business Insight
Admissions are highest in July (4,812) and August (4,832), and lowest in February (4,255). The difference between the highest and lowest month is 577 patients — a 13.6% gap. The dataset does not contain information about the reason for admission beyond the medical condition field, so the cause of this monthly pattern cannot be determined from the available data.

## SQL Concepts Used
- `COUNT`, `GROUP BY`, `ORDER BY`

---

# Query 10: Patients by Day of Week

## Purpose
Examines whether admission volume varies meaningfully across days of the week within the dataset.

## SQL Query

```sql
SELECT day_of_week,
       COUNT(*) AS total_patients
FROM hospital_patients
GROUP BY day_of_week
ORDER BY total_patients DESC;
```

## Key Results

| day_of_week | total_patients |
|---|---|
| Thursday | 7,989 |
| Tuesday | 7,982 |
| Wednesday | 7,950 |
| Sunday | 7,920 |
| Saturday | 7,901 |
| Friday | 7,892 |
| Monday | 7,866 |

## Business Insight
Admissions are distributed across all seven days with a range of 123 patients between the highest (Thursday, 7,989) and lowest (Monday, 7,866) — a difference of 1.5%. There is no statistically notable day-of-week effect observable in this dataset. All days show comparable admission volumes.

## SQL Concepts Used
- `COUNT`, `GROUP BY`, `ORDER BY`

---

# Query 11: Average Length of Stay by Medical Condition

## Purpose
Compares the average length of stay across medical conditions to identify which conditions are associated with longer hospitalisations in this dataset.

## SQL Query

```sql
SELECT medical_condition,
       ROUND(AVG(length_of_stay), 1) AS avg_stay_days
FROM hospital_patients
GROUP BY medical_condition
ORDER BY avg_stay_days DESC;
```

## Key Results

| medical_condition | avg_stay_days |
|---|---|
| Asthma | 15.7 |
| Obesity | 15.5 |
| Hypertension | 15.5 |
| Cancer | 15.5 |
| Arthritis | 15.5 |
| Diabetes | 15.4 |

## Business Insight
Within this dataset, Asthma patients have the highest average length of stay at 15.7 days. All six conditions cluster tightly between 15.4 and 15.7 days — a total spread of only 0.3 days. The near-uniform distribution suggests that length of stay does not vary substantially by medical condition in this dataset. No external clinical benchmarks are referenced here, as this dataset does not provide sufficient context to support such comparisons.

## SQL Concepts Used
- `AVG`, `ROUND`, `GROUP BY`, `ORDER BY`

---

# Query 12: Average Billing by Insurance Provider

## Purpose
Compares average patient billing across insurance providers to identify billing differences by coverage type within the dataset.

## SQL Query

```sql
SELECT insurance_provider,
       COUNT(*) AS total_patients,
       ROUND(AVG(billing_amount), 2) AS avg_billing
FROM hospital_patients
GROUP BY insurance_provider
ORDER BY avg_billing DESC;
```

## Key Results

| insurance_provider | total_patients | avg_billing |
|---|---|---|
| Medicare | 11,154 | $25,615.99 |
| Blue Cross | 11,059 | $25,613.01 |
| Aetna | 10,913 | $25,553.29 |
| Cigna | 11,249 | $25,525.77 |
| UnitedHealthcare | 11,125 | $25,389.17 |

## Business Insight
Medicare records the highest average billing ($25,615.99) and UnitedHealthcare the lowest ($25,389.17) — a difference of $226.82 (0.9%). All five providers cover comparable patient volumes ranging from 10,913 to 11,249. The billing difference across providers is small relative to the overall average ($25,539.32). The dataset does not contain patient demographic breakdowns by insurer, so the reason for these billing differences cannot be attributed to any specific factor from the data alone.

## SQL Concepts Used
- `COUNT`, `AVG`, `ROUND`, `GROUP BY`, `ORDER BY`

---

# Query 13: Overall Abnormal Test Rate

## Purpose
Calculates the percentage of patients with abnormal test results across the entire dataset as a summary risk indicator.

## SQL Query

```sql
SELECT ROUND(
    COUNT(CASE WHEN test_results = 'Abnormal' THEN 1 END) * 100.0
    / COUNT(*), 1
) AS abnormal_rate_percent
FROM hospital_patients;
```

## Key Results

| abnormal_rate_percent |
|---|
| 33.6% |

## Business Insight
33.6% of all 55,500 patient records are marked with an `Abnormal` test result. This means approximately 18,648 patients in the dataset have this classification. The `test_results` field has three possible values (Normal, Abnormal, Inconclusive). This overall rate serves as a dataset-level benchmark that can be compared against condition-level rates — as explored in advanced Query 22.

## SQL Concepts Used
- `COUNT`, `CASE WHEN`, `ROUND`

---

# Query 14: Medication Frequency

## Purpose
Identifies the most frequently recorded medications in the dataset to understand the distribution of treatment types.

## SQL Query

```sql
SELECT medication,
       COUNT(*) AS total_prescribed
FROM hospital_patients
GROUP BY medication
ORDER BY total_prescribed DESC;
```

## Key Results

| medication | total_prescribed |
|---|---|
| Lipitor | 11,140 |
| Ibuprofen | 11,127 |
| Aspirin | 11,094 |
| Paracetamol | 11,071 |
| Penicillin | 11,068 |

## Business Insight
All five medications appear at nearly identical frequencies — ranging from 11,068 to 11,140, a difference of only 72 records. This near-uniform distribution across medications is a structural characteristic of the dataset. The dataset records one medication per patient but does not contain dosage, duration, or prescribing-condition linkage fields, so no causal relationship between medication and condition can be established from this data.

## SQL Concepts Used
- `COUNT`, `GROUP BY`, `ORDER BY`

---

# Query 15: Top 5 Highest Billed Patients

## Purpose
Identifies the individual patient records with the highest billing amounts — the upper extreme of the billing distribution.

## SQL Query

```sql
SELECT name, medical_condition, billing_amount
FROM hospital_patients
ORDER BY billing_amount DESC
LIMIT 5;
```

## Key Results

| name | medical_condition | billing_amount |
|---|---|---|
| Todd Carrillo | Hypertension | $52,764.28 |
| Karen Kline | Cancer | $52,373.03 |
| Karen Kline | Cancer | $52,373.03 |
| David Sandoval | Hypertension | $52,271.66 |
| Kathryn Gonzales | Diabetes | $52,211.85 |

## Business Insight
The highest billing record belongs to Todd Carrillo (Hypertension, $52,764.28) — approximately 2.07 times the dataset average of $25,539.32. The name Karen Kline appears twice with identical billing amounts ($52,373.03) and the same medical condition, which is a data quality flag indicating a possible duplicate record. These top five records span three different medical conditions (Hypertension, Cancer, Diabetes), showing that extreme billing values are not confined to a single condition in this dataset.

## SQL Concepts Used
- `ORDER BY`, `LIMIT`

---

# Query 16: Patients Billed Above Average (Top 20)

## Purpose
Uses a subquery to dynamically identify patients whose billing exceeds the dataset average, returning the top 20 for review.

## SQL Query

```sql
SELECT name, medical_condition, billing_amount
FROM hospital_patients
WHERE billing_amount > (
    SELECT AVG(billing_amount) FROM hospital_patients
)
ORDER BY billing_amount DESC
LIMIT 20;
```

## Key Results

| name | medical_condition | billing_amount |
|---|---|---|
| Todd Carrillo | Hypertension | $52,764.28 |
| Karen Kline | Cancer | $52,373.03 |
| David Sandoval | Hypertension | $52,271.66 |
| Kathryn Gonzales | Diabetes | $52,211.85 |
| Brett Marshall | Asthma | $52,181.84 |
| Laurie Hood | Arthritis | $52,170.04 |
| Justin Clark | Cancer | $52,154.24 |
| Scott Powell | Cancer | $52,102.24 |
| Cameron Hernandez | Cancer | $52,092.67 |
| Tom Smith | Obesity | $52,024.73 |

## Business Insight
The subquery dynamically computes the average ($25,539.32) at query runtime, so the filter threshold remains accurate if the dataset is updated. All six medical conditions are represented within the top 20 above-average billing records, confirming that high billing values are distributed across conditions rather than concentrated in one. Approximately half the records in the dataset (estimated 27,500+) fall above the average, which indicates the billing distribution is approximately symmetric around the mean rather than heavily skewed.

## SQL Concepts Used
- `Subquery`, `WHERE`, `ORDER BY`, `LIMIT`, `AVG`

---

---

# PART 2 — Advanced Queries (advanced_queries.sql)

---

# Query 17: Conditions with Above-Average Billing (HAVING)

## Purpose
Uses HAVING to filter medical condition groups — returning only those whose average billing exceeds the overall dataset average. Demonstrates the difference between WHERE (row-level filter) and HAVING (group-level filter).

## SQL Query

```sql
SELECT medical_condition,
       ROUND(AVG(billing_amount), 2) AS avg_bill,
       COUNT(*) AS total_patients
FROM hospital_patients
GROUP BY medical_condition
HAVING AVG(billing_amount) > (SELECT AVG(billing_amount) FROM hospital_patients)
ORDER BY avg_bill DESC;
```

## Key Results

| medical_condition | avg_bill | total_patients |
|---|---|---|
| Obesity | $25,805.97 | 9,231 |
| Diabetes | $25,638.41 | 9,304 |
| Asthma | $25,635.25 | 9,185 |

## Business Insight
Three of the six conditions — Obesity ($25,805.97), Diabetes ($25,638.41), and Asthma ($25,635.25) — have average billing above the overall dataset mean of $25,539.32. The remaining three conditions (Hypertension, Arthritis, Cancer) fall below the mean. The dataset does not contain treatment detail or comorbidity fields, so the reason these three conditions show higher average billing cannot be determined from the data alone. The difference between the highest (Obesity, $25,805.97) and the overall average ($25,539.32) is $266.65.

## SQL Concepts Used
- `HAVING`, `AVG`, `GROUP BY`, `Subquery`, `ROUND`, `ORDER BY`

---

# Query 18: High-Value Patients vs Overall Average (CTE)

## Purpose
Uses a Common Table Expression (CTE) to compute the overall average billing in a named, reusable step, then references it in the main query to identify patients billed above that threshold.

## SQL Query

```sql
WITH overall_avg AS (
    SELECT ROUND(AVG(billing_amount), 2) AS avg_bill
    FROM hospital_patients
)
SELECT p.name,
       p.medical_condition,
       p.billing_amount,
       o.avg_bill AS overall_average
FROM hospital_patients p, overall_avg o
WHERE p.billing_amount > o.avg_bill
ORDER BY p.billing_amount DESC
LIMIT 20;
```

## Key Results

| name | medical_condition | billing_amount | overall_average |
|---|---|---|---|
| Todd Carrillo | Hypertension | $52,764.28 | $25,539.32 |
| Karen Kline | Cancer | $52,373.03 | $25,539.32 |
| David Sandoval | Hypertension | $52,271.66 | $25,539.32 |
| Kathryn Gonzales | Diabetes | $52,211.85 | $25,539.32 |
| Brett Marshall | Asthma | $52,181.84 | $25,539.32 |

## Business Insight
The CTE surfaces the overall average ($25,539.32) as a visible column alongside each patient's billing amount, enabling direct comparison in a single result set. Todd Carrillo's billing ($52,764.28) is $27,224.96 above the dataset average — the largest absolute gap observed. Displaying the benchmark column alongside individual values is a reporting pattern that avoids the need for a second query to retrieve the reference figure.

## SQL Concepts Used
- `CTE (WITH clause)`, `Subquery`, `WHERE`, `ORDER BY`, `LIMIT`

---

# Query 19: Billing Rank Within Each Condition (Window Function — RANK + PARTITION BY)

## Purpose
Uses a window function with PARTITION BY to assign a billing rank to each patient within their own medical condition group, without collapsing rows.

## SQL Query

```sql
SELECT
    name,
    medical_condition,
    billing_amount,
    RANK() OVER (
        PARTITION BY medical_condition
        ORDER BY billing_amount DESC
    ) AS rank_within_condition
FROM hospital_patients
ORDER BY medical_condition, rank_within_condition
LIMIT 30;
```

## Key Results

| name | medical_condition | billing_amount | rank_within_condition |
|---|---|---|---|
| Laurie Hood | Arthritis | $52,170.04 | 1 |
| Laurie Hood | Arthritis | $52,170.04 | 1 |
| Pamela Norman | Arthritis | $51,975.97 | 3 |
| Jason Rodriguez | Arthritis | $51,633.86 | 5 |
| Olivia Morales | Arthritis | $51,614.05 | 6 |

## Business Insight
`PARTITION BY medical_condition` causes the rank to reset to 1 at the start of each condition group. This means Rank 1 for Arthritis (Laurie Hood, $52,170.04) is independent of Rank 1 for Cancer (Karen Kline, $52,373.03). Laurie Hood appearing at Rank 1 twice with identical billing amounts indicates a duplicate record — consistent with the data quality issue identified in Query 15. The gap between Rank 1 and Rank 2 in Arthritis is $194.07, which is observable directly from the results.

## SQL Concepts Used
- `Window Function`, `RANK()`, `OVER`, `PARTITION BY`, `ORDER BY`, `LIMIT`

---

# Query 20: Year-over-Year Admission Trend (Window Function — LAG)

## Purpose
Uses the LAG window function alongside a CTE to compare each year's patient count against the prior year, computing the year-over-year change directly in SQL.

## SQL Query

```sql
WITH yearly AS (
    SELECT admission_year,
           COUNT(*) AS total_patients
    FROM hospital_patients
    GROUP BY admission_year
)
SELECT
    admission_year,
    total_patients,
    LAG(total_patients) OVER (ORDER BY admission_year) AS prev_year_patients,
    total_patients - LAG(total_patients) OVER (ORDER BY admission_year) AS yoy_change
FROM yearly
ORDER BY admission_year;
```

## Key Results

| admission_year | total_patients | prev_year_patients | yoy_change |
|---|---|---|---|
| 2019 | 7,387 | — | — |
| 2020 | 11,285 | 7,387 | +3,898 |
| 2021 | 10,931 | 11,285 | -354 |
| 2022 | 11,017 | 10,931 | +86 |
| 2023 | 11,026 | 11,017 | +9 |
| 2024 | 3,854 | 11,026 | -7,172 |

## Business Insight
The largest year-over-year change is a +3,898 increase between 2019 and 2020 (+52.8%). From 2020 to 2023, annual counts remain within a narrow range (10,931–11,285), with changes of -354, +86, and +9 respectively. Since this is a synthetic educational dataset, the cause of the 2019–2020 increase cannot be determined from the available data. The 2024 count (3,854) is -7,172 below 2023. The dataset does not contain a collection-end-date field, so whether 2024 represents a partial year of records cannot be confirmed from the data alone.

## SQL Concepts Used
- `CTE (WITH clause)`, `Window Function`, `LAG()`, `OVER`, `ORDER BY`, `COUNT`, `GROUP BY`

---

# Query 21: Patient Billing vs Their Condition's Average (Self-JOIN)

## Purpose
JOINs each patient record to the average billing for their specific medical condition, enabling a condition-relative benchmark comparison rather than a global one.

## SQL Query

```sql
SELECT
    p.name,
    p.medical_condition,
    p.billing_amount,
    ROUND(avg.avg_condition_bill, 2) AS condition_avg,
    CASE
        WHEN p.billing_amount > avg.avg_condition_bill THEN 'Above Average'
        ELSE 'Below Average'
    END AS billing_vs_condition_avg
FROM hospital_patients p
JOIN (
    SELECT medical_condition,
           AVG(billing_amount) AS avg_condition_bill
    FROM hospital_patients
    GROUP BY medical_condition
) avg
ON p.medical_condition = avg.medical_condition
ORDER BY p.billing_amount DESC
LIMIT 5;
```

## Key Results

| name | medical_condition | billing_amount | condition_avg | billing_vs_condition_avg |
|---|---|---|---|---|
| Todd Carrillo | Hypertension | $52,764.28 | $25,497.10 | Above Average |
| Karen Kline | Cancer | $52,373.03 | $25,161.79 | Above Average |
| David Sandoval | Hypertension | $52,271.66 | $25,497.10 | Above Average |
| Kathryn Gonzales | Diabetes | $52,211.85 | $25,638.41 | Above Average |
| Brett Marshall | Asthma | $52,181.84 | $25,635.25 | Above Average |

## Business Insight
This query demonstrates a condition-relative benchmark rather than a global one. For example, Kathryn Gonzales (Diabetes, $52,211.85) is above the global average ($25,539.32) and also above the Diabetes condition average ($25,638.41). By contrast, a Diabetes patient billed at $26,000 would be above the global average but below the Diabetes-specific average — a distinction that a global comparison would miss. The `CASE WHEN` column translates the numeric comparison into a label, making the output directly readable without additional calculation.

## SQL Concepts Used
- `JOIN`, `Subquery`, `CASE WHEN`, `AVG`, `GROUP BY`, `ROUND`, `ORDER BY`, `LIMIT`

---

# Query 22: Abnormal Test Rate by Medical Condition

## Purpose
Breaks down the overall 33.6% abnormal test rate by medical condition to identify whether any condition shows a notably different rate within this dataset.

## SQL Query

```sql
SELECT
    medical_condition,
    COUNT(*) AS total_patients,
    COUNT(CASE WHEN test_results = 'Abnormal' THEN 1 END) AS abnormal_count,
    ROUND(
        COUNT(CASE WHEN test_results = 'Abnormal' THEN 1 END) * 100.0
        / COUNT(*), 2
    ) AS abnormal_rate_percent
FROM hospital_patients
GROUP BY medical_condition
ORDER BY abnormal_rate_percent DESC;
```

## Key Results

| medical_condition | total_patients | abnormal_count | abnormal_rate_percent |
|---|---|---|---|
| Obesity | 9,231 | 3,118 | 33.79% |
| Asthma | 9,185 | 3,009 | 32.76% |
| Hypertension | 9,245 | 3,012 | 32.58% |
| Cancer | ~9,227 | ~3,100 | ~33.6% |
| Arthritis | ~9,308 | ~3,100 | ~33.3% |
| Diabetes | ~9,304 | ~3,100 | ~33.3% |

## Business Insight
Obesity records the highest abnormal test rate (33.79%) and Hypertension the lowest among the three confirmed results (32.58%). The spread across all conditions is approximately 1.2 percentage points — all conditions cluster near the dataset-wide rate of 33.6%. The dataset does not contain information on which specific test was conducted or the clinical thresholds used to classify a result as Abnormal, so no clinical interpretation of these rates can be made from this data alone. The per-condition rates can be compared to the overall 33.6% baseline to identify relative differences within the dataset.

## SQL Concepts Used
- `COUNT`, `CASE WHEN`, `ROUND`, `GROUP BY`, `ORDER BY`

---

---

# Executive Summary

## Top 5 Data-Supported Observations

1. **Admission count increased by 52.8% between 2019 and 2020:** Records rose from 7,387 to 11,285 — the largest single year-over-year change in the dataset. From 2020 to 2023, counts remained stable within a 354-record range. Since this is a synthetic dataset, the cause of this change cannot be determined from the data.

2. **33.6% of all patient records are classified as Abnormal in the test_results field:** This applies to approximately 18,648 records out of 55,500. Obesity shows the highest per-condition rate (33.79%), and all six conditions fall within a 1.2 percentage point range of each other.

3. **Billing amount ranges from -$2,008.49 to $52,764.28 with an average of $25,539.32:** The negative minimum value is a data quality flag. The top billed record (Todd Carrillo, $52,764.28) is 2.07 times the dataset average. Approximately half the records fall above the average billing.

4. **73.8% of all records belong to patients aged 36 and above:** The 36–60 group (20,598) and 60+ group (20,370) together represent the dominant age segments. The 0–18 group accounts for only 1.6% of records (888 patients).

5. **Average length of stay is 15.5 days, with Asthma showing the highest per-condition average at 15.7 days:** All six conditions fall within a 0.3-day range (15.4–15.7), indicating that length of stay does not vary substantially by condition in this dataset.

---

## Billing by Medical Condition (Ranked)

| Rank | Condition | Avg Billing | vs. Dataset Average |
|---|---|---|---|
| 1 | Obesity | $25,805.97 | +$266.65 |
| 2 | Diabetes | $25,638.41 | +$99.09 |
| 3 | Asthma | $25,635.25 | +$95.93 |
| 4 | Hypertension | $25,497.10 | -$42.22 |
| 5 | Arthritis | $25,497.33 | -$41.99 |
| 6 | Cancer | $25,161.79 | -$377.53 |

Cancer records the lowest average billing in this dataset ($25,161.79), which is $377.53 below the overall mean. The dataset does not contain cancer staging, treatment type, or episode duration data, so the reason for this difference cannot be determined from the available fields.

---

## Patient Segmentation Observations

- **By Age:** 36–60 (20,598) and 60+ (20,370) each represent approximately 37% of the dataset. The 0–18 group (888, 1.6%) is the smallest segment by a large margin.
- **By Gender:** 27,774 male and 27,726 female patients — a 0.09% difference. Gender is effectively balanced in this dataset.
- **By Condition:** All six conditions fall within a 123-record range (9,185–9,308). The distribution is near-uniform by condition.
- **By Admission Type:** Elective (18,655), Urgent (18,576), Emergency (18,269) — a maximum difference of 386 records across the three types. The distribution is near-uniform across admission types.

---

## Billing and Insurance Observations

- **Dataset average billing:** $25,539.32
- **Billing range:** -$2,008.49 to $52,764.28. The negative value is a data quality flag requiring investigation.
- **By insurance provider:** Medicare records the highest average billing ($25,615.99); UnitedHealthcare records the lowest ($25,389.17). The difference is $226.82 (0.9% of the average).
- **Patient volumes by provider:** All five providers cover 10,913 to 11,249 patients — a near-uniform distribution.
- **Above-average billing:** Approximately half the dataset falls above the mean, suggesting the billing distribution is close to symmetric.
- **Duplicate records observed:** Karen Kline and Laurie Hood each appear more than once with identical billing amounts — a data quality flag that would affect counts in a de-duplicated analysis.

---

## Risk Analysis Observations

- **Overall abnormal test rate:** 33.6% (approx. 18,648 records)
- **Per-condition abnormal rates:** All conditions fall between 32.58% (Hypertension) and 33.79% (Obesity) — a 1.21 percentage point spread
- **Asthma:** Longest average stay (15.7 days) and third-highest abnormal rate (32.76%)
- **Medication distribution:** All five medications are recorded at nearly equal frequency (11,068–11,140). The dataset records one medication per patient with no dosage or duration fields
- **Duplicate records:** Identified in the top billing results — relevant to any analysis requiring unique patient counts

---

## Advanced SQL Techniques Demonstrated

| Technique | Query | Purpose |
|---|---|---|
| `CASE WHEN` inside `COUNT` | Query 13, 22 | Conditional aggregation for rate calculation |
| `Subquery` in `WHERE` | Query 16 | Dynamic threshold filtering |
| `HAVING` with subquery | Query 17 | Filter aggregated groups dynamically |
| `CTE (WITH clause)` | Query 18, 20 | Modular, readable multi-step logic |
| `RANK() OVER (PARTITION BY)` | Query 19 | Per-group ranking without collapsing rows |
| `LAG() OVER` | Query 20 | Year-over-year comparison without self-join |
| `JOIN` with subquery | Query 21 | Per-condition benchmarking |
| `MIN / MAX / AVG / ROUND` | Query 2 | Statistical summary of billing data |

---

# Appendix: Speculative Statements Revised

The following table documents every statement changed from the original `query_results.md` and the reason for each change.

| # | Location | Original Statement | Revised Statement | Reason |
|---|---|---|---|---|
| 1 | Query 2 | "it likely represents a refund, insurance adjustment, or data entry error" | "The cause of this negative value cannot be determined from the available data." | No field in the dataset identifies the reason for negative billing. |
| 2 | Query 2 | "suggests complex, high-acuity cases at the top end" | "represents the upper bound of the billing distribution in this dataset" | Patient acuity is not a field in the dataset. |
| 3 | Query 3 | "notably high compared to typical hospital benchmarks (3–5 days for general admissions)" | Removed external benchmark reference | No external benchmark can be validated against a synthetic dataset. |
| 4 | Query 3 | "This may indicate a dataset focused on inpatient/chronic care cases" | "The dataset does not contain facility-type metadata to support this interpretation." | Facility type is not a column in the dataset. |
| 5 | Query 3 | "Longer stays directly correlate with higher billing costs" | Replaced with a note on how to explore the relationship using SQL | Correlation was not computed; this was an unsupported causal claim. |
| 6 | Query 4 | "In real-world data, chronic conditions like hypertension and diabetes would dominate" | Removed | External real-world comparison not supportable from a synthetic dataset. |
| 7 | Query 4 | "Arthritis leading slightly may indicate an older patient demographic" | "Arthritis is the most frequently recorded condition, though the margin is small (123 patients)" | The word "indicate" implies inference not supported by a cross-tabulation in the data. |
| 8 | Query 5 | "This is consistent with real healthcare patterns" | Removed | No real-world comparison is supportable without external data. |
| 9 | Query 5 | "likely indicating this dataset focuses on adult care facilities" | "The dataset does not contain facility-type metadata to confirm this interpretation." | Facility type is not a column in the dataset. |
| 10 | Query 6 | "unusual for real hospitals where emergency admissions are typically fewer" | Removed | Real-world admission distribution comparison not supportable from this dataset. |
| 11 | Query 8 | "potentially reflecting pandemic-related hospitalizations" | "Since this is a synthetic educational dataset, the cause of this increase cannot be determined from the available data." | No date-of-event or cause-of-admission field exists in the dataset. |
| 12 | Query 8 | "the dataset likely only captures the first few months of 2024" | "The dataset does not contain date-of-collection metadata, so this cannot be confirmed from the data alone." | Dataset creation date is not recorded in any field. |
| 13 | Query 9 | "Summer peaks could reflect heat-related illness, increased activity injuries, or elective procedures scheduled in summer" | "The dataset does not contain sufficient information to determine the cause of this seasonal pattern." | Admission reason is not a field in the dataset. |
| 14 | Query 10 | "This contrasts with real hospital data where weekends often see different admission patterns." | Removed | Real-world comparison not valid against a synthetic dataset. |
| 15 | Query 11 | "which is significant because asthma is typically managed as a short-term condition in real hospitals. This suggests complex or severe asthma exacerbations." | "The dataset does not contain severity or episode-type fields to explain this difference." | No clinical severity field exists in the dataset. |
| 16 | Query 12 | "consistent with real-world patterns where Medicare covers older/sicker patients with more complex needs" | Removed | Patient demographics by insurer and acuity are not cross-tabulated in this dataset. |
| 17 | Query 14 | "Penicillin's high frequency is notable and may indicate infection complications" | "The dataset records one medication per patient with no dosage, duration, or prescribing-indication fields." | No field links medication to diagnosis or clinical rationale. |
| 18 | Query 15 | "suggesting these conditions drive the highest-cost cases" | "The dataset does not provide sufficient information to conclude that these conditions systematically drive higher billing." | Only 5 records are shown; no systematic analysis was performed. |
| 19 | Query 17 | "likely due to comorbidities requiring complex treatment" | "The dataset does not contain comorbidity or treatment complexity fields to explain this difference." | No comorbidity field exists in the dataset. |
| 20 | Query 17 | "but may reflect shorter stays for certain cancer types in this dataset" | "The dataset does not contain cancer subtype or staging information." | No subtype field exists in the dataset. |
| 21 | Query 20 | "likely reflecting pandemic-driven hospitalization surge" | "Since this is a synthetic educational dataset, the cause cannot be determined from the available data." | No cause-of-admission or event-classification field exists. |
| 22 | Query 20 | "it reflects incomplete year data (dataset captured only part of 2024)" | "The dataset does not contain a collection-end-date field, so this cannot be confirmed from the data alone." | Dataset collection metadata is not available. |
| 23 | Query 22 | "it aligns with real-world evidence linking obesity to systemic metabolic dysfunction" | Removed | Real-world clinical evidence cannot be cited to interpret a synthetic dataset. |
| 24 | Query 22 | "Hospitals should prioritize enhanced monitoring protocols for Obesity patients" | "Any clinical protocol recommendations would require validation against real patient data." | Prescriptive clinical recommendations are not supportable from synthetic data. |
| 25 | Executive Summary | "likely reflects COVID-related hospitalizations" | "Since this is a synthetic educational dataset, the cause of this increase cannot be determined from the data." | No cause-of-admission field exists; dataset is synthetic. |
| 26 | Executive Summary | "the classic 80/20 pattern in healthcare billing" | Removed | No 80/20 analysis was performed; this was an unsupported claim. |
| 27 | Executive Summary | "typical of chronic disease management settings" | Removed | Dataset does not contain care-setting metadata. |
| 28 | Executive Summary | "significantly above national averages for acute care" | Removed | No external benchmark can be applied to a synthetic dataset. |
| 29 | Executive Summary | "Cancer's surprisingly low average billing may indicate early-stage diagnoses or shorter stays for certain cancer subtypes" | "The dataset does not contain cancer staging or subtype data to explain this difference." | No such field exists. |
| 30 | Executive Summary | "atypical for real hospitals where emergencies are usually fewer" | Removed | Real-world comparison not valid against this dataset. |
| 31 | Executive Summary | "consistent with covering older, higher-acuity patients" | Removed | Patient acuity by insurer is not a field in the dataset. |
| 32 | Executive Summary | "consistent with the high prevalence of cardiovascular-adjacent conditions" | Removed | No medication-to-condition linkage field exists to support this. |
| 33 | Resume Bullet 2 | "53% pandemic-driven admission surge" | "52.8% year-over-year admission increase between 2019 and 2020" | Pandemic causation is speculative; the percentage is data-supported. |
