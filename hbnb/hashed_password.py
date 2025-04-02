import bcrypt

password = b'admin1234'
hashed = bcrypt.hashpw(password, bcrypt.gensalt())
print(hashed.decode())

# $2b$12$RStd6NU.fBlTsVZlWU7cvujN3Pl3aA21mpyWqpVn9dno6g0lnGHGu