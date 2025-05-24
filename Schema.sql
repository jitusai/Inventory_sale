create database inventory_db;
use inventory_db;
create table Products(product_id varchar(20) primary key,
                      name varchar(100),category varchar(50),
					  price decimal(10,2), quantity int);
create  table Customers(customer_id varchar(20) primary key,
                        name varchar(100),
						phone varchar(15));
create table sales(sale_id int primary key auto_increment,
                   customer_id varchar(20),product_id varchar(20),
                   quantity int,sale_date date,
				   foreign key(customer_id) references Customers(customer_id),
				   foreign key(product_id) references Products(product_id));