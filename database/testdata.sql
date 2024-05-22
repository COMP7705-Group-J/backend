insert into user
values (1,"test","zxc@qq.com,","password",NOW(),NOW());

insert into chatbot
values (1,1, "chatbot01", 0, "", NOW(), FALSE);

insert into chat_history
values (1,1,NOW(),"test data", 1);

insert into chat_history
values (1,1,NOW(),"test data1", 0);