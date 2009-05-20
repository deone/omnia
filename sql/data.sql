use procure;

insert into user (username, password, firstname, lastname, roles) values ("dayoo", md5("admin"), "Oladayo", "Osikoya", "Administrator");
insert into user (username, password, firstname, lastname, roles) values ("femio", md5("buyer"), "Olufemi", "Olusola", "Buyer");
insert into user (username, password, firstname, lastname, roles) values ("chukwudio", md5("procman"), "Chukwudi", "Ogwumba", "Procurement Manager");
insert into user (username, password, firstname, lastname, roles) values ("audue", md5("wareman"), "Audu", "Ernest", "Warehouse Manager");

insert into vendor (name, address, phone) values ("Hewlett Packard", "Oko Oloyun Street, Victoria Island", "08023456789");
insert into vendor (name, address, phone) values ("Microsoft", "Bishop Oluwole Street, Ikoyi", "08038388888");
insert into vendor (name, address, phone) values ("Procter & Gamble", "Asaba, Delta State", "08054673456");

insert into item (name, type) values ("HP Server", "Computer Hardware");
insert into item (name, type) values ("Windows Server", "Computer Software");
insert into item (name, type) values ("Microsoft Outlook", "Computer Software");
insert into item (name, type) values ("Microsoft Vista", "Computer Software");
insert into item (name, type) values ("HP Notebook", "Computer Hardware");
insert into item (name, type) values ("Microsoft Windows Server 2003", "Computer Software");
insert into item (name, type) values ("Forklift", "Engineering Tool");
insert into item (name, type) values ("Oil Drill", "Engineering Tool");

insert into warehouse(location, address, manager, manager_email) values ("Ikeja", "Oba Akinjobi Way, G.R.A", 4, "deone@example.com");
