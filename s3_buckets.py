__author__ = 'martin'
import boto

s3 = boto.connect_s3()

bucket_name = 'mybucket95126'   # Name has to be unique
print "Creating new bucket with name: " + bucket_name
bucket = s3.create_bucket(bucket_name)

from boto.s3.key import Key
k = Key(bucket)
k.key = 'foo.txt'  # Create a file in bucket

print "Uploading some data to " + bucket_name + " with key: " + k.key
k.set_contents_from_string('Hey Foo!')   # Write to file foo.txt

contentOfFile = k.get_contents_as_string()  # Get content from foo.txt
print 'Content of file ' + k.key + ' is: ' + contentOfFile

listOfBuckets = s3.get_all_buckets()

for i in listOfBuckets:
    print 'Bucket: ', i.name


raw_input("Press enter to delete both the object and the bucket...")

# Buckets cannot be deleted unless they're empty. Since we still have a
# reference to the key (object), we can just delete it.
print "Deleting the object."
k.delete()

# Now that the bucket is empty, we can delete it.
print "Deleting the bucket."
s3.delete_bucket(bucket_name)
