----Easy Problems -----
 
----1.	Show first name, last name, and gender of patients who's gender is 'M' 
select first_name,last_name,gender from patients
where gender = 'M'


----2.	Show first name and last name of patients who does not have allergies. (null) 
select first_name,last_name 
from patients
where allergies IS  null

---3.	Show first name of patients that start with the letter 'C' 
select first_name
from patients
where first_name like 'C%'


---4.	Show first name and last name of patients that weight within the range of 100 to 120 (inclusive) 
select first_name,last_name
from patients
where weight between 100 and 120


---5.	Update the patients table for the allergies column. If the patient's allergies is null then replace it with 'NKA' 
update patients
set allergies = 'NKA'
where allergies is NULL


---6.	Show first name and last name concatinated into one column to show their full name. 
select CONCAT(first_name,' ',last_name) AS full_name
from patients


---7.	Show first name, last name, and the full province name of each patient. 
       ---Example: 'Ontario' instead of 'ON' 
select p.first_name,p.last_name,n.province_name
from patients p 
join province_names n ON p.province_id = n.province_id


---8.	Show how many patients have a birth_date with 2010 as the birth year. 
select count(*) from patients
where year(birth_date) = 2010


---9.	Show the first_name, last_name, and height of the patient with the greatest height. 
select first_name,last_name,height
from patients
where height  =(select max(height) from	patients)


---10.	Show all columns for patients who have one of the following patient_ids: 1,45,534,879,1000 
select * from
patients
where patient_id IN(1,45,534,879,1000)


---11.	Show the total number of admissions 
select count(patient_id)
from admissions


---12.	Show all the columns from admissions where the patient was admitted and discharged on the same day. 
select * from
admissions
WHERE admission_date = discharge_date


---13.	Show the patient id and the total number of admissions for patient_id 579. 
select patient_id,count(patient_id)
from admissions
where patient_id = 579


---14.	Based on the cities that our patients live in, show unique cities that are in province_id 'NS'? 
select distinct(city) from
patients
where province_id = 'NS'


---15.	Write a query to find the first_name, last name, and birth date of patients who has height greater than 160 and weight greater than 70 
select first_name,last_name,birth_date
from patients
where height > 160 and weight > 70


---16.	Write a query to find list of patients first_name, last_name, and allergies from city 'Hamilton' where allergies is not null 
select first_name,last_name,allergies
from patients
where city = 'Hamilton' and allergies is not NULL


---17.	Based on cities where our patient lives in, write a query to display the list of unique city starting with a vowel (a, e, i, o, u). Show the result order in ascending by city. 
select distinct(city)  As unique_city
from patients
where city like 'a%'
OR city like 'e%'
or city like 'i%'
or city like 'o%'
oR city like 'u%'
order by city
