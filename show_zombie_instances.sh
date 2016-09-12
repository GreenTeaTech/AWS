#!/bin/bash

# You may adjust these values
START_TIME="2016-08-31T00:01:00Z"
END_TIME="2016-09-06T23:59:00Z"
METRIC="CPUUtilization"
PERIOD="604800"
STATISTICS="Average"
PROFILE="dev"
REGION="us-east-1"
MAX_THRESHOLD=10.0
MIN_THRESHOLD=0.0

# Parse JSON
function jsonval {
        temp=`echo $json | sed 's/\\\\\//\//g' | sed 's/[{}]//g' | awk -v k="text" '{n=split($0,a,","); for (i=1; i<=n; i++) print a[i]}' | sed 's/\"\:\"/\|/g' | sed 's/[\,]/ /g' | sed 's/\"//g' | grep -w $str | cut -d":" -f2 | sed -e 's/^ *//g' -e 's/ *$//g'`
        echo ${temp##*|}
}

# Store all instances in temp file
aws ec2 describe-instances --region ${REGION} --profile ${PROFILE} --query 'Reservations[].Instances[].[ InstanceId,[Tags[?Key==`Name`].Value][0][0],[Tags[?Key==`service-name`].Value][0][0],State.Name,InstanceType,Placement.AvailabilityZone ]' --output table > all_instances

for instance in `cat all_instances | grep -v "DescribeInstances" | awk -F"|" '{print $2}' | sed 's/ //'`; do
        status=`cat all_instances | grep ${instance} | awk -F"|" '{print $5}'`
        type=`cat all_instances | grep ${instance} | awk -F"|" '{print $6}'`
        name=`cat all_instances | grep ${instance} | awk -F"|" '{print $3}'`
        service_name=`cat all_instances | grep ${instance} | awk -F"|" '{print $4}'`

        if [ $status == "stopped" ]; then
                echo "${name} ${instance} ${type} ${status}" >> stopped_instances
        fi

        json=`aws cloudwatch get-metric-statistics --metric-name ${METRIC} --start-time ${START_TIME} --end-time ${END_TIME} --period ${PERIOD} --namespace AWS/EC2 --statistics ${STATISTICS} --dimensions Name=InstanceId,Value=${instance} --region ${REGION} --profile ${PROFILE}`
        str="Average"
        cpu=`jsonval`

# Show only running instances with cpu value between thresholds
        if [ ! -z "${cpu}" ] && (( $(echo "${cpu} > ${MIN_THRESHOLD}" | bc -l) )) && (( $(echo "${cpu} < ${MAX_THRESHOLD}" | bc -l) )); then
                echo "${name} ${service_name} ${instance} ${type} ${status} Average cpu -> ${cpu}"
        fi
done
cat stopped_instances
# Remove temp file
rm -f stopped_instances
rm -f all_instances
