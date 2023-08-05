-- maildrake/store/fixture.sql
-- Part of Mail Drake, an email server for development and testing.
--
-- Copyright © 2017 Ben Finney <ben+python@benfinney.id.au>
--
-- This is free software, and you are welcome to redistribute it under
-- certain conditions; see the end of this file for copyright
-- information, grant of license, and disclaimer of warranty.

-- Sample data fixture for Mail Drake database.

INSERT INTO message
        (
            message_id, created_at, "date",
            sender, recipients, subject,
            "body", mime_type, "raw")
VALUES
        (
            '566b9184556a2e3c12c157a135238290a10c90bd@googlemail.com',
            '2017-02-01', '2017-01-01', 'marshallkevin@gmail.com',
            'roy10@larson.org.au, stephanierusso@hayes.org.au, ccochran@smith.info, irwinspencer@parker.com',
            'Illo aperiam eum nemo corrupti aut quisquam.',
            'Nihil illum ab autem. Cum numquam exercitationem dolores incidunt aspernatur sint. Quos quaerat veniam provident eius.',
            'text/plain',
            'Message-Id: <566b9184556a2e3c12c157a135238290a10c90bd@googlemail.com>
Date: Sun, 01 Jan 2017 00:00:00 +0000
From: marshallkevin@gmail.com
To: roy10@larson.org.au, stephanierusso@hayes.org.au, ccochran@smith.info, irwinspencer@parker.com
Subject: Illo aperiam eum nemo corrupti aut quisquam.

Nihil illum ab autem. Cum numquam exercitationem dolores incidunt aspernatur sint. Quos quaerat veniam provident eius.
'),
        (
            'cbd4074ed2d91524590aaa4faf7ffaf8@iis.com.au',
            '2017-02-01', '2017-01-02', 'hlopez@harris.biz',
            'monique94@watts.biz, smithmiranda@hotmail.com.au',
            'Odio praesentium nostrum fugit dicta at libero quae.',
            'Error facilis eligendi deserunt sit dolorem aliquid debitis. Aperiam hic earum animi quibusdam est omnis. Iusto neque aspernatur quam doloremque.',
            'text/plain',
            'Message-Id: <cbd4074ed2d91524590aaa4faf7ffaf8@iis.com.au>
Date: Mon, 02 Jan 2017 00:00:00 +0000
From: hlopez@harris.biz
To: monique94@watts.biz, smithmiranda@hotmail.com.au
Subject: Odio praesentium nostrum fugit dicta at libero quae.

Error facilis eligendi deserunt sit dolorem aliquid debitis. Aperiam hic earum animi quibusdam est omnis. Iusto neque aspernatur quam doloremque.
'),
        (
            '62551d29a4385e0e0e7679b94c671ef72fdcdbcfb01c61bee93c96b9d5268c71@mail.thompson-hall.edu',
            '2017-02-01', '2017-01-03', 'ryan21@thompson-hall.edu',
            'juliaharris@hotmail.com',
            'Dolorum deleniti consectetur provident.',
            'Qui dolor fugit aliquam repudiandae exercitationem. Beatae deserunt iure neque ab vel. Quisquam provident illo commodi eaque maiores omnis repellat. Dolorum labore hic officia molestias non.',
            'text/plain',
            'Message-Id: <62551d29a4385e0e0e7679b94c671ef72fdcdbcfb01c61bee93c96b9d5268c71@mail.thompson-hall.edu>
Date: Tue, 03 Jan 2017 00:00:00 +0000
From: ryan21@thompson-hall.edu
To: juliaharris@hotmail.com
Subject: Dolorum deleniti consectetur provident.

Qui dolor fugit aliquam repudiandae exercitationem. Beatae deserunt iure neque ab vel. Quisquam provident illo commodi eaque maiores omnis repellat. Dolorum labore hic officia molestias non.
')
;


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
