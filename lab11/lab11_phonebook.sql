
-- 1. Функция для поиска по шаблону (часть имени, фамилия, номер телефона)
CREATE OR REPLACE FUNCTION search_phonebook(pattern TEXT)
RETURNS TABLE(id INT, name VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT id, name, phone
    FROM phonebook
    WHERE name ILIKE '%' || pattern || '%' OR phone ILIKE '%' || pattern || '%';
END;
$$ LANGUAGE plpgsql;

-- 2. Процедура для добавления нового пользователя или обновления номера телефона
CREATE OR REPLACE PROCEDURE add_or_update_user(new_name VARCHAR, new_phone VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM phonebook WHERE name = new_name) THEN
        UPDATE phonebook SET phone = new_phone WHERE name = new_name;
    ELSE
        INSERT INTO phonebook(name, phone) VALUES (new_name, new_phone);
    END IF;
END;
$$;

-- 3. Процедура для вставки множества новых пользователей с проверкой телефона
CREATE OR REPLACE PROCEDURE add_multiple_users(names TEXT[], phones TEXT[])
LANGUAGE plpgsql AS $$
DECLARE
    i INT;
BEGIN
    FOR i IN 1..array_length(names, 1) LOOP
        IF phones[i] ~ '^\+?\d{10,15}$' THEN  -- Проверка формата телефона
            IF NOT EXISTS (SELECT 1 FROM phonebook WHERE name = names[i]) THEN
                INSERT INTO phonebook(name, phone) VALUES (names[i], phones[i]);
            END IF;
        ELSE
            RAISE NOTICE 'Неверный номер телефона: %', phones[i];
        END IF;
    END LOOP;
END;
$$;

-- 4. Функция для запроса данных с разбиением на страницы
CREATE OR REPLACE FUNCTION get_phonebook_page(limit INT, offset INT)
RETURNS TABLE(id INT, name VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT id, name, phone
    FROM phonebook
    LIMIT limit OFFSET offset;
END;
$$ LANGUAGE plpgsql;

-- 5. Процедура для удаления записи по имени или номеру телефона
CREATE OR REPLACE PROCEDURE delete_user_or_phonebook_entry(delete_value TEXT)
LANGUAGE plpgsql AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM phonebook WHERE name = delete_value) THEN
        DELETE FROM phonebook WHERE name = delete_value;
    ELSIF EXISTS (SELECT 1 FROM phonebook WHERE phone = delete_value) THEN
        DELETE FROM phonebook WHERE phone = delete_value;
    ELSE
        RAISE NOTICE 'Запись не найдена с таким именем или номером телефона';
    END IF;
END;
$$;
