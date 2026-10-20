-- =============================================
-- Система учёта договоров: SQL-запросы проекта
-- =============================================

-- ---------------------------------------------
-- Выборка списков (SELECT / ORDER BY)
-- ---------------------------------------------

-- 1. Все контрагенты (сортировка по названию)
SELECT id, name, inn
FROM contractors
ORDER BY name;

-- 2. Все договоры с сортировкой по сумме (убывание)
SELECT id, number, contractor_id, amount, start_date, end_date
FROM contracts
ORDER BY amount DESC;

-- ---------------------------------------------
-- Фильтрация (WHERE)
-- ---------------------------------------------

-- 3. Договоры с суммой больше 100000
SELECT id, number, amount
FROM contracts
WHERE amount > 100000
ORDER BY amount DESC;

-- 4. Договоры, срок действия которых истекает до заданной даты
SELECT id, number, end_date
FROM contracts
WHERE end_date < '2026-01-01'
ORDER BY end_date;

-- 5. Контрагенты с ИНН, начинающимся на '77' (московские)
SELECT id, name, inn
FROM contractors
WHERE inn LIKE '77%'
ORDER BY name;

-- ---------------------------------------------
-- Соединение таблиц (JOIN)
-- ---------------------------------------------

-- 6. Список договоров с названием контрагента
SELECT contracts.id,
       contracts.number,
       contractors.name AS contractor_name,
       contracts.amount,
       contracts.start_date,
       contracts.end_date
FROM contracts
JOIN contractors ON contracts.contractor_id = contractors.id
ORDER BY contracts.number;

-- 7. Платежи с номером договора и названием контрагента
SELECT payments.id,
       payments.payment_date,
       payments.amount,
       contracts.number   AS contract_number,
       contractors.name   AS contractor_name
FROM payments
JOIN contracts   ON payments.contract_id  = contracts.id
JOIN contractors ON contracts.contractor_id = contractors.id
ORDER BY payments.payment_date;

-- ---------------------------------------------
-- Агрегатные функции
-- ---------------------------------------------

-- 8. Общая сумма всех договоров
SELECT COUNT(*)         AS contracts_count,
       SUM(amount)      AS total_amount,
       AVG(amount)      AS avg_amount,
       MIN(amount)      AS min_amount,
       MAX(amount)      AS max_amount
FROM contracts;

-- 9. Сумма платежей по конкретному договору
SELECT contracts.number,
       COUNT(payments.id) AS payments_count,
       SUM(payments.amount) AS total_paid
FROM contracts
LEFT JOIN payments ON payments.contract_id = contracts.id
WHERE contracts.id = 1
GROUP BY contracts.id, contracts.number;

-- 10. Договоры с итоговой суммой с НДС 20 % (вычисление в SQL)
SELECT id,
       number,
       amount,
       ROUND(amount * 1.2, 2) AS amount_with_vat
FROM contracts
ORDER BY number;

-- ---------------------------------------------
-- Группировка (GROUP BY)
-- ---------------------------------------------

-- 11. Количество договоров у каждого контрагента
SELECT contractors.name AS contractor_name,
       COUNT(contracts.id) AS contracts_count,
       COALESCE(SUM(contracts.amount), 0) AS total_amount
FROM contractors
LEFT JOIN contracts ON contracts.contractor_id = contractors.id
GROUP BY contractors.id, contractors.name
ORDER BY contracts_count DESC;

-- ---------------------------------------------
-- Фильтрация групп (HAVING)
-- ---------------------------------------------

-- 12. Контрагенты, у которых больше одного договора
SELECT contractors.name AS contractor_name,
       COUNT(contracts.id) AS contracts_count
FROM contractors
JOIN contracts ON contracts.contractor_id = contractors.id
GROUP BY contractors.id, contractors.name
HAVING COUNT(contracts.id) > 1
ORDER BY contracts_count DESC;