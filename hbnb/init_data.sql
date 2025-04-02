-- Admin User
INSERT INTO Users (id, email, first_name, last_name,  password, is_admin)
VALUES (
    '36c9057e-ddd3-4c3b-9731-9f487208bbc1',
    'Aylin@hbnb.io',
    'Aylin',
    'Pintos',
    '$2b$12$RStd6NU.fBlTsVZlWU7cvujN3Pl3aA21mpyWqpVn9dno6g0lnGHGu',
    TRUE
);

-- Initial Amenities
INSERT INTO Amenity (id, name)
VALUES
    ('b65a4b5d-8e4e-4970-92e4-94592f0d84e9', 'WiFi'),
    ('7f647ee9-fb46-4f2b-babc-4087ae893a91', 'Swimming Pool'),
    ('2f5cfa41-41c9-4ce2-b5a2-c2748a6b42e0', 'Air Conditioning');