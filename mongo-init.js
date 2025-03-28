db.createUser({
  user: process.env.MONGO_INITDB_ROOT_USERNAME,
  pwd: process.env.MONGO_INITDB_ROOT_PASSWORD,
  roles: [{ role: "dbOwner", db: process.env.MONGO_INITDB_DATABASE }]
});

db = db.getSiblingDB("OnlineEventBookingPlatform");

db.createCollection("events");

db.counters.insertOne({
  _id: "event_id",
  seq: 0
});
