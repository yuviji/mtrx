import json

with open('business_data.json', 'r') as file:
    data = json.load(file)

nums = []

for business in data:
    business_name = business.get("business_name")
    nums.append(len(business.get("business_reviews", [])))
    if nums[-1] < 50:
        print(f"{business_name}: {nums[-1]}")
        # data.remove(business)

print(min(nums))
print(max(nums))
# with open('business_data.json', 'w') as file:
#     json.dump(data, file, indent=4) 