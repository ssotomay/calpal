
load data local infile '~/public_html/cgi-bin/mollee/cdata.csv'
into table course_data
fields terminated by ','
enclosed by '"'
lines terminated by '\r\n'
(CRN, course, title, distribution, time, professor1, professor2, location, days);