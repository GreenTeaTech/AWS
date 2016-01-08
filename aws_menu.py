#!/usr/bin/env python

# California region

import boto.ec2
import time

isValid = 1
ec2 = boto.ec2.connect_to_region("us-west-1")

def check_state(choice):
    reservations = ec2.get_all_reservations(
                    filters={'instance-id': choice})
    for reservation in reservations:
        for instance in reservation.instances:
            state = instance.update()
            while state not in ('running', 'stopped', 'terminated'):
                time.sleep(2)
                state = instance.update()
                print " state:", state

def print_instances():
    reservations = ec2.get_all_reservations()
    for reservation in reservations:
        for instance in reservation.instances:
            if 'Name' in instance.tags:
                print "%s (%s) [%s]" % (instance.tags['Name'], instance.id, instance.state)
            else:
                print "%s [%s]" % (instance.id, instance.state)

def stop_instance(choice):
    print 'Stopping instance: ', choice
    ec2.stop_instances(instance_ids=choice)
    check_state(choice)

def start_instance(choice):
    print 'Starting up instance: ', choice
    ec2.start_instances(instance_ids=choice)
    check_state(choice)

def reboot_instance(choice):
    print 'Rebooting instance: ', choice
    ec2.reboot_instances(instance_ids=choice)

def terminate_instance(choice):
    print 'Terminating instance: ', choice
    ec2.terminate_instances(instance_ids=choice)
    check_state(choice)

def check_id(choice):
    success = False
    reservations = ec2.get_all_reservations()
    for reservation in reservations:
        for instance in reservation.instances:
            if str(instance.id) == choice:
                success = True
    return success

while isValid:

    print (30 * '-')
    print ("   AWS - MENU")
    print (30 * '-')
    print ("1. Launch Bitmani Wordpress EC2")
    print ("2. Launch Ubuntu 64-bit EC2")
    print ("3. List instances")
    print ("4. Stop instance")
    print ("5. Start instance")
    print ("6. Reboot instance")
    print ("7. Terminate instance")
    print ("8. Exit")
    print (30 * '-')

    try :
        choice = int ( raw_input('Enter your choice [1-8] : ') )

    except ValueError, e :
        print ("'%s' is not a valid integer." % e.args[0].split(": ")[1])

    if choice == 1:
        reservation = ec2.run_instances('ami-c5f30081',
                                        key_name='california',
                                        instance_type='t2.micro',
                                        security_groups=['default'])

        instance = reservation.instances[0]
        print 'waiting for instance'
        while instance.state != 'running':
            print '.'
            time.sleep(5)
            instance.update()
        print 'done'
        instance.add_tag('Name','Wordpress-Server')

    elif choice == 2:
        reservation = ec2.run_instances('ami-df6a8b9b',
                                        key_name='california',
                                        instance_type='t2.micro',
                                        security_groups=['default'])

        instance = reservation.instances[0]
        print 'waiting for instance'
        while instance.state != 'running':
            print '.'
            time.sleep(5)
            instance.update()
        print 'done'
        instance.add_tag('Name','Ubuntu-Server')

    elif choice == 3:
        print_instances()

    elif choice == 4:
        print_instances()
        choice = raw_input('Enter the instance id to stop: ')
        if check_id(choice):
            stop_instance(choice)
        else:
            print "Instance id doesn't exist."

    elif choice == 5:
        print_instances()
        choice = raw_input('Enter the instance id to start: ')
        if check_id(choice):
            start_instance(choice)
        else:
            print "Instance id doesn't exist."

    elif choice == 6:
        print_instances()
        choice = raw_input('Enter the instance id to reboot: ')
        if check_id(choice):
            reboot_instance(choice)
        else:
            print "Instance id doesn't exist."

    elif choice == 7:
        print_instances()
        choice = raw_input('Enter the instance id to terminate: ')
        if check_id(choice):
            terminate_instance(choice)
        else:
            print "Instance id doesn't exist."

    elif choice == 8:
        isValid = 0

    else:
        exit(1)
