import json
import boto3
import time
import os
  

def lambda_handler(event, context):
    # TODO implement
    client = boto3.client('ec2')
    instance_Id_list = []
    response=client.describe_instances(
        Filters=[
            {'Name': 'tag-key', 'Values': ['nishu']},
            # { 'Name': 'instance-state-name','Values': ['running'] }
        ]
         )  
    for each in response['Reservations']:
        for i in each['Instances']:
            instance_Id_list.append(i['InstanceId']) #list of all instance id
    for each in range(len(instance_Id_list)):
        response_create_image = client.create_image(
        InstanceId=instance_Id_list[each],
        Name='migration-test-karan'+str(each),
        NoReboot=True,
        )    
    # print(response_create_image)
    # print(instance_Id_list)
        images = client.describe_images(ImageIds=[response_create_image["ImageId"]])
        for image in images["Images"]:
            img=image["State"]
            print(img)
            if img == 'failed':
                print("AMI creation failed for instance:" ,instance_Id_list[each])
            elif img == 'pending':
                while True:
                    if img == 'failed':
                        print("AMI creation failed for instance:" ,instance_Id_list[each])
                        break
                    elif img == 'available':
                        print("AMI creation completed for instance:" ,instance_Id_list[each])
                        break
                    else:
                        time.sleep(20)
                        images = client.describe_images(ImageIds=[response_create_image["ImageId"]])
                        for image in images["Images"]:
                            img=image["State"]
