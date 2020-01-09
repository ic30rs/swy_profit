from pulp import *
import pulp.solvers
import pulp.solverdir
import model
import time
import frozen_dir


def main(consTime):
    foodList = model.readFood()

    c_list = list()
    consume_list = list()
    time_list = list()
    b_list = model.readFarm()

    for i in range(6):
        consume_list.append(list())

    for food in foodList:
        c_list.append(-food.price)
        for i in range(6):
            consume_list[i].append(food.getConsumption(i))
        time_list.append(food.time)

    if consTime:
        consume_list.append(time_list)
        b_list.append(model.readTime())

    V_NUM = len(foodList)
    variables = [pulp.LpVariable(foodList[i].name, lowBound=0, cat=pulp.LpInteger) for i in range(0, len(foodList))]
    # 目标函数
    c = c_list
    objective = sum([c[i] * variables[i] for i in range(0, V_NUM)])
    # 约束条件
    constraints = []

    for i, con in enumerate(consume_list):
        constraints.append(sum([con[i] * variables[i] for i in range(0, V_NUM)]) <= b_list[i])

    prob = LpProblem("swy_prob", LpMinimize)
    prob.addVariables(variables)
    for cons in constraints:
        prob.addConstraint(cons)
    prob.setObjective(objective)

    startTime = time.time()
    prob.solve(solver=COIN_CMD(path=frozen_dir.app_path() + "\\cbc.exe"))
    endTime = time.time()

    print("计算完成，用时" + str((endTime - startTime) / 1000) + "秒")
    print("最大盈利" + str(-value(objective)) + "贝币")

    for i, var in enumerate(variables):
        if value(var) != 0:
            print("制作 " + foodList[i].name + " " + str(value(var)) + "个")


if __name__ == '__main__':
    main(True)
    time.sleep(1000000)
