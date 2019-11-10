create database pickme
on
(
	name = pickme,
	filename = 'E:\pickme\pickme.ndf',
	size = 1024mb,
	filegrowth = 10%
)
log
on
(
	name = pickme_log,
	filename = 'E:\pickme\pickme_log.ldf',
	size = 100mb,
	filegrowth = 10%
);
use pickme

create table users
(
	username varchar(16) primary key,
	userpwd varchar(20)
);

create table student
(
	susername varchar(16) primary key,
	sname varchar(20),
	ssex char(2) check(ssex in ('ÄÐ','Å®')),
	userid char(18) unique,
	useridphoto varchar(256),
	sinfo varchar(32),
	sidphoto varchar(256),
	sbirth date,
	stel char(11) unique,
	suserphoto varchar(256),
	foreign key(susername) references users(username)

);


create table driver
(
	dusername  varchar(16) primary key,
	dname varchar(20),
	dsex char(2) check(dsex in ('ÄÐ','Å®')),
	userid char(18) unique,
	useridphoto varchar(256),
	dinfo varchar(32),
	didphoto varchar(256),
	cycletype varchar(32),
	cycleinfo varchar(256),
	cyclephoto varchar(256),
	dbirth date ,
	dtel char(11) unique,
	duserphoto varchar(256)
	foreign key(dusername) references users(username)
);
 
create table orders
(
	orderid int identity(1,1) primary key,
	susername varchar(16),
	dusername varchar(16),
	fast_car int,
	free_ride int,
	rent_car int,
	finish int,
	startpoint varchar(256),
	endpoint varchar(256),
	sdate date,
	stime time,
	price float(2),
	cyclephoto1 varchar(256),
	cyclephoto2 varchar(256),
	comment1 varchar(256),
	comment2 varchar(256),
	deposit int,
	foreign key(dusername) references driver(dusername),
	foreign key(susername) references student(susername)
);

