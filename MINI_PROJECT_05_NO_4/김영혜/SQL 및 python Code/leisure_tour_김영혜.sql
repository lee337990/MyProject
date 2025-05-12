use leisure;

# 공통으로 사용될 year와 region 테이블 만들기
create table years (
    year int primary key);

insert into years (year)
values (2000), (2001), (2002), (2003), (2004), (2005), (2006), (2007), (2008), 
       (2009), (2010), (2011), (2012), (2013), (2014), (2015), (2016), (2017), 
       (2018), (2019), (2020), (2021), (2022), (2023), (2024);

create table regions (
    region_name VARCHAR(50) primary key);

insert into regions (region_name)
values ('서울특별시'), ('부산광역시'), ('대구광역시'), ('인천광역시'), ('광주광역시'),
       ('대전광역시'), ('울산광역시'), ('세종특별자치시'), ('경기도'), ('강원특별자치도'),
       ('충청북도'), ('충청남도'), ('전북특별자치도'), ('전라남도'), ('경상북도'),
       ('경상남도'), ('제주특별자치도'), ('전국');
select * from regions;

# 한국어로 된 컬럼을 바꾸기...ㅋㅋ...
# `year`로 통일!
ALTER TABLE ski_fixed RENAME column `연도` TO `year`;
ALTER TABLE tour_fixed RENAME COLUMN `연도` TO `year`;
ALTER TABLE park_fixed RENAME COLUMN `연도` TO `year`;

# 연도에 따른 각 경기침체 지표 변화 테이블 만들기
# 지금은 각 경제 지표 테이블 마다 지역별로 데이터가 있음
# 전국 총합계인 '계' 데이터를 가지고 테이블 만들기
CREATE TABLE economic_summary (
    year INT PRIMARY KEY,
    national_unemployment_rate FLOAT, # 전국 실업률
    national_employment_rate FLOAT,   # 전국 고용률
    active_population INT,            # 경제활동 인구
    inactive_population INT           # 비경제활동 인구
);
ALTER TABLE economic_summary
MODIFY COLUMN active_population FLOAT,
MODIFY COLUMN inactive_population FLOAT;


DESC economic_summary;
desc inactive_economy_data;
ALTER TABLE economic_summary MODIFY COLUMN inactive_population BIGINT;

INSERT INTO economic_summary (year, national_unemployment_rate, national_employment_rate, active_population, inactive_population)
SELECT e.year, u.전국 AS national_unemployment_rate, e.전국 AS national_employment_rate, 
       a.전국 AS active_population, n.전국 AS inactive_population
FROM employment_data e
JOIN unemployment_data u ON e.year = u.year
JOIN active_economy_data a ON e.year = a.year
JOIN inactive_economy_data n ON e.year = n.year;

select * from economic_summary;

# economic_summary 테이블과 year 테이블 연결
ALTER TABLE economic_summary ADD FOREIGN KEY (year) REFERENCES years(year);

# 모든 테이블을 economic_summary와 연결
ALTER TABLE employment_data ADD FOREIGN KEY (year) REFERENCES economic_summary(year);
ALTER TABLE unemployment_data ADD FOREIGN KEY (year) REFERENCES economic_summary(year);
ALTER TABLE active_economy_data ADD FOREIGN KEY (year) REFERENCES economic_summary(year);
ALTER TABLE inactive_economy_data ADD FOREIGN KEY (year) REFERENCES economic_summary(year);
ALTER TABLE ski_fixed ADD FOREIGN KEY (year) REFERENCES economic_summary(year);
ALTER TABLE park_fixed ADD FOREIGN KEY (year) REFERENCES economic_summary(year);
ALTER TABLE tour_fixed ADD FOREIGN KEY (year) REFERENCES economic_summary(year);
ALTER TABLE hotspring_data ADD FOREIGN KEY (year) REFERENCES economic_summary(year);


# VScode Python 코드에 넣을 query 확인---------------------------------------------------

SELECT year, 전국, 서울특별시, 부산광역시, 대구광역시, 
              인천광역시, 광주광역시, 대전광역시, 울산광역시
FROM employment_data
WHERE year >= 2013
ORDER BY year;

SELECT year, 전국, 경상북도, 경상남도, 강원특별자치도, 충청남도, 부산광역시
FROM hotspring_data
WHERE year >= 2013
ORDER BY year;

SELECT year, 롯데월드, 이월드, 서울랜드, 에버랜드, 경주월드, 
       (롯데월드 + 이월드 + 서울랜드 + 에버랜드 + 경주월드) AS 전체_이용객수
FROM park_fixed
ORDER BY year;

ALTER TABLE tour_fixed
CHANGE COLUMN `관광지점 수` `관광지점_수` INT;

ALTER TABLE tour_fixed
CHANGE COLUMN `입장객 수` `입장객_수` INT;

SELECT year, 관광지점_수, 입장객_수
FROM tour_fixed
ORDER BY year;

ALTER table ski_fixed
CHANGE COLUMN `스키 이용객 수` `스키_이용객_수` INT;

SELECT s.year, s.스키_이용객_수, e.active_population AS 경제활동인구, 
       e.inactive_population AS 비경제활동인구, e.national_unemployment_rate AS 실업률
FROM ski_fixed s
INNER JOIN economic_summary e ON s.year = e.year
ORDER BY s.year;

SELECT t.year, t.입장객_수, 
       e.inactive_population AS 비경제활동인구, e.national_unemployment_rate AS 실업률
FROM tour_fixed t
INNER JOIN economic_summary e ON t.year = e.year
ORDER BY t.year;

SELECT p.year,p.전체_이용객수,
    e.inactive_population AS 비경제활동인구, e.national_unemployment_rate AS 실업률
FROM (
    SELECT year,
           (롯데월드 + 이월드 + 서울랜드 + 에버랜드 + 경주월드) AS 전체_이용객수
    FROM park_fixed
) p
INNER JOIN economic_summary e ON p.year = e.year
ORDER BY p.year;

SELECT h.year, h.전국 AS 전국_온천_이용객, e.active_population AS 경제활동인구, 
       e.inactive_population AS 비경제활동인구, e.national_unemployment_rate AS 실업률
FROM hotspring_data h
INNER JOIN economic_summary e ON h.year = e.year
ORDER BY h.year;

SELECT e.year,
       e.전국 AS 고용률,
       u.전국 AS 실업률,
       a.전국 AS 경제활동인구비율,
       i.전국 AS 비경제활동인구수,
       p.전체_이용객수 AS 놀이공원_이용객,
       h.전국 AS 온천_이용객,
       s.스키_이용객_수 AS 스키장_이용객,
       t.입장객_수 AS 관광_입장객
FROM employment_data e
INNER JOIN unemployment_data u ON e.year = u.year
INNER JOIN active_economy_data a ON e.year = a.year
INNER JOIN inactive_economy_data i ON e.year = i.year
INNER JOIN (
    SELECT year, (롯데월드 + 이월드 + 서울랜드 + 에버랜드 + 경주월드) AS 전체_이용객수
    FROM park_fixed
) p ON e.year = p.year
INNER JOIN hotspring_data h ON e.year = h.year
INNER JOIN ski_fixed s ON e.year = s.year
INNER JOIN tour_fixed t ON e.year = t.year
ORDER BY e.year;

desc employment_data;
select * from employment_data;

desc park_fixed;


desc unemployment_data;
desc employment_data;
desc active_economy_data;
desc inactive_economy_data;

desc park_fixed;
desc hotspring_data;
desc ski_fixed;
desc tour_fixed;
desc income_impacts;
desc economic_summary;





