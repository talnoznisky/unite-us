
# Unite Us take-home
## Prompt
A directory holds about 500 files that are HTTP access logs in common log format.  Eg.,

123.66.150.17 - - [12/Aug/2010:02:45:59 +0000] "POST /wordpress3/wp-admin/admin-ajax.php HTTP/1.1" 200 2 "http://www.example.com/wordpress3/wp-admin/post-new.php" "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.25 Safari/534.3"

Each log file contains 24 hours of data and is about 500MB.  Write a script that will produce a minute-by-minute CSV that contains an aggregate count of the accesses organized by HTTP status code (200 in the above example).  If the above example was the only input, the result would be
```
# time, 200
12/Aug/2010:02:45, 1
```

## Instructions
- `git clone`  this repo
- run `sh run.sh` in root

### TODO:
- clean up input and output file name concatentations
- add regex checks and logging for log metadata parsing and extraction
- refactor `create_output_list` 
