-- Süper admin şifresi: 518518 (hash edilmiş hali)
INSERT IGNORE INTO users (username, email, password, is_superadmin) 
VALUES (
    'superadmin', 
    'superadmin@example.com',
    'pbkdf2:sha256:260000$8FOQpGqBX7u8kKlm$337b2b5394c5c996d2daf084dc7c8c7bfd087499b45e22a523fd39bddfd3ac6a',
    1
);

UPDATE users 
SET 
    email = 'superadmin@example.com',
    password = 'pbkdf2:sha256:260000$8FOQpGqBX7u8kKlm$337b2b5394c5c996d2daf084dc7c8c7bfd087499b45e22a523fd39bddfd3ac6a',
    is_superadmin = 1
WHERE username = 'superadmin';
