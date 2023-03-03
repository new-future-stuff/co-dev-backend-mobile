INSERT INTO skill (id, name) VALUES 
(1, 'FastAPI'),
(2, 'Django'),
(3, 'Express'),
(4, 'Spring Boot'),
(5, 'ASP.NET'),
(6, 'Laravel'),
(7, 'Ruby on Rails'),
(8, 'Fiber Framework'),
(9, 'CakePHP'),
(10, 'Flask'),
(11, 'Play'),
(12, 'Flutter'),
(13, 'Phoenix'),
(14, 'HTML'),
(15, 'CSS'),
(16, 'Bootstrap'),
(17, 'Foundation'),
(18, 'Semantic UI'),
(19, 'Materialize'),
(20, 'Material Design Lite'),
(21, 'Pure'),
(22, 'Sass'),
(23, 'LESS'),
(24, 'Angular'),
(25, 'Vue.js'),
(26, 'Ember.js'),
(27, 'React'),
(28, 'jQuery'),
(29, 'D3.js'),
(30, 'Rust'),
(31, 'C++'),
(32, 'C'),
(33, 'Python'),
(34, 'Ruby'),
(35, 'Node.js'),
(36, 'Go'),
(37, 'Ubuntu'),
(38, 'Debian'),
(39, 'Unix'),
(40, 'Networking Security and Protocols'),
(41, 'Vim'),
(42, 'Docker'),
(43, 'Terraform'),
(44, 'AWS'),
(45, 'Azure'),
(46, 'Linode'),
(47, 'Swift'),
(48, 'Kotlin'),
(49, 'Java'),
(50, 'PyTorch'),
(51, 'TensorFlow'),
(52, 'Apache'),
(53, 'IoT'),
(54, 'NoSQL'),
(55, 'R'),
(56, 'Kubernetes'),
(57, 'Keras'),
(58, 'XGBoost'),
(59, 'Darknet');

INSERT INTO language (id, name) VALUES 
    (1, 'Русский'),
    (2, 'English');

INSERT INTO country (id) VALUES 
    (1),
    (2),
    (3),
    (4),
    (5);

INSERT INTO translatedcountryname (country_id, name, language_id) VALUES
    (1, 'Россия', 1),
    (2, 'США', 1),
    (3, 'Канада', 1),
    (4, 'Великобритания', 1),
    (5, 'Германия', 1),
    (1, 'Russia', 2),
    (2, 'USA', 2),
    (3, 'Canada', 2),
    (4, 'United Kingdom', 2),
    (5, 'Germany', 2);

INSERT INTO user (id, name, hashed_password, salt, profile_picture_url, email) VALUES 
    (1, 'Александр', '123456', 'salt123', 'https://randomuser.me/api/portraits/men/1.jpg', 'alexander@example.com'),
    (2, 'Елена', 'abcdef', 'salt456', 'https://randomuser.me/api/portraits/women/1.jpg', 'elena@example.com');

INSERT INTO userskilllink (user_id, skill_id) VALUES 
    (1, 1),
    (1, 2),
    (1, 3),
    (2, 4),
    (2, 5);

INSERT INTO project (id, name, description, creator_id, reward, currency, logo_url) VALUES 
    (1, 'Веб-приложение с использованием Django', 'Веб-приложение для управления проектами с использованием фреймворка Django', 1, 2000, 'руб', 'https://cdn.example.com/project1_logo.jpg'),
    (2, 'Сервис покупки билетов на концерты', 'Сервис, который позволяет заказывать билеты на концерты', 2, 1500, 'руб', 'https://cdn.example.com/project2_logo.jpg');

INSERT INTO projectskilllink (project_id, skill_id) VALUES 
    (1, 2),
    (1, 6),
    (1, 25),
    (2, 8),
    (2, 27),
    (2, 31);
