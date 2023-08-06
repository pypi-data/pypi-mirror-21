Changelog
=========

Changes with latest version of libaws
----------------------------------------------

Version 1.0 -------------2016-06-04

1.use boto software to implement base amazon web service
2.enable upload muliti part files to bucket
3.enable max upload retry attemps
4.upload files enable resume from break point
5.real upload speed end progress show
6.enable download files from bucket to local
7.download files enable resume from break point
8.enable max download retry attemps
5.real download speed end progress show



Version 1.0.1 -------------2016-06-04
1.fix tiny bug of init app data path

Version 1.0.2 -------------2016-06-05
1.fix missing logger config file 
2.when download files path is not exist,create it

Version 1.0.3 -------------2016-06-06
1.enable download or upload zero files
2.enable color print log
3.enable upload daemon process
4.add switch param to enable debug log or not 

Version 1.0.4 -------------2016-06-17
1. fix get file hash memory error cause program corrupted
2. modidy and optimise program description
3. adjust upload and download some warn log level 
4. enable create instance vpc subnet route security from config file
5. develop an awskit tool to enable s3 and ec2 command collection with console commandline
6. repair download bucket child folder files bug
7. repair when bucket set policy , cause download file fail bug
8. enable set bucket policy with bucket console commandline
9. enable launch a default instance and auto connect with ssh


Version 1.0.5 -------------2016-07-18
1.fix when image_id is not exists,cause program corrupted 
2.optimise instace config,each region contains a instance config file suitable with this region
3 delelte same vpc config,when vpc exists
4.add caculate file md5 and aws e_tag function module
5.enable instance stop,reboot,terminate function
6.enable i2,r3 type instance spot request
7.get default image id when image_id is not exist

Version 1.0.6 -------------2016-07-29
1.enable download daemon process
2.repair upload file to s3 bug
3.show upload or download time when upload or download finished
4.backup key file when create new key 
5.repair create default instance key bug
6 enable set thread config number when upload file to s3
7.repair upload progreass show bug
8.repair download file permision bug
9.optimise s3 upload/download param usage

Version 1.0.7 -------------2016-08-23
1.optimise s3/ec2 param usage
2.repair upload same file to different bucket bug
3.enable wait for spot request to complete and tag spot instance
4.support download s3 dir files
5.support upload dir files to s3

Version 1.0.8 -------------2016-09-2
1.optimise download s3 dir recursion files
2.save ec2 instance info to db
3.enable to find instance by fuzzy tag name
4.enable batch stop,term,start,reboot instances
5.repair create instance tag error
6.suport multithread download s3 files

Version 1.0.9 -------------2016-09-30
1.accelerate spot request instance speed
2.repair ec2 bucket error
3.enable ec2 instance put into placegroup
4.enable start stop and delete download action
5.enable start stop and delete all downloads action
6.enable bucket key delete action

Version 1.1.0 -------------2016-10-14
1.enable attach volumes to instance
2.enable bucket list action
3.repair list bucket dir child keys bug
4.repair s3 download many times bug
5.optimise log display
6.repair yaml format file name

Version 1.1.1 -------------2017-04-11
1.repair s3 file download etag not match bug
2.calucate file hash support devide by part size or part num
3.enable upload file to s3 with devide by part size or part num,default is upload with part size which is 8MB 
