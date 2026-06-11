-- ============================================================
-- Hospital Patient Analytics — Advanced SQL Queries
-- Database : hospital.db (SQLite)
-- Table    : hospital_patients
-- Concepts : HAVING, CTEs, Window Functions, LAG, Self-Join
-- ============================================================


-- ================================
-- 1. HAVING — Filter After Grouping
-- ================================
-- Interview explanation:
-- "WHERE filters rows before grouping.
--  HAVING filters groups after aggregation.
--  Here I want only conditions where the average bill is above
--  the overall average — so I use a subquery inside HAVING."

SELECT medical_condition,
       ROUND(AVG(billing_amount), 2) AS avg_bill,
       COUNT(*)                      AS total_patients
FROM hospital_patients
GROUP BY medical_condition
HAVING AVG(billing_amount) > (SELECT AVG(billing_amount) FROM hospital_patients)
ORDER BY avg_bill DESC;


-- ================================
-- 2. CTE — Common Table Expression
-- ================================
-- Interview explanation:
-- "A CTE is like a temporary named result I can reference
--  in the same query. It makes complex queries easier to read.
--  Here I first calculate the overall average billing in the CTE,
--  then use it to find high-value patients."

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


-- ================================
-- 3. Window Function — RANK with PARTITION BY
-- ================================
-- Interview explanation:
-- "A window function performs a calculation across a set of rows
--  related to the current row without collapsing them into groups.
--  PARTITION BY medical_condition means the rank resets for each
--  condition — so I can see the top billed patient per condition."

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


-- ================================
-- 4. Window Function — LAG for Year-over-Year Trend
-- ================================
-- Interview explanation:
-- "LAG lets me look at the previous row's value.
--  I first aggregate total patients per year using a CTE,
--  then use LAG to compare each year against the previous year
--  to show growth or decline in admissions."

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


-- ================================
-- 5. Self-Join — Compare Patients to Condition Average
-- ================================
-- Interview explanation:
-- "Even with one table, I can JOIN it to a subquery.
--  Here I join each patient to the average billing of their
--  own medical condition to see if they were billed above
--  or below the average for their condition."

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
LIMIT 20;


-- ================================
-- 6. Abnormal Test Rate per Condition
-- ================================
-- Interview explanation:
-- "CASE WHEN inside COUNT lets me count only rows that meet
--  a condition. Dividing by total COUNT gives me a percentage.
--  This shows which medical condition has the highest risk of
--  abnormal test results."

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
