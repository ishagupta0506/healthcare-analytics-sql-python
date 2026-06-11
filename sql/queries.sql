-- ============================================================
-- Hospital Patient Analytics — Core SQL Queries
-- Database : hospital.db (SQLite)
-- Table    : hospital_patients
-- Purpose  : KPI analysis, segmentation, cost & risk insights
-- ============================================================

-- NOTE: Table creation and data loading are handled by
--       load_to_sqlite.py using Python + pandas.


-- ================================
-- 1. Key KPI Analysis
-- ================================

-- How many patients are in the dataset?
SELECT COUNT(*) AS total_patients
FROM hospital_patients;

-- What is the average, minimum, and maximum billing amount?
SELECT
    ROUND(AVG(billing_amount), 2) AS avg_billing,
    ROUND(MIN(billing_amount), 2) AS min_billing,
    ROUND(MAX(billing_amount), 2) AS max_billing
FROM hospital_patients;

-- What is the average length of hospital stay?
SELECT ROUND(AVG(length_of_stay), 1) AS avg_stay_days
FROM hospital_patients;


-- ================================
-- 2. Patient Segmentation
-- ================================

-- How many patients have each medical condition?
SELECT medical_condition,
       COUNT(*) AS total_patients
FROM hospital_patients
GROUP BY medical_condition
ORDER BY total_patients DESC;

-- How are patients distributed across age groups?
SELECT age_group,
       COUNT(*) AS total_patients
FROM hospital_patients
GROUP BY age_group
ORDER BY age_group;

-- How many patients came in under each admission type?
SELECT admission_type,
       COUNT(*) AS total_patients
FROM hospital_patients
GROUP BY admission_type
ORDER BY total_patients DESC;

-- What is the gender split of patients?
SELECT gender,
       COUNT(*) AS total_patients
FROM hospital_patients
GROUP BY gender
ORDER BY total_patients DESC;


-- ================================
-- 3. Time-Based Analysis
-- ================================

-- How many patients were admitted each year?
SELECT admission_year,
       COUNT(*) AS total_patients
FROM hospital_patients
GROUP BY admission_year
ORDER BY admission_year;

-- Which month sees the most admissions?
SELECT admission_month,
       COUNT(*) AS total_patients
FROM hospital_patients
GROUP BY admission_month
ORDER BY admission_month;

-- Which day of the week has the most admissions?
SELECT day_of_week,
       COUNT(*) AS total_patients
FROM hospital_patients
GROUP BY day_of_week
ORDER BY total_patients DESC;


-- ================================
-- 4. Cost & Risk Analysis
-- ================================

-- Which medical condition leads to the longest hospital stays?
SELECT medical_condition,
       ROUND(AVG(length_of_stay), 1) AS avg_stay_days
FROM hospital_patients
GROUP BY medical_condition
ORDER BY avg_stay_days DESC;

-- Which insurance provider has the highest average billing?
SELECT insurance_provider,
       COUNT(*) AS total_patients,
       ROUND(AVG(billing_amount), 2) AS avg_billing
FROM hospital_patients
GROUP BY insurance_provider
ORDER BY avg_billing DESC;

-- What percentage of all test results are Abnormal?
SELECT ROUND(
    COUNT(CASE WHEN test_results = 'Abnormal' THEN 1 END) * 100.0
    / COUNT(*), 1
) AS abnormal_rate_percent
FROM hospital_patients;

-- Which medications are prescribed most often?
SELECT medication,
       COUNT(*) AS total_prescribed
FROM hospital_patients
GROUP BY medication
ORDER BY total_prescribed DESC;


-- ================================
-- 5. High Value Patients
-- ================================

-- Who are the top 5 highest billed patients?
SELECT name, medical_condition, billing_amount
FROM hospital_patients
ORDER BY billing_amount DESC
LIMIT 5;

-- Which patients were billed above the dataset average? (Top 20)
SELECT name, medical_condition, billing_amount
FROM hospital_patients
WHERE billing_amount > (
    SELECT AVG(billing_amount) FROM hospital_patients
)
ORDER BY billing_amount DESC
LIMIT 20;
