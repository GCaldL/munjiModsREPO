import openai
import time

openai.api_key = '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'


def Generate_Addresses(address):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a chatbot"},
            {"role": "user",
             "content": '''
            Input Text:29 Watervale Place Calamvale Brisbane City Queensland 4116 Jayden Pearce 31 Cerulean Rd Karnup 6176 Wa Phillip Myers
            Name:, Street: Address:, Suburb:, City:, State:, Postcode:
Jayden Pearce, 29 Watervale Place, Calamvale, Brisbane City, QLD, 4116
Phillip Myers, 31 Cerulean Rd,              , Karnup       ,WA, 6176
            '''},
            {"role": "user",
             "content": "Input Text: " + address},
        ]
    )

    result = ''
    for choice in response.choices:
        result += choice.message.content
    return result


path = 'input_addresses.txt'

input_file = open(path, 'r')
input_lines = input_file.readlines()

input_text = ""

line_index = 0
output_csv = open("./output.csv", "a")
csv_header = "Name, Street Address, Suburb, City, State, Postcode"

output_csv.write(csv_header)
for line in input_lines:
    line_index += 1
    input_text += line
    # limit lines to 25 at a time
    if line_index > 25:
        print("THIS MESS OF AN INPUT:")
        print(input_text)
        fixed_addresses = Generate_Addresses(input_text)
        print("AI GENERATED RESULTS:")
        print(csv_header)
        print(fixed_addresses)
        output_csv.write(fixed_addresses)
        # API request limits :(
        time.sleep(21)
        # reset stuff
        input_text = ""
        line_index = 0
output_csv.close()
