'''
You have a list of students. Each student has:
	•	A name
	•	A list of their exam scores

You want to:
	1.	Filter out students who failed (average score < 40)
	2.	Map each student to their average score
	3.	Sort students by their average score
	4.	Reduce to get the total class score
	5.	Use lambda throughout for compact logic
students = [
    {"name": "Alice", "scores": [85, 90, 88]},
    {"name": "Bob", "scores": [40, 35, 45]},
    {"name": "Charlie", "scores": [20, 30, 25]},
    {"name": "Diana", "scores": [70, 60, 75]},
]
'''

from functools import reduce

students = [
    {"name": "Alice", "scores": [85, 90, 88]},
    {"name": "Bob", "scores": [40, 30, 45]},
    {"name": "Charlie", "scores": [20, 30, 25]},
    {"name": "Diana", "scores": [70, 60, 75]},
]


averaged = list(map(lambda s: (s["name"], sum(s["scores"]) / len(s["scores"])), students))

passed = list(filter(lambda s: s[1] >= 40, averaged))


sorted_by_avg = sorted(averaged, key=lambda s: s[1])

total_class_score = reduce(lambda acc, s: acc + s[1], sorted_by_avg, 0)

failed_students = list(map(lambda s: s[0], list(filter(lambda s: s[1] < 40, averaged))))

print("Sorted Passed Students with Averages:", sorted_by_avg)
print("Failed Students:", failed_students)
print("Total Class Score:", total_class_score)


