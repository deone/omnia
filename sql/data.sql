use omnia;

insert into user (username, password, firstname, lastname, roles) values ("deone", md5("dune369"), "Oladayo", "Osikoya", "Administrator");
insert into user (username, password, firstname, lastname, roles) values ("deone125", md5("dune369"), "Olufemi", "Olusola", "User");

insert into vendor (name, address, phone) values ("Hewlett Packard", "Oko Oloyun Street, Victoria Island", "08023456789");
insert into vendor (name, address, phone) values ("Microsoft", "Bishop Oluwole Street, Ikoyi", "08038388888");

insert into item (name, type) values ("Longhorn Server", "Hardware");
insert into item (name, type) values ("Microsoft Office", "Software");
insert into item (name, type) values ("Windows Mail Exchange", "Software");
insert into item (name, type) values ("Microsoft Vista", "Software");
insert into item (name, type) values ("HP Notebook", "Hardware");
insert into item (name, type) values ("Microsoft Windows Server 2003", "Software");
