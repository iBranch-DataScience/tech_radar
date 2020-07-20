// Create collection
db.createCollection( 'scraping_log',)

// Create index
db.scraping_log.createIndex({
        keyword: 1,
        timestamp: 1,
        http_code: 1,
}, )
