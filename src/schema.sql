CREATE TABLE MONITORING (
  ID integer primary key autoincrement,
  TS timestamp not null,
  URL string not null,
  LABEL string not null,
  RESPONSE_TIME float,
  STATUS_CODE integer default null,
  CONTENT_LENGTH integer default null
);
