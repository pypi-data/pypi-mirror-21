#awskit

how to install awskit
	1.install pip 
	2. run command:
		pip install libaws
	3.run awskit
		as follows:
		xxxxxx$ awskit
		usage: awskit [-h] [-s3] [-ec2]
		optional arguments:
		  -h, --help   show this help message and exit
		  -s3:
		    s3 param groups
			-s3, --s3    set the param is s3 storage group params true or false
		-ec2:
			ec2 param groups
			-ec2, --ec2  set the param is ec2 group params true or false


awskit --help information

	1.upload file to bucket
	awskit -s3 -upload xxxxx
	useage:
	  -file FILE_PATH, --file FILE_PATH [Required]
	  -bucket BUCKET, --bucket BUCKET
							dest bucket to upload [Required]
	  -part PART_NUM, --part PART_NUM
							part num of file [DEFAULT 6]
	  -key KEY, --key KEY   dest bucket key 
	  -ignore-bucket-file, --ignore-bucket-file
							when file exist in bucket ,ignore it or not [DEFAULT False]
	  -force-again-upload, --force-again-upload
							need to upload again when upload is exists [DEFAULT False]


							
	2.awskit -s3 -download xxxxx
	download bucket file to local computer
	useage:
	  -bucket BUCKET, --bucket BUCKET
							dest bucket to download file [Required]
	  -key KEY, --key KEY   bucket file to download [Required]
	  -path PATH, --path PATH
							file download path to save [Default .]
	  -filename FILENAME, --filename FILENAME
							download file name [DEFAULT False]
	  -force-again-download, --force-again-download
							need to download again when download is exists[DEFAULT False]


	3. awskit -s3 -bucket xxxx
	operation on bucket
	useage:

		name BUCKET, --name BUCKET
						dest bucket to operate
		-put-bucket-policy, --put-bucket-policy
							set bucket policy
		-json BUCKET_POLICY_JSON, --json BUCKET_POLICY_JSON
									bucket policy json file
	
	4. awskit -s3 -md5 xxxx
	caculate file md5 hash value
	useage:
		-path FILE_PATH, --path FILE_PATH
	            file path to caculate md5
		-part PART_NUMBER, --part PART_NUMBER
				divide part number of file

	5. awskit -ec2
		create instance vpc subnet route security from config
		a):
			create instance
				awskit -ec2 --instance -c xxxxxxx (create and lanuch instance from config)
			create vpc
				awskit -ec2 --vpc -c xxxxxx  (create vpc from config) 
			create subnet
				awskit -ec2 --subnet -c  (create subnet from config)
			create route:
				awskit -ec2 --route -c  (create route from config)
			create security group
				awskit -ec2 -security -c (create security group from config)



