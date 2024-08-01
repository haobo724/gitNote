import boto3

def get_instance_state_by_key(instance:dict,key,parent_key=[]):
    if type(instance) == list:
        if len(instance) == 0:
            return None
        instance = instance[0]
    if key in instance.keys():
        return instance[key],parent_key
    else:
        for k in instance.keys():
            parent_key.append(k)
            result = get_instance_state_by_key(instance[k],key,parent_key)
            if result != None:
                return result, parent_key
            parent_key.remove(k)    
    

if __name__ == "__main__":
    ec2 = boto3.client("ec2")
    response = ec2.describe_instances()
    
    instance = response["Reservations"]
    id,parent_key = get_instance_state_by_key(instance,"State")
    print(id)
    print(parent_key)
