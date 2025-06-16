-- Enum for booking status
DO $$ BEGIN
    CREATE TYPE booking_status AS ENUM ('PENDING', 'CONFIRMED');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- Create the users table
CREATE TABLE IF NOT EXISTS users (
    userid SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password TEXT NOT NULL,
    usertype VARCHAR(50) CHECK (usertype IN ('customer', 'eventmanager')) NOT NULL
);

-- Create the bookings table
CREATE TABLE IF NOT EXISTS bookings (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    event_id INT NOT NULL,
    tickets INT NOT NULL CHECK (tickets > 0),
    total_amount INT NOT NULL CHECK (total_amount >= 0),
    status booking_status DEFAULT 'PENDING',
    FOREIGN KEY (user_id) REFERENCES users(userid) ON DELETE CASCADE
);



-- Create the payments table
CREATE TABLE IF NOT EXISTS payments (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    account_id INT NOT NULL,
    booking_id INT NOT NULL,
    amount INT NOT NULL CHECK (amount >= 0),
    status VARCHAR(20) DEFAULT 'SUCCESS',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(userid) ON DELETE CASCADE,
    FOREIGN KEY (booking_id) REFERENCES bookings(id) ON DELETE CASCADE
);
