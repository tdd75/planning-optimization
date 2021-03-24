import pandas as pd
import random
import math

# Tính xác suất cho các thuộc tính rời rạc


def cal_discrete_prob(x, training_data, col_name):
    m = len(training_data)
    n = len(training_data[training_data[col_name] == x])
    return n/m

# Tính xác suất theo phân phối gauss cho các thuộc tính liên tục


def cal_continous_prob(x, mean, stdev):
    print(stdev)
    e = float(math.exp(-pow((x-mean), 2)/(2*pow(stdev, 2))))
    return float(e/(math.sqrt(2*math.pi*pow(stdev, 2))))

# Tính xác suất cho input đầu vào


def cal_class_prob(training_data, inputVector):
    columns = ['report', 'age', 'income', 'share', 'expenditure', 'owner', 'selfemp', 'dependents', 'months',
               'majorcard', 'active']
    prob = 1
    for i in columns:
        if i == "selfemp" or i == "owner":
            prob = prob*cal_discrete_prob(inputVector[i], training_data, i)
        else:
            prob = prob * \
                cal_continous_prob(
                    inputVector[i], training_data[i].mean(), training_data[i].std())
    return prob


def cal_tag_prob(training_data):
    count_yes = len(training_data[training_data["card"] == "yes"])
    count_no = len(training_data[training_data["card"] == "no"])
    all = len(training_data)
    return float(count_yes/all), float(count_no/all)

# Dự đoán


def predict(training_data, inputVector):
    tag_prob = cal_tag_prob(training_data)
    prob_yes = cal_class_prob(
        training_data[training_data["card"] == "yes"], inputVector)*tag_prob[0]
    prob_no = cal_class_prob(
        training_data[training_data["card"] == "no"], inputVector)*tag_prob[1]
    if prob_yes > prob_no:
        return "yes"
    else:
        return "no"

# Check kết quả


def compare(training_data, testing_data):
    true_case = 0
    for i in range(len(testing_data)):
        if predict(training_data, testing_data.iloc[i]) == testing_data.iloc[i]["card"]:
            true_case = true_case+1
    return true_case/len(testing_data)


dataset = pd.read_csv(
    r'E:\Users\Vu\Documents\PycharmProject\ML\AER_credit_card_data.csv')
# split data
ratio = 0.7
test_list = dataset.values.tolist()
train_size = int(len(test_list)*ratio)
i = 0
train_list = []
while i != train_size:
    index = random.randrange(len(test_list) - 1)
    train_list.append(test_list[index])
    test_list.pop(index)
    i = i + 1
train_data = pd.DataFrame(train_list, columns=['card', 'report', 'age', 'income', 'share',
                          'expenditure', 'owner', 'selfemp', 'dependents', 'months', 'majorcard', 'active'])
test_data = pd.DataFrame(test_list, columns=['card', 'report', 'age', 'income', 'share',
                         'expenditure', 'owner', 'selfemp', 'dependents', 'months', 'majorcard', 'active'])
print(compare(train_data, test_data))
