import boto.ec2

conn = boto.ec2.connect_to_region("us-west-2")

conn.run_instances(
        'ami-fbf6f1cb',
        key_name='martin',
        instance_type='t2.micro',
        security_groups=['default'])
