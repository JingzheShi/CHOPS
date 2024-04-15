PREFIX = 'logs_MAIN_EXP_for_INs\Cgpt3.5Egpt3.5Vgpt3.5_24032811'
INPUT = True
NAME_LIST = [
        '_instructions_augmentedclassifier_input_words.txt',
        '_instructions_augmentedexecutor_input_words.txt',
        '_instructions_augmentedverifier_input_words.txt',
        '_newQAsclassifier_input_words.txt',
        '_newQAsexecutor_input_words.txt',
        '_newQAsverifier_input_words.txt',
    ]

if INPUT:
    pass
else:
    NAME_LIST = [
        name.replace('_input_words.txt', '_output_words.txt') for name in NAME_LIST
    ]


# FILE_PATHS = [f'{PREFIX}{name}' for name in NAME_LIST]
FILE_PATHS = [
    'logs_MAIN_EXP_for_INs\Cgpt3.5Egpt4NoVerifyVgpt3.5_24032811_instructions_augmentedexecutor_output_words.txt',
    'logs_MAIN_EXP_for_INs\Cgpt3.5Egpt4Vgpt3.5_24032811_newQAsexecutor_output_words.txt',
]

# Initialize a counter
char_count = 0

# Open the file and count the characters
for file_path in FILE_PATHS:
    with open(file_path, 'r') as file:
        for line in file:
            char_count += len(line)
    print("char count:", char_count)

avg_char_count = char_count / (102+104) / 1000

# Print the result
print(f'Total number of characters in the file: {char_count}')
print('Average Question characters: {0:.2f}k'.format(avg_char_count))