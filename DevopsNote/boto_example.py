import boto3

def get_instance_state_by_key(instance:dict,key):
    if type(instance) == list:
        if len(instance) == 0:
            return None
        instance = instance[0]
    if key in instance.keys():
        return instance[key]
    else:
        for k in instance.keys():
            result = get_instance_state_by_key(instance[k],key)
            if result != None:
                return result
    

if __name__ == "__main__":
    ec2 = boto3.client("ec2")
    response = ec2.describe_instances()
    
    instance = response["Reservations"]
    id = get_instance_state_by_key(instance,"State")
    print(id)
