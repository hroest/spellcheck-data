
"""
    DROP TABLE IF EXISTS `page`;
    /*!40101 SET @saved_cs_client     = @@character_set_client */;
    /*!40101 SET character_set_client = utf8 */;
    CREATE TABLE `page` (
      `page_id` int(8) unsigned NOT NULL AUTO_INCREMENT,
      `page_namespace` int(11) NOT NULL DEFAULT '0',
      `page_title` varbinary(255) NOT NULL DEFAULT '',
      `page_restrictions` tinyblob NOT NULL,
      `page_counter` bigint(20) unsigned NOT NULL DEFAULT '0',
      `page_is_redirect` tinyint(1) unsigned NOT NULL DEFAULT '0',
      `page_is_new` tinyint(1) unsigned NOT NULL DEFAULT '0',
      `page_random` double unsigned NOT NULL DEFAULT '0',
      `page_touched` varbinary(14) NOT NULL DEFAULT '',
      `page_links_updated` varbinary(14) DEFAULT NULL,
      `page_latest` int(8) unsigned NOT NULL DEFAULT '0',
      `page_len` int(8) unsigned NOT NULL DEFAULT '0',
      `page_content_model` varbinary(32) DEFAULT NULL,
      PRIMARY KEY (`page_id`),
      UNIQUE KEY `name_title` (`page_namespace`,`page_title`),
      KEY `page_random` (`page_random`),
      KEY `page_len` (`page_len`),
      KEY `page_redirect_namespace_len` (`page_is_redirect`,`page_namespace`,`page_len`)
    ) ENGINE=InnoDB AUTO_INCREMENT=52169215 DEFAULT CHARSET=binary;
    /*!40101 SET character_set_client = @saved_cs_client */;
"""


import gzip

f = "enwiki-20161101-page.sql.gz"

pagefile = gzip.open(f, "rb")
for l in pagefile:
    if l.startswith("INSERT INTO"):

        for qq in l.split("),("):
            fields = qq.split(",")
            pgid = fields[0]
            pgns = fields[1]
            pgtitle = fields[2]
            pgredir = fields[5]

            ## if pgredir == "1" and pgns == "0":
            ##     print pgtitle, pgns

            # no redirects, only ns 0
            if pgredir == "0" and pgns == "0":
                print pgtitle




