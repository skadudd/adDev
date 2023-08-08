import pandas as pd

points_list = [0] * 8

def result_deco(func):
    def wrapper(*args, **kwargs):
        global points_list
        question_no, points, result = func(*args, **kwargs)
        if result:
            points_list[question_no] = points
            print(f'정답입니다! {points}점 누적 되었습니다!')
        else:
            points_list[question_no] = 0
            print('오답입니다. 다시 한번 확인해주세요.')       

        print('현재 누적 점수:', sum(points_list), '/ 100')
        
    return wrapper

# 1-1
@result_deco
def check_01_01(df: pd.core.frame.DataFrame):
    question_no, points = 0, 10

    try:
        def try_except(df: pd.core.frame.DataFrame):
            try:
                return len(df.구분.unique()) == 3
            except:
                return False
        
        condition_dict = {
            'condition01': len(df) == 318,
            'condition02': sum('(' in col for col in df.columns) == 0,
            'condition03': df.columns[3:].is_monotonic_increasing,
            'condition04': try_except(df),
        }

        if sum(condition_dict.values()) == len(condition_dict):
            result = True
        else:
            result = False
    except:
        result = False
        
    return question_no, points, result

# 1-2
@result_deco
def check_01_02(df: pd.core.frame.DataFrame):
    question_no, points = 1, 10
    
    try:
        def try_except(df: pd.core.frame.DataFrame):
            try:
                return len(df.구분.unique()) == 3
            except:
                return False
        
        def try_except_value(value):
            try:
                return all(['(' not in value, ' ' not in value])
            except:
                return False
        
        condition_dict = {
            'condition01': len(df) == 318,
            'condition02': sum('(' in col for col in df.columns) == 0,
            'condition03': try_except(df),
            'condition04': df.구분.apply(try_except_value).sum() == len(df),
        }

        if sum(condition_dict.values()) == len(condition_dict):
            result = True
        else:
            result = False
    except:
        result = False

    return question_no, points, result

# 1-3
@result_deco
def check_01_03(df: pd.core.frame.DataFrame):
    question_no, points = 2, 10

    try:
        def try_except(df: pd.core.frame.DataFrame):
            try:
                return len(df.구분.unique()) == 3
            except:
                return False
        
        def try_except_value(value):
            try:
                return all(['(' not in value, ' ' not in value])
            except:
                return False
        
        condition_dict = {
            'condition01': len(df) == 318,
            'condition02': sum('(' in col for col in df.columns) == 0,
            'condition03': try_except(df),
            'condition04': df.구분.apply(try_except_value).sum() == len(df),
            'condition05': df.isna().sum().sum() == 0,
            'condition06': sum(df[col].dtype == int for col in df.columns[3:]) == len(range(1988, 2021+1)),
            'condition07': df.applymap(lambda value: value == 0).sum().sum() == 5549,
        }

        if sum(condition_dict.values()) == len(condition_dict):
            result = True
        else:
            result = False
    except:
        result = False

    return question_no, points, result

# 1-4
@result_deco
def check_01_04(df: pd.core.frame.DataFrame):
    question_no, points = 3, 10
    
    try:
        condition_dict = {
            'condition01': len(df) == 318,
            'condition02': df.isna().sum().sum() == 0,
            'condition03': sum(idx == '소계' for idx_3 in df.index for idx in idx_3) == 0,
            'condition04': df.index.names == ['자치구', '사고유형', '구분'],
            'condition05': df.sum().sum() == 7352573,
        }

        if sum(condition_dict.values()) == len(condition_dict):
            result = True
        else:
            result = False
    except:
        result = False
        
    return question_no, points, result

# 1-5
@result_deco
def check_01_05(df: pd.core.frame.DataFrame):
    question_no, points = 4, 10
    
    try:
        condition_dict = {
            'condition01': len(df) == 318,
            'condition02': (df == 0).sum().sum() == 5549 - len(range(17)),
            'condition03': sum(idx == '소계' for idx_3 in df.index for idx in idx_3) == 0,
            'condition04': df.index.names == ['자치구', '사고유형', '구분'],
            'condition05': df[df['1988']!=0].iloc[:,:17].sum(axis=1).sum()/2 == 820161,
        }

        if sum(condition_dict.values()) == len(condition_dict):
            result = True
        else:
            result = False
    except:
        result = False
        
    return question_no, points, result

# 2-1
@result_deco
def check_02_01(df: pd.core.frame.DataFrame):
    question_no, points = 5, 10
    
    try:
        condition_dict = {
            'condition01': len(df) == 107,
            'condition02': (df == 0).sum().sum() == 1787,
            'condition03': df.iloc[[105]].max(axis=1).values[0] == 1164,
            'condition04': df.index.names == ['자치구', '사고유형', '구분'][:-1],
            'condition05': df['1997'].sum()/2 == df['1997'].iloc[0],
        }

        if sum(condition_dict.values()) == len(condition_dict):
            result = True
        else:
            result = False
    except:
        result = False
        
    return question_no, points, result

# 2-2
@result_deco
def check_02_02(df: pd.core.frame.DataFrame):
    question_no, points = 6, 20
    
    type_list = ['합계', '차대사람', '차대차', '차량단독', '건널목']
    gu_list = ['서울시', '종로구', '중구', '용산구', '성동구', '광진구', '동대문구', '중랑구', '성북구', '강북구', '도봉구', '노원구', '은평구', '서대문구', '마포구', '양천구', '강서구', '구로구', '금천구', '영등포구', '동작구', '관악구', '서초구', '강남구', '송파구', '강동구']
    
    try:
        condition_dict = {
            'condition01': len(df) == 104,
            'condition02': (df==0).sum().sum() == 112,
            'condition03': all(df.loc['합계'].index == gu_list) and all(df.index.get_level_values(0).unique() == type_list[:-1]),
            'condition04': all(df.columns == list(map(str, range(2005, 2022)))),
            'condition05': (df.iloc[23, 4], df.iloc[12, 6], df.iloc[98, 11]) == (27, 20, 1),
        }

        if sum(condition_dict.values()) == len(condition_dict):
            result = True
        else:
            result = False
    except:
        result = False
        
    return question_no, points, result

# 3
@result_deco
def check_03(df: pd.core.frame.DataFrame):
    question_no, points = 7, 20
    
    type_list = ['합계', '차대사람', '차대차', '차량단독', '건널목']
    gu_list = ['서울시', '종로구', '중구', '용산구', '성동구', '광진구', '동대문구', '중랑구', '성북구', '강북구', '도봉구', '노원구', '은평구', '서대문구', '마포구', '양천구', '강서구', '구로구', '금천구', '영등포구', '동작구', '관악구', '서초구', '강남구', '송파구', '강동구']
    
    try:
        condition_dict = {
            'condition01': len(df) == 104,
            'condition02': (df < 1).sum().sum() == 798,
            'condition03': all(df.index.get_level_values(0).unique() == gu_list) and all(df.loc['용산구'].index.unique() == type_list[:-1]),
            'condition04': all(df.columns == list(map(str, range(2005, 2022)))),
            'condition05': (df.iloc[23, 4], df.iloc[12, 6], df.iloc[98, 11]) == (8.11, 0.77, 0.32),
        }

        if sum(condition_dict.values()) == len(condition_dict):
            result = True
        else:
            result = False
    except:
        result = False
        
    return question_no, points, result