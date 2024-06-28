insert into User
values (1,"test","zxc@qq.com,","password",NOW(),NOW());

insert into ChatBot
values (1,1, "chatbot01", 0, "", NOW(), FALSE);

insert into Chat_history
values (1,1,NOW()+1,"test data", 1);

insert into Chat_history
values (1,1,NOW()+2,"test data1", 0);

insert into Chat_history
values (1,2,NOW()+3,"test data2", 1);

insert into Chat_history
values (1,2,NOW()+4,"test data3", 0);

insert into Prompt
values (1,1,"last_summary","");