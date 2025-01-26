use Accounts;
SET autocommit = OFF;

create table Accounts(
id int primary key auto_increment,
account_number int unique check(account_number BETWEEN 10000 AND 99999 ),
balance BIGINT
);

delimiter //
create view Bank_amount
as
select sum(balance)
from Accounts; //

delimiter //
create view Bank_number
as
select count(account_number)
from Accounts; //