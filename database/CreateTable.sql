create Table User(
    user_id int primary key,
    username varchar(255),
    email varchar(255),
    password varchar(255),
    created_at timestamp,
    updated_at timestamp
);


create Table ChatBot(
    user_id int REFERENCES User(user_id),
    chatbot_id int
);

create Table Chat_history(
    user_id int REFERENCES User(user_id),
    chatbot_id int REFERENCES ChatBot(chatbot_id),
    create_at timestamp,
    content longtext,
    by_user bool
);