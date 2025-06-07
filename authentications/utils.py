

def validations(data,structer):
    initital_dict = {
        "error_status":False,
        "error":{

        }
    }
    for key,value in structer.items():
        if not isinstance(data.get(key),value):
            initital_dict['error_status'] = True
            initital_dict["error"][key] = f"please enter valide {key}"
        else:
            initital_dict[key] = data.get(key)
    return initital_dict
            