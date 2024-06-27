drop table if exists User;
create Table User(
    user_id int primary key,
    username varchar(255),
    email varchar(255),
    password varchar(255),
    created_at timestamp,
    updated_at timestamp
);

drop table if exists Chatbot;
create Table ChatBot(
    user_id int REFERENCES User(user_id),
    chatbot_id int,
    chatbot_name varchar(255),
    chatbot_type tinyint,
    chatbot_persona varchar (255) not null default '',
    create_at timestamp,
    is_deleted bool
);

drop table if exists Chat_history;
create Table Chat_history(
    user_id int REFERENCES User(user_id),
    chatbot_id int REFERENCES ChatBot(chatbot_id),
    create_at timestamp,
    content longtext,
    by_user bool
);

drop table if exists Prompt;
create Table Prompt(
    user_id int REFERENCES User(user_id),
    chatbot_id int REFERENCES ChatBot(chatbot_id),
    prompt_name varchar(255),
    prompt_content longtext
);