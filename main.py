from elementary_school_proto import serialize, deserialize

example_data = [
    None,
    3,
    5,
    26,
    9876543210,
    "Hello, F*ckupathlon!",
    "This is a text either... 9876543210",
    {"name": "Tyrion Lannister","age": 24,"tldr": "Drinks and knows things"},
    ["apple", "banana", "orange", 111],
    ["1 cica", ["HEJ"], {"a": 600, "b": [101]}]
]
for item in example_data:
    data = serialize(item)
    with open("saved.scp", "a") as f:
        f.write(data + '\n')
    print(deserialize(data))
