use Accounts;
SET autocommit = OFF;

create table Accounts(
id int primary key auto_increment,
account_number int check(account_number BETWEEN 10000 AND 99999 ),
balance BIGINT
);