use leisure;

select u.year, u.전국, m.전국
from unemployment_data as u
inner join movie_audience_number as m
on u.year = m.year;

select c.year, m.전국, c.소비자물가지수
from consumer_price_index as c
inner join movie_audience_number as m 
on c.year = m.year;

select ot.year, m.전국, ot.OTT이용자수
from ott_users_number as ot
inner join movie_audience_number as m
on ot.year = m.year;


ALTER TABLE movie_audience_number
ADD FOREIGN KEY (year) REFERENCES years(year);

ALTER TABLE movie_audience_number ADD PRIMARY KEY (year);

ALTER TABLE consumer_price_index
ADD FOREIGN KEY (year) REFERENCES movie_audience_number(year);

ALTER TABLE ott_users_number
ADD FOREIGN KEY (year) REFERENCES movie_audience_number(year);

ALTER TABLE movie_audience_number
ADD FOREIGN KEY (year) REFERENCES unemployment_data;

ALTER TABLE movie_audience_number DROP FOREIGN KEY movie_audience_number_ibfk_2;

ALTER TABLE consumer_price_index DROP FOREIGN KEY consumer_price_index_ibfk_1;

drop table if exists consumer_price_index;

select con.year, mov.전국, con.영화소비자
from consumer_price_movie as con
inner join movie_audience_number as mov
on con.year = mov.year;

ALTER TABLE consumer_price_movie
ADD FOREIGN KEY (year) REFERENCES movie_audience_number(year);