# import our cooking_task from tasks
from tasks import cooking_task

# Dishes ordered for Table-1
table_1_dishes = ["Chicken Biryani", "Lemon chicken", "Pepper chicken"]

# Call the cooking_task.delay task with input parameters defined for that Task.
result = cooking_task.delay("Table-1", table_1_dishes)

# prints the task id
print(result)

table_2_dishes = ["Mutton Biryani", "Egg Biryani"]
result2 = cooking_task.apply_async(args=["Table-2", table_2_dishes])
print(result2)

table_3_dishes = ["Butter Naan", "Andhra Chicken"]
result3 = cooking_task.apply_async(args=["Table-3", table_3_dishes])
print(result3)

table_4_dishes = ["Chicken Manchurian", "Chicken Noodles"]
result4 = cooking_task.apply_async(args=["Table-4", table_4_dishes])
print(result4)
