import parser


def lean_to_html(input_file=None, output_file=None, input_string=None):
    if input_file is not None and input_string is not None:
        raise ValueError("Cannot set both input_file and input_string")
    if input_file is not None:
        file = open(input_file)
        input_string = file.read()
        file.close()
    leanhtml = parser.transform(input_string)
    output = leanhtml.to_html()
    if output_file is None:
        print(output)
    else:
        file = open(output_file, "w")
        file.write(output)
        file.close()
