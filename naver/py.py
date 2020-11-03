    


user_data = {'gender' : None, 'height' : None, 'std_weight' : None}

def gender_input_func():
    print('남성과 여성 중 성별을 입력해 주세요')
    gender_data = input()
    return gender_data

def height_input_func():
    print('신장을 입력해 주세요')
    height_data = input()
    return height_data

def get_std_weight(gender, height):
    if gender == '남성':
        std_weight = ((int(height) ** 2) * 22) / 10000
        return std_weight
    else :
        std_weight = ((int(height) ** 2) * 21) / 10000
        return std_weight

def rip_number(std_weight):
    std_weight = round(std_weight,2)
    return std_weight

def user_data_update(gender, height, std_weight):
    user_data.update(gender=gender)
    user_data.update(height=height)
    user_data.update(std_weight=std_weight)

def print_result():
    print('키' + user_data.get('height') + ' ' + user_data.get('gender') + '의 표준 체중은' , user_data.get('std_weight'))

def init():
    gender = str(gender_input_func())
    if (gender == '남성') | (gender == '여성'):
        height = str(height_input_func())
        std_weight = get_std_weight(gender, height)
        std_weight = rip_number(std_weight)
        user_data_update(gender,height,std_weight)
        print_result()
    else :
        print('error')
        init()

init()
