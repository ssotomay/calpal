use random;

drop table if exists course_data;
create table course_data(
	CRN char(5) primary key,
	course varchar(40),
	title varchar(100),
	distribution varchar(50),
	time varchar(100),
	professor1 varchar(100),
	professor2 varchar(100),
	location varchar(50),
	days varchar(10));


drop table if exists students;
create table students(
       bNum char(8),
       CRN char(5),
       course varchar(40),
       title varchar(100),
       distribution varchar(50),
       time varchar(100),
       professor1 varchar(100),
       professor2 varchar(100),
       location varchar(50),
       days varchar(10),
       primary key (bNum,CRN));
       
