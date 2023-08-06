-- maildrake/store/schema.sql
-- Part of Mail Drake, an email server for development and testing.
--
-- Copyright © 2017 Ben Finney <ben+python@benfinney.id.au>
--
-- This is free software, and you are welcome to redistribute it under
-- certain conditions; see the end of this file for copyright
-- information, grant of license, and disclaimer of warranty.

-- Schema initialisation script for Mail Drake database.

DROP TABLE IF EXISTS message;
CREATE TABLE message (
        message_id VARCHAR NOT NULL,
        created_at TIMESTAMP,
        "date" TIMESTAMP,
        sender VARCHAR,
        recipients VARCHAR,
        subject VARCHAR,
        "body" BLOB,
        "raw" BLOB,
        mime_type VARCHAR,
        PRIMARY KEY (message_id)
        );

DROP TABLE IF EXISTS message_part;
CREATE TABLE IF NOT EXISTS message_part (
        message_id VARCHAR NOT NULL
            REFERENCES message (message_id),
        part_index INTEGER,
        mime_type VARCHAR,
        is_attachment BOOLEAN,
        filename VARCHAR,
        "encoding" VARCHAR,
        "body" BLOB,
        "raw" BLOB,
        PRIMARY KEY (message_id, part_index)
        );


-- Copyright © 2017 Ben Finney <ben+python@benfinney.id.au>
--
-- This is free software: you may copy, modify, and/or distribute this work
-- under the terms of the GNU Affero General Public License as published by the
-- Free Software Foundation; version 3 of that license or any later version.
-- No warranty expressed or implied. See the file ‘LICENSE.AGPL-3’ for details.


-- Local variables:
-- coding: utf-8
-- mode: sql[ansi]
-- End:
-- vim: fileencoding=utf-8 filetype=sql :
