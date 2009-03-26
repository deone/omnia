use omnia;

insert into user (username, password, firstname, lastname, roles) values ("deone", md5("dune369"), "Oladayo", "Osikoya", "Administrator");
insert into user (username, password, firstname, lastname, roles) values ("deone125", md5("dune369"), "Olufemi", "Olusola", "User");

insert into vendor (name, address, phone) values ("Hewlett Packard", "Oko Oloyun Street, Victoria Island", "08023456789");
insert into vendor (name, address, phone) values ("Microsoft", "Bishop Oluwole Street, Ikoyi", "08038388888");
insert into vendor (name, address, phone) values ("Procter & Gamble", "Asaba, Delta State", "08054673456");

insert into item (name, type) values ("Longhorn Server", "Computer Hardware");
insert into item (name, type) values ("Microsoft Office", "Computer Software");
insert into item (name, type) values ("Windows Mail Exchange", "Computer Software");
insert into item (name, type) values ("Microsoft Vista", "Computer Software");
insert into item (name, type) values ("HP Notebook", "Computer Hardware");
insert into item (name, type) values ("Microsoft Windows Server 2003", "Computer Software");
insert into item (name, type) values ("Forklift", "Engineering Tool");
insert into item (name, type) values ("Oil Drill", "Engineering Tool");
